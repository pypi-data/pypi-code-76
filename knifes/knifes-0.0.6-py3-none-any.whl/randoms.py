import random
import string


def random_str(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

