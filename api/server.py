from fastapi import FastAPI
from kafka import KafkaConsumer
import json

app = FastAPI()

consumer = KafkaConsumer(
    "prediction_topic",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

@app.get("/stream")
def stream():
    for msg in consumer:
        return msg.value