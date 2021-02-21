from datetime import date, datetime
from typing import Optional

epoch = datetime.utcfromtimestamp(0)


def date_to_datetime(date_: date, hour: Optional[int] = 0, minute: Optional[int] = 0,
                     second: Optional[int] = 0) -> datetime:
    return datetime(date_.year, date_.month, date_.day, hour, minute, second)


def date_to_unixtimestamp(date_: date):
    return int((date_to_datetime(date_) - epoch).total_seconds() * 1000.0)


def datetime_to_unixtimestamp(datetime_: datetime):
    return int((datetime_ - epoch).total_seconds() * 1000.0)
