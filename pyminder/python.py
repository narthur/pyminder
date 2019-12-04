import time
import random
import datetime
import os


class Python:
    @staticmethod
    def print(*lines):
        if not lines:
            print('')

        for line in lines:
            print(line)

    @staticmethod
    def input(prompt):
        return input(prompt)

    @staticmethod
    def sleep(secs):
        time.sleep(secs)

    @staticmethod
    def random_choice(items):
        return random.choice(items)

    @staticmethod
    def time_now():
        return time.time()

    @staticmethod
    def date_now():
        return datetime.datetime.now()

    def open_file(self, rel_path):
        return open(os.path.join(self.get_base_dir(), rel_path), 'rb')

    @staticmethod
    def get_base_dir():
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
