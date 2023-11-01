import os
import string
import random
from typing import Optional, List


NOUNS: Optional[List[str]] = None
ADJECTIVES: Optional[List[str]] = None


def _load_words() -> None:
    global NOUNS, ADJECTIVES

    dir = os.path.dirname(__file__)

    with open(os.path.join(dir, 'data', 'nouns.txt'), 'r') as file:
        NOUNS = file.read().strip().split(os.linesep)

    with open(os.path.join(dir, 'data', 'adjectives.txt'), 'r') as file:
        ADJECTIVES = file.read().strip().split(os.linesep)


def random_string(
    length: int = 32,
    alphabet: str = string.ascii_uppercase + string.ascii_lowercase + string.digits,
) -> str:
    return ''.join(random.choices(alphabet, k = length))


def random_username(random_length: int = 6) -> str:
    if NOUNS is None or ADJECTIVES is None:
        _load_words()

    random_alphabet = string.ascii_lowercase + string.digits

    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    suffix = ''.join(
        random.choices(random_alphabet, k = random_length),
    )

    return f'{adjective}_{noun}_{suffix}'


def random_password(length: int = 16) -> str:
    return random_string(length)


def random_xkcd_password(count: int = 6) -> str:
    if NOUNS is None:
        _load_words()

    return '_'.join(
        word.upper() for word in random.sample(NOUNS, k = count)
    )


def random_text(
    sentences_count: int = 4,
    words_in_sentence: int = 6,
) -> str:
    if NOUNS is None or ADJECTIVES is None:
        _load_words()

    sentences = []

    for _ in range(sentences_count):
        words = []

        for _ in range(words_in_sentence):
            word = random.choice(random.choice([NOUNS, ADJECTIVES]))
            words.append(word)

        sentence = ' '.join(words).capitalize() + '.'
        sentences.append(sentence)

    return ' '.join(sentences)
