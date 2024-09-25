import logging

def get_logger(filename):
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(filename, mode='w')
    handler.setFormatter(logging.Formatter(fmt='%(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger
