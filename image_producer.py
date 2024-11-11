import confluent_kafka
from confluent_kafka import Producer, Consumer
import base64
import os


config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

producer = Producer(config)

def send_message(topic, key, message):
    producer.produce(topic, key=key, value=message)
    producer.flush()

for filename in os.listdir('images'):
    with open(os.path.join('images', filename), "rb") as image_file:
        blob = base64.b64encode(image_file.read())
        send_message('test_topic', filename, blob)