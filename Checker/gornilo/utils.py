from random import randint
from string import ascii_uppercase, digits
from datetime import datetime
from contextlib import contextmanager


def generate_flag():
    return "".join((ascii_uppercase + digits)[randint(0, len(ascii_uppercase)-1)] for _ in range(31)) + "="


@contextmanager
def measure(logger):
    start = datetime.now()
    try:
        yield None
    finally:
        logger.info(f"Action completed in {(datetime.now() - start).seconds} sec!")