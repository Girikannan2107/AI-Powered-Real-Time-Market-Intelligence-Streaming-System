import json
import time
import random
from kafka import KafkaProducer


news_data = {
    "symbol": "AAPL",
    "title": headline,
    "sentiment": sentiment,
    "price": random.uniform(250, 280),  # ADD THIS
    "timestamp": time.time()
}

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

while True:
    news_data = {
        "symbol": "AAPL",
        "title": random.choice([   # 🔥 FIXED HERE
            "Market crashes",
            "Stock surges",
            "Tech rally",
            "Economic slowdown"
        ]),
        "sentiment": random.choice(["positive", "negative"]),
        "timestamp": time.time()
    }

    producer.send("news_topic", news_data)
    producer.flush()

    print("Sent news:", news_data)
    time.sleep(5)