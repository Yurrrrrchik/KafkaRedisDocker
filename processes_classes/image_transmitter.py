import logging
from multiprocessing import Process

from confluent_kafka import Consumer, KafkaError
from numpy import frombuffer, float32


class ImageTransmitter(Process):
    """
    The process takes as parameters Kafka consumer config,
    the name of the topic consumer will be subscribed for
    and the queue where the array of images will be placed.
    """
    def __init__(self, config, topic, image_queue):
        Process.__init__(self)
        self.image_queue = image_queue
        self.config = config
        self.topic = topic

    def run(self):
        """
        Initializes a Kafka consumer with the given
        configuration, subscribes to a given topic,
        enters an infinite loop to poll for messages.
        Value of a recieved message gets converted from
        a byte array to a NumPy array of type float32.
        Tuple of message key and NumPy array places
        into a queue for further processing.
        """
        try:
            consumer = Consumer(self.config)
            consumer.subscribe([self.topic])

            while True:
                message = consumer.poll()

                if message is None:
                    continue

                if message.error():

                    if message.error().code() == KafkaError._PARTITION_EOF:
                        logging.error(f'Reached end of topic {message.topic()} [{message.partition()}] '
                                      f'at offset {message.offset()}')

                    else:
                        logging.error(f'Error occured: {message.error()}')

                else:
                    image_array = frombuffer(message.value(), dtype=float32)
                    self.image_queue.put((message.key(), image_array))
                    logging.info(f"{message.key()} is in queue")

        except ValueError:
            pass

        except KeyboardInterrupt:
            consumer.close()
