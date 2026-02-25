import pathway as pw
from agents import sentiment, volatility, predict, brokerage

# -----------------------------
# Schema (MATCH GENERATOR)
# -----------------------------
class NewsSchema(pw.Schema):
    symbol: str
    title: str
    price: float
    timestamp: float

KAFKA_CONFIG = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "pathway-group",
    "auto.offset.reset": "latest",
}

news = pw.io.kafka.read(
    rdkafka_settings=KAFKA_CONFIG,
    topic="news_topic",
    schema=NewsSchema,
    format="json",
)

processed = news.select(
    symbol=news.symbol,
    title=news.title,
    price=news.price,
    timestamp=news.timestamp,  # IMPORTANT
    sentiment_score=pw.apply(sentiment, news.title),
    volatility_score=pw.apply(volatility, news.price),
)

result = processed.select(
    symbol=processed.symbol,
    title=processed.title,
    price=processed.price,
    timestamp=processed.timestamp,
    recommendation=pw.apply(
        lambda s, v: predict(s, v)[0],
        processed.sentiment_score,
        processed.volatility_score,
    ),
    confidence=pw.apply(
        lambda s, v: predict(s, v)[1],
        processed.sentiment_score,
        processed.volatility_score,
    ),
    brokerage_cost=pw.apply(brokerage, processed.price),
)

pw.io.kafka.write(
    result,
    rdkafka_settings={"bootstrap.servers": "kafka:9092"},
    topic_name="prediction_topic",
    format="json",
)

pw.run()