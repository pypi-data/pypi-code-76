from datetime import datetime
from pytz import timezone


def get_kst():
    return datetime.now(timezone('Asia/Seoul'))

def get_kst_ymd():
    return get_kst().strftime('%Y-%m-%d')

