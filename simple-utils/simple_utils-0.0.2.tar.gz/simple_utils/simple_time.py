from datetime import datetime
from pytz import timezone


class SimpleTime():

    @staticmethod
    def get_kst():
        return datetime.now(timezone('Asia/Seoul'))
