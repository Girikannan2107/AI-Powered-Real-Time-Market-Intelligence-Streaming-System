import os
import json
import time
import requests
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
# Wait until Kafka is ready
producer = None
while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Connected to Kafka ✅ (Market Producer)")
    except NoBrokersAvailable:
        print("Kafka not ready, retrying...")
        time.sleep(5)


def fetch_price():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": "AAPL",
        "apikey": ALPHA_VANTAGE_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "Global Quote" in data and data["Global Quote"]:
            return {
                "symbol": "AAPL",
                "price": float(data["Global Quote"]["05. price"]),
                "timestamp": time.time()
            }

        return None

    except Exception as e:
        print("Market fetch error:", e)
        return None


while True:
    market_data = fetch_price()

    if market_data:
        producer.send("market_topic", market_data)
        print("Sent market:", market_data)

    time.sleep(20)