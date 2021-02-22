import string
import uuid
import random
from os.path import splitext
from typing import List, Iterable
from uuid import UUID

DOMAINS = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "yahoo.com"]


def file_ext(f: str) -> str:
    """Get the file extension of a file."""
    return splitext(f)[1]


def file_name(f: str) -> str:
    """Get the filename of a file without the extension."""
    return splitext(f)[0]


def get_random_items(items: Iterable, count: int) -> list:
    iterator = iter(items)
    try:
        items = [iterator.next() for _ in range(count)]
    except StopIteration:
        raise ValueError("Sample larger than population.")
    random.shuffle(items)
    for i, v in enumerate(iterator, count):
        r = random.randint(0, i)
        if r < count:
            items[r] = v
    return items


def get_random_domain(domains: List[str]) -> str:
    return random.choice(domains)


def get_random_name(length: int) -> str:
    letters = string.ascii_lowercase[:12]
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email(length: int = 10) -> str:
    return f'{get_random_name(length)}@{get_random_domain(DOMAINS)}'


def generate_random_uuids(count: int = 10) -> List[UUID]:
    return [uuid.uuid4() for _ in range(count)]


def generate_random_numbers():
    return [random.randint(1, 100) for _ in range(0, 5)]
