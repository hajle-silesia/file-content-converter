import base64
import json
import threading

import fastapi
import kafka

from src.file_content_converter import FileContentConverter


def load_events():
    consumer = kafka.KafkaConsumer(bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
                                   value_deserializer=lambda message: json.loads(base64.b64decode(message).decode()),
                                   )
    consumer.subscribe(topics=["file-content-monitor-topic"])
    for event in consumer:
        file_content_converter.update(event.value)


app = fastapi.FastAPI()

producer = kafka.KafkaProducer(bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
                               value_serializer=lambda message: base64.b64encode(
                                   json.dumps(message, default=str).encode()),
                               )
file_content_converter = FileContentConverter(producer)

events_thread = threading.Thread(target=load_events)
events_thread.start()


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


@app.get("/content")
async def content():
    return {"content": file_content_converter.content,
            }
