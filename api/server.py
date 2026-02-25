from fastapi import FastAPI
from kafka import KafkaConsumer
import json

app = FastAPI()

consumer = KafkaConsumer(
    "prediction_topic",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

latest_data = {}

@app.get("/latest")
def get_latest():
    global latest_data
    for message in consumer:
        latest_data = message.value
        break
    return latest_data