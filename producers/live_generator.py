import time
import random
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

titles = [
    "Market crashes",
    "Tech rally",
    "Economic slowdown",
    "Stock surges",
    "Strong quarterly earnings",
    "Global uncertainty rises"
]

while True:
    data = {
        "symbol": "AAPL",
        "title": random.choice(titles),
        "price": round(random.uniform(260, 300), 2),  # ADD THIS
        "timestamp": time.time()
    }

    producer.send("news_topic", data)
    print("Generated:", data)

    time.sleep(2)