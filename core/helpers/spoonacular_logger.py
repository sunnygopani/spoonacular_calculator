# importing module
import logging
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(BASE_DIR, "settings/constants.json")) as f:
    data = json.load(f)
f.close()


class Logger:

    def __init__(self, filepath=""):
        self.FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(filename)s:%(lineno)s - %(funcName)5s() - "
                                           "%(message)s")
        self.LOG_FILE = filepath if filepath else os.path.join(BASE_DIR, "logs\{:%Y-%m-%d}.log").format(
            datetime.now())
        self.LOG_LEVEL = data['LOGGING_LEVEL']

    @property
    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.LOG_FILE, when='midnight')
        file_handler.setFormatter(self.FORMATTER)
        return file_handler

    def get_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_file_handler)
        logger.propagate = False
        logger.setLevel(self.LOG_LEVEL)
        return logger
