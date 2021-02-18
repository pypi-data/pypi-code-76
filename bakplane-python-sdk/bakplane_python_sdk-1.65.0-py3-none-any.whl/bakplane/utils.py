import ctypes
import farmhash
import json
import typing
from datetime import datetime
from timeit import default_timer as timer

from google.protobuf.timestamp_pb2 import Timestamp

from bakplane.bakplane_pb2 import TimestampRange
from bakplane.extensions.base import ExecutionStatistics


def hash_string(s: str) -> int:
    return ctypes.c_long(farmhash.fingerprint64(s)).value


def to_timestamp(dt: datetime) -> int:
    ts = Timestamp()
    ts.FromDatetime(dt)

    return ts.seconds


def to_proto_timestamp(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)

    return ts


def to_proto_timestamp_range(s: datetime, e: datetime) -> TimestampRange:
    return TimestampRange(
        start_dt=to_proto_timestamp(s), end_dt=to_proto_timestamp(e)
    )


def to_execution_statistics(s: timer, e: timer) -> ExecutionStatistics:
    return ExecutionStatistics(e - s)


def parse_value_by_type(s: str, t: int) -> typing.Any:
    if t is None:
        return None

    if t == 0:
        return str(s)
    elif t == 1:
        return int(s)
    elif t == 2:
        return int(s)
    elif t == 3:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    elif t == 4:
        return s == "true" or s == "TRUE" or s == "1" or s == 1
    elif t == 5:
        return float(s)
    elif t == 6:
        return s
    elif t == 7:
        return datetime.strptime(s, "%Y-%m-%d")
    elif t == 8:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
    elif t == 9:
        return datetime.strptime(s, "%H:%M:%S.%f")
    elif t == 10:
        return json.loads(s)
