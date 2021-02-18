import logging
import uuid
import datetime as dt
import numpy as np

from typing import List
from collections import deque, defaultdict

from metta.common import iter_utils, time_utils
from metta.common.topics import ProtobufMessage
from metta.proto.trace_pb2 import Trace, TraceTouch


class InokyoProfilerError(Exception):
    pass


def make_uid():
    return uuid.uuid4()


def init_trace() -> Trace:
    trace = Trace(id=str(make_uid()))
    return touch_trace(trace, "create")


def init_msg_trace(msg: ProtobufMessage) -> ProtobufMessage:
    try:
        msg.HasField("trace")
    except ValueError:
        raise InokyoProfilerError("message does not have a field 'trace' of type Trace")

    msg.trace.CopyFrom(init_trace())
    return msg


def touch_trace(trace: Trace, name: str) -> Trace:
    touch = TraceTouch(name=name, time=time_utils.time_ms())
    trace.touches.extend([touch])
    return trace


def touch_msg(msg: ProtobufMessage, name: str) -> ProtobufMessage:
    if not msg.HasField("trace"):
        logging.debug(
            "message tracing requires ProtobufMessage to set field 'trace' of type Trace",
        )
        return msg

    touch_trace(msg.trace, name)
    return msg


def pass_trace(src: ProtobufMessage, dest: ProtobufMessage) -> None:
    if not (src.HasField("trace")):
        logging.debug(
            "message tracing requires ProtobufMessage src to set field 'trace' of type Trace",
        )
        return
    dest.trace.CopyFrom(src.trace)


def copy_trace(trace: Trace, dest: ProtobufMessage) -> None:
    dest.trace.CopyFrom(trace)


def merge_traces(traces: List[Trace]) -> Trace:
    trace = Trace(id=str(make_uid()))
    touch = TraceTouch(
        name="merge-sources",
        time=min([touch.time for trace in traces for touch in trace.touches]),
    )
    trace.touches.extend([touch])
    return trace


def time_mapping(granularity):
    return {
        Timer.MINUTES: "min",
        Timer.SECONDS: "s",
        Timer.MILLISECONDS: "ms",
        Timer.MICROSECONDS: "μs",
        Timer.NANOSECONDS: "ns",
    }[granularity]


class Timer:
    MINUTES = int(60e9)
    SECONDS = int(1e9)
    MILLISECONDS = int(1e6)
    MICROSECONDS = int(1e3)
    NANOSECONDS = 1

    @staticmethod
    def print_nothing(time):
        pass

    @classmethod
    def on_iter(cls, iterable, **kwargs):
        timer = cls(**kwargs)
        timer.start()
        for v in iterable:
            timer.tick()
            yield v

    @staticmethod
    def print_from_format_string(format_string, granularity=None):
        if granularity is None:
            granularity = Timer.MILLISECONDS
        return lambda time: print(
            format_string.format(time, Timer.time_mapping(granularity))
        )

    @staticmethod
    def moving_average(print_func, size=10, frequency=1):
        window = deque()
        idx = 0

        def new_print_func(ms):
            nonlocal idx
            idx += 1
            window.append(ms)
            if len(window) >= size:
                window.popleft()
            if idx % frequency == 0:
                return print_func(np.mean(list(window)))

        return new_print_func

    @staticmethod
    def time_mapping(granularity):
        return {
            Timer.MINUTES: "min",
            Timer.SECONDS: "s",
            Timer.MILLISECONDS: "ms",
            Timer.MICROSECONDS: "μs",
            Timer.NANOSECONDS: "ns",
        }[granularity]

    def __init__(
        self, granularity=None, print_func=None, disable=False, if_in_profile=False
    ):
        self.granularity = (
            granularity if granularity is not None else Timer.MILLISECONDS
        )
        self.interval_string = self.time_mapping(self.granularity)
        self._start = None

        if if_in_profile:
            self.disable = _STACK_COUNT == 0
        else:
            self.disable = disable

        format_string = "time: {:.3f}{}"
        self.print_func = (
            print_func
            if print_func is not None
            else self.print_from_format_string(format_string, self.granularity)
        )

    def __enter__(self):
        self._start = time_utils.time_ms()
        return self

    def start(self):
        self.__enter__()

    def tick(self, print_func=None):
        now = time_utils.time_ms()
        interval = None
        if print_func is None:
            print_func = self.print_func
        if self._start is not None:
            interval = self._tock(print_func)
        self._start = now
        return interval

    def _tock(self, print_func, now=None):
        if now is None:
            now = time_utils.time_ms()
        interval = float(now - self._start) / self.granularity
        if not self.disable:
            print_func(interval)
        return interval

    def __exit__(self, type, value, traceback):
        self._tock(self.print_func)


