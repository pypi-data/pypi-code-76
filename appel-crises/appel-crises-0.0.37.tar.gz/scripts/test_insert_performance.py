import random
import string
import time
from tqdm import tqdm

from appel_crises.models import Signature

LETTERS = string.ascii_lowercase


def random_letters(n):
    return random.sample(LETTERS, n)


def generate_random_signature_data():
    first_name = random_letters(5)
    surname = random_letters(5)
    email = f"{random_letters(8)}@{random_letters(7)}.{random_letters(3)}"
    return email, first_name, surname


def insert_signatures(n):
    insert_times = []
    for _ in tqdm(range(n)):
        email, first_name, surname = generate_random_signature_data()
        Signature(email=email, first_name=first_name, surname=surname).save()
        insert_times.append(time.time())

    return insert_times
