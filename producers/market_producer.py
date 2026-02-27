import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Optional

import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

logger = logging.getLogger(__name__)


# =====================================================
# Domain Layer
# =====================================================

@dataclass(frozen=True)
class MarketEvent:
    """
    Immutable domain event representing a market snapshot.

    Domain objects must remain infrastructure-agnostic.
    """
    symbol: str
    price: float
    timestamp: float


# =====================================================
# Abstraction Layer (Dependency Inversion)
# =====================================================

class PriceFetcher(ABC):
    """Contract for any market price provider."""

    @abstractmethod
    def fetch(self) -> Optional[MarketEvent]:
        pass


class EventProducer(ABC):
    """Contract for any event publishing system."""

    @abstractmethod
    def send(self, topic: str, event: MarketEvent) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class RetryPolicy(ABC):
    """Defines retry strategy behavior."""

    @abstractmethod
    def execute(self, func):
        pass


# =====================================================
# Infrastructure Layer
# =====================================================

class AlphaVantageClient(PriceFetcher):
    """
    Concrete implementation of PriceFetcher.

    Isolated external API logic.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str, symbol: str = "AAPL") -> None:
        self.api_key = api_key
        self.symbol = symbol

    def fetch(self) -> Optional[MarketEvent]:
        if not self.api_key:
            raise ValueError("API key not configured")

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": self.symbol,
            "apikey": self.api_key,
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)
        data = response.json()

        quote = data.get("Global Quote")

        if not quote or "05. price" not in quote:
            logger.warning("Invalid API response")
            return None

        return MarketEvent(
            symbol=self.symbol,
            price=float(quote["05. price"]),
            timestamp=time.time(),
        )


class ExponentialBackoffRetry(RetryPolicy):
    """
    Implements exponential backoff retry pattern.
    """

    def __init__(self, max_retries: int = 5, base_delay: int = 2) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay

    def execute(self, func):
        for attempt in range(self.max_retries):
            try:
                return func()
            except NoBrokersAvailable:
                delay = self.base_delay ** attempt
                logger.warning("Retrying in %s seconds...", delay)
                time.sleep(delay)

        raise ConnectionError("Max retries exceeded")


class KafkaProducerAdapter(EventProducer):
    """
    Kafka implementation of EventProducer interface.
    """

    def __init__(self, bootstrap_servers: str, retry_policy: RetryPolicy) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.retry_policy = retry_policy
        self.producer = self._connect()

    def _connect(self) -> KafkaProducer:
        def connect():
            return KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )

        return self.retry_policy.execute(connect)

    def send(self, topic: str, event: MarketEvent) -> None:
        self.producer.send(topic, asdict(event))
        logger.info(
            "Event sent | Symbol=%s | Price=%.2f",
            event.symbol,
            event.price,
        )

    def close(self) -> None:
        self.producer.close()


# =====================================================
# Application Service Layer
# =====================================================

class MarketProducerService:
    """
    Application orchestrator.

    Depends ONLY on abstractions (PriceFetcher, EventProducer).
    This enables:
        - Easy testing with mocks
        - Swappable infrastructure
        - Clean separation of concerns
    """

    def __init__(
        self,
        fetcher: PriceFetcher,
        producer: EventProducer,
        topic: str,
        interval: int,
    ) -> None:
        self.fetcher = fetcher
        self.producer = producer
        self.topic = topic
        self.interval = interval
        self._running = True

    def run_once(self) -> None:
        event = self.fetcher.fetch()

        if event:
            self.producer.send(self.topic, event)

    def start(self) -> None:
        logger.info("Market Producer Started")

        try:
            while self._running:
                self.run_once()
                time.sleep(self.interval)

        finally:
            self.producer.close()

    def stop(self) -> None:
        self._running = False
