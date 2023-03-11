import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter

def get_logger(name: str, logfile='example.log'):
    logger = getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler_format = Formatter('[%(levelname)s]\t%(asctime)s : %(message)s')

    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(handler_format)

    file_handler = FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(handler_format)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
