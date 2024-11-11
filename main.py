import time

import confluent_kafka
import multiprocessing
from confluent_kafka import Producer, Consumer
#import sys, types
import numpy
import redis
import os
import json
from PIL import Image
#import dill
from queue import Empty

config = {
    'bootstrap.servers': 'host:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

r = redis.Redis(host='host', port=6379, db=0)

processes = []
#def close_consumer(consumer):
#    consumer.close()

class FirstProcess(multiprocessing.Process):
    def __init__(self, config, image_queue):
        multiprocessing.Process.__init__(self)
        self.image_queue = image_queue
        self.config = config

    def run(self):
        try:
            consumer = Consumer(config)
            consumer.subscribe(['test_topic'])
            while True:
                message = consumer.poll(timeout=1.0)
                if message is None:
                    print("No messages i guess")
                else:
                    image_array = numpy.frombuffer(message.value(), dtype=numpy.float32)
                    self.image_queue.put((message.key(), image_array))
                    print(message.key(), ' in queue')
        except KeyboardInterrupt:
            consumer.close()
            for process in processes:
                process.join()
            print("The end.")
        except AttributeError:
            print("No messages i guess")


class SecondProcess(multiprocessing.Process):
    def __init__(self, image_queue):
        multiprocessing.Process.__init__(self)
        self.image_queue = image_queue

    def run(self):
        try:
            while True:
                filename, blob = self.image_queue.get()
                print(filename, ' got from queue')
                image_path = os.path.join('saved_images', str(filename)[2:-1])
                image = Image.fromarray(blob)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                print(image_path)
                image.save(image_path)
                save_time = time.localtime()
                image_size = os.path.getsize(image_path)
                image_info = {'path': image_path, 'timestamp': save_time, 'size': image_size}
                r.set(filename, json.dumps(image_info))
                print(r.get(filename))
        except Empty:
            print("Empty queue")
        except KeyboardInterrupt:
            print("The end.")


if __name__ == '__main__':
    print("work pleeeeeaaaaaaaaaaaaaaaaaseeeeee")
    r.set('a', 7)
    image_queue = multiprocessing.Queue()
    fp = FirstProcess(config, image_queue)
    fp.start()
    processes.append(fp)
    sp = SecondProcess(image_queue)
    sp.start()
    processes.append(sp)