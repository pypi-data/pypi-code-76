import time
from datetime import datetime

DATE_TIME_FORMAT = '%Y.%m.%d %H:%M:%S'

def format_timestamp(timestamp, formats=DATE_TIME_FORMAT, is_millisecond=True):
    if is_millisecond:
        timestamp = round(timestamp / 1000.0, 2)
    date_array = datetime.utcfromtimestamp(timestamp)
    return date_array.strftime(formats)

def get_utc_timestamp(is_millisecond=True):
    timestamp = time.time()
    return int(timestamp * 1000) if is_millisecond else timestamp