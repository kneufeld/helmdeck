import sys
import logging

# logging.basicConfig(format='%(filename)s %(lineno)s %(message)s')

def create_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)

    h1 = logging.StreamHandler(sys.stderr)
    h1.setLevel(logging.INFO)
    h1.set_name("stderr")

    logger.addHandler(h1)

    return logger
