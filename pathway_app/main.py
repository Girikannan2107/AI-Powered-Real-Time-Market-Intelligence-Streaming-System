import pathway as pw
from agents import sentiment, volatility, predict, brokerage

# ---------------------
# Define Schemas
# ---------------------

class NewsSchema(pw.Schema):
    symbol: str
    title: str


class MarketSchema(pw.Schema):
    symbol: str
    price: float


# ---------------------
# Kafka Configuration (IMPORTANT FIX)
# ---------------------

KAFKA_CONFIG = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "pathway-group",
    "auto.offset.reset": "earliest"
}

# ---------------------
# Read Kafka Streams
# ---------------------

news = pw.io.kafka.read(
    rdkafka_settings=KAFKA_CONFIG,
    topic="news_topic",
    schema=NewsSchema,
    format="json"
)

market = pw.io.kafka.read(
    rdkafka_settings=KAFKA_CONFIG,
    topic="market_topic",
    schema=MarketSchema,
    format="json"
)

# ---------------------
# Apply Agents
# ---------------------

news_processed = news.select(
    symbol=news.symbol,
    title=news.title,
    sentiment_score=pw.apply(sentiment, news.title)
)

market_processed = market.select(
    symbol=market.symbol,
    price=market.price,
    vol=pw.apply(volatility, market.price)
)

# ---------------------
# Join Streams
# ---------------------

joined = news_processed.join(
    market_processed,
    news_processed.symbol == market_processed.symbol
)

# ---------------------
# Prediction Logic
# ---------------------

result = joined.select(
    symbol=joined.symbol,
    title=joined.title,
    recommendation=pw.apply(
        lambda s, v: predict(s, v)[0],
        joined.sentiment_score,
        joined.vol
    ),
    confidence=pw.apply(
        lambda s, v: predict(s, v)[1],
        joined.sentiment_score,
        joined.vol
    ),
    price=joined.price,
    brokerage_cost=pw.apply(brokerage, joined.price)
)

# ---------------------
# Add RAG Layer
# ---------------------
final = result

# ---------------------
# Write Output to Kafka
# ---------------------
pw.io.kafka.write(
    result,
    {"bootstrap.servers": "kafka:9092"},
    "prediction_topic",
    format="json",
)
# ---------------------
# Run Streaming Engine
# ---------------------

pw.run()