class ProtoTimer:
    def __init__(
        self,
        print_freq: int = 1,
        granularity: float = Timer.MILLISECONDS,
        disable=False,
    ):

        self.print_freq = print_freq
        self.granularity = granularity
        self.interval_string = time_mapping(self.granularity)
        self._step = 0
        self.disable = disable

        self._traces = dict()
        self._paths = defaultdict(list)

    def __enter__(self):
        self._step = time_utils.time_ms()
        return self

    @staticmethod
    def path_from_trace(trace: Trace):
        return ":".join([touch.name for touch in trace.touches])

    @staticmethod
    def deltas_from_trace(trace: Trace):
        return list(
            map(
                lambda traces: traces[1].time - traces[0].time,
                iter_utils.pairwise(trace.touches),
            )
        )

    def mean_deltas(self, path: str):
        path_length = len(path.split(":"))
        traces = [self._traces[id_] for id_ in self._paths[path]]
        deltas_for_traces = [self.deltas_from_trace(trace) for trace in traces]
        return [
            np.mean([trace_deltas[t] for trace_deltas in deltas_for_traces])
            for t in range(path_length - 1)
        ]

    def clear_history(self):
        self._traces = dict()
        self._paths = defaultdict(list)

    def register(self, *msg: ProtobufMessage):
        if not self.disable:
            for touch in msg:
                if not touch.HasField("trace"):
                    raise InokyoProfilerError(
                        "message tracing requires ProtobufMessage to set field 'trace' of type Trace"
                    )

                self._traces[touch.trace.id] = touch.trace
                self._paths[self.path_from_trace(touch.trace)].append(touch.trace.id)

            # Print every print_freq messages
            step = self._step + len(msg)
            residual = step - self.print_freq
            if residual >= 0:
                self.print()
                self.clear_history()
                self._step = 0
            self._step += len(msg)

    def throughput(self):
        last_touches = [trace.touches[-1].time for trace in self._traces.values()]
        latest_receive = max(last_touches)
        earliest_receive = min(last_touches)
        return len(last_touches) / ((latest_receive - earliest_receive) / Timer.SECONDS)

    def latency(self):
        first_touches = [trace.touches[0].time for trace in self._traces.values()]
        earliest_first_touch = max(first_touches)
        return (time_utils.time_ms() - earliest_first_touch) / self.granularity

    def print(self):
        print(f"| DistinctPaths: {len(self._paths)}")
        print(f"|")

        time_unit = Timer.time_mapping(self.granularity)
        for path in self._paths.keys():
            print(f"| {path}")
            timings = self.mean_deltas(path)

            for timing, (src_name, dest_name) in zip(
                timings, iter_utils.pairwise(path.split(":"))
            ):
                disp_time = timing / self.granularity
                print(f"├ {src_name} -> {dest_name}: {disp_time:.3f}{time_unit}")
            print(f"├ Total: {sum(timings) / self.granularity:.3f}{time_unit}")
            print(f"├ Throughput: {self.throughput():.3f}fps")
            print(f"├ Latency: {self.latency():.3f}{time_unit}")


_STACK_COUNT = 0
_STACK_PRINTS = []


class StackTimer(Timer):
    @staticmethod
    def print_from_format_string(format_string, granularity=None):
        if granularity is None:
            granularity = Timer.MILLISECONDS
        return lambda time: (
            format_string.format(time, Timer.time_mapping(granularity))
        )

    def _tock(self, print_func, now=None):
        if now is None:
            now = time_utils.time_ms()
        if not self.disable:
            interval = float(now - self._start)
            res = print_func(interval / self.granularity)
            if res is not None:
                if _STACK_COUNT == 1:
                    print(res)

                    depths = [depth for _, depth, _ in _STACK_PRINTS]
                    depths = depths[1:]
                    depths.append(-1)

                    for (time, depth, string), next_depth in zip(_STACK_PRINTS, depths):

                        if next_depth > -1 and next_depth < depth:
                            point_char = "└"
                        else:
                            point_char = "├"

                        pre = "│ " * (depth - 2) + point_char + "─"
                        print(pre + string)

                        if depth == 2:
                            interval -= time

                    if len(_STACK_PRINTS) > 1:
                        print(
                            f"└─unaccounted: {interval / self.granularity:.3f}{StackTimer.time_mapping(self.granularity)}"
                        )

                    _STACK_PRINTS.clear()
                else:
                    self.old_prints.append((interval, _STACK_COUNT, res))
        return now

    def __enter__(self):
        if not self.disable:
            global _STACK_COUNT
            global _STACK_PRINTS
            _STACK_COUNT += 1
            self.old_prints = _STACK_PRINTS
            _STACK_PRINTS = []
        return super().__enter__()

    def __exit__(self, type, value, tb):
        global _STACK_COUNT
        global _STACK_PRINTS
        super().__exit__(type, value, tb)
        if not self.disable:
            self.old_prints += _STACK_PRINTS
            _STACK_PRINTS = self.old_prints
            _STACK_COUNT -= 1


if __name__ == "__main__":

    def test(n):
        if n == 0:
            return
        with StackTimer(print_func=lambda ms: f"test {n}: {ms:.4f}ms"):
            for i in range(n):
                test(n - 1)

    test(3)
