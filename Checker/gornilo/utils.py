from random import randint
from string import ascii_uppercase, digits
from datetime import datetime
from contextlib import contextmanager


def generate_flag():
    flag_symbols = ascii_uppercase + digits
    return "".join((flag_symbols[randint(0, len(flag_symbols)-1)] for _ in range(31))) + "="


@contextmanager
def measure(action_name: str) -> None:
    start = datetime.now()
    prefix = f"[{action_name}] " if action_name else None
    print(prefix + f"Measure started at {start}.")
    try:
        yield None
    finally:
        print(prefix + f"Action completed in {(datetime.now() - start).seconds} sec!")