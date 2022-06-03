import os
import json
import logging
from datetime import datetime, timedelta

from kafka import KafkaConsumer

TOPIC_NAME = 'locations'
# KAFKA_SERVER = 'host.docker.internal:9092'
KAFKA_SERVER = os.environ.get("KAFKA_URI", "kafka:9092")
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

def create(location):
    conn = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    cur = conn.cursor()

    person_id = location["person_id"]
    creation_time = datetime.now()
    latitude = int(location["latitude"])
    longitude = int(location["longitude"])

    # table_insert = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))" \
    #     .format(user_id, latitude, longitude)
    table_insert = "INSERT INTO location (person_id, creation_time, coordinate) VALUES ({}, {}, ST_Point({}, {}))" \
        .format(person_id, creation_time, latitude, longitude)

    print(table_insert)
    cur.execute(table_insert)

for message in consumer:
    new_location = create(json.loads(message.value))
    print(new_location)


