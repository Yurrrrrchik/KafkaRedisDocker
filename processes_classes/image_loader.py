import json
import logging
from multiprocessing import Process
import os
import time

from PIL import Image
from redis import Redis


r = Redis(host='redis', port=6379, db=0)


class ImageLoader(Process):
    """
    The process takes as parametr queue
    from which NumPynarrays will be taken.
    """
    def __init__(self, image_queue):
        Process.__init__(self)
        self.image_queue = image_queue

    def run(self):
        """
        Enters an infinite loop and gets filenames and
        NumPy arrays from queue, converts arrays to image.
        Images are being saved in folder "saved_images"
        with a corresponding filename. Information about image
        such as image path, save time and image size is being
        saved in redis with file name as a key.
        """
        while True:
            filename, blob = self.image_queue.get()
            logging.info(f"{filename} is taken from queue")
            image_path = os.path.join('saved_images', str(filename)[2:-1])
            image = Image.fromarray(blob)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(image_path)
            save_time = time.localtime()
            image_size = os.path.getsize(image_path)
            image_info = {'path': image_path, 'timestamp': save_time, 'size': image_size}
            r.set(filename, json.dumps(image_info))
            logging.info(f"{filename} data is saved in redis")