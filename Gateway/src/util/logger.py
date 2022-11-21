from src.constants.const import System
import logging
import os


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Log Everything

    # create file if it doesn't exist
    os.makedirs(os.path.dirname(System.LOGGING_PATH_ERROR), exist_ok=True)

    # create file handler which logs error messages
    fh = logging.FileHandler(System.LOGGING_PATH_ERROR)
    fh.setLevel(logging.ERROR)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(System.STDOUT_LOG_LEVEL)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
