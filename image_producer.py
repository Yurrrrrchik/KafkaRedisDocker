from base64 import b64encode
import os

from confluent_kafka import Producer, Consumer

def produce_images():
    """
    Initializes a Kafka producer with the specified configuration
    and iterates over all image files in the 'images' directory.
    Opens each image file in binary read mode, reads the image data
    and encodes it in base64 format. Sends the encoded image data to
    a Kafka topic named 'test_topic', using the filename as the key.
    Flushes the producer to ensure that all messages are sent.
    """
    config = {'bootstrap.servers': 'localhost:9092',}
    producer = Producer(config)

    for filename in os.listdir('images'):

        with open(os.path.join('images', filename), "rb") as image_file:
            blob = b64encode(image_file.read())
            producer.produce('test_topic', key=filename, value=blob)
            producer.flush()


if __name__ == '__main__':
    produce_images()