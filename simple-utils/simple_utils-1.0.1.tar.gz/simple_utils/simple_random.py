import uuid
import time
from . import simple_text

def get_uuid():
    return str(uuid.uuid1())


def make_uuid_including_time():
    return str(time.time_ns()) + "_" + simple_text.get_random_string(5)

