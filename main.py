import logging
from multiprocessing import Queue

from processes_classes.image_loader import ImageLoader
from processes_classes.image_transmitter import ImageTransmitter


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        config = {
            'bootstrap.servers': 'kafka:29092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        }
        topic = 'test_topic'
        image_queue = Queue()
        transmitter = ImageTransmitter(config, topic, image_queue)
        loader = ImageLoader(image_queue)
        transmitter.start()
        loader.start()
    except KeyboardInterrupt:
        transmitter.terminate()
        transmitter.join()
        loader.terminate()
        loader.join()
        logging.info("Extra program finish")


