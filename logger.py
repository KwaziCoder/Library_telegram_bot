import logging
from logging.handlers import RotatingFileHandler

MAX_LOG_FILE_CAPACITY = 52428800
MAX_LOG_BACKUPS = 1

def set_logger() -> None:
    handler = RotatingFileHandler(f"work.log", mode='a', maxBytes=MAX_LOG_FILE_CAPACITY, backupCount=MAX_LOG_BACKUPS)

    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')

    handler.setFormatter(formatter)

    logging.basicConfig(handlers=[handler], level=logging.INFO)
