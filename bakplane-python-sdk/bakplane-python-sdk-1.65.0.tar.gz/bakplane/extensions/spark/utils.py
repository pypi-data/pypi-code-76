from bakplane.extensions.base import WriteMode
from datetime import datetime, timedelta


def to_spark_save_mode(mode: WriteMode) -> str:
    if mode == WriteMode.APPEND:
        return "append"

    if mode == WriteMode.ERROR_IF_EXISTS:
        return "errorifexists"

    if mode == WriteMode.IGNORE:
        return "ignore"

    return "overwrite"


def timestamp_to_datetime(timestamp: int):
    if timestamp < 0:
        return datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    else:
        return datetime.utcfromtimestamp(timestamp)


def timestamp_to_date_string(timestamp: int, f="%Y-%m-%d"):
    dt = timestamp_to_datetime(timestamp)
    return dt.strftime(f)


def datetime_to_date_string(dt: datetime, f="%Y-%m-%d"):
    return dt.strftime(f)
