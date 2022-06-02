import os
import json

from kafka import KafkaConsumer

from wsgi import app
from app.udaconnect.services import LocationService

TOPIC_NAME = 'locations'
# KAFKA_SERVER = 'host.docker.internal:9092'
KAFKA_SERVER = os.environ.get("KAFKA_URI", "kafka:9092")


with app.app_context():
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)
    for message in consumer:
        LocationService.create(json.loads(message.value))
