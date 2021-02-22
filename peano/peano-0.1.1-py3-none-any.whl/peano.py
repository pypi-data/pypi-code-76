import time, logging, signal, asyncio
from typing import Any, List, Callable, TypeVar, cast
from functools import wraps
from datetime import datetime as dt

from influxdb_client import InfluxDBClient, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

F = TypeVar("F", bound=Callable[..., Any]) 

def init(url: str,
         organ: str,
         token: str,
         bucket: str,
         *,
         loop: asyncio.AbstractEventLoop = None,
         delay_s: int = 60,
         latency_accuracy: int = 6,
         batch_size: int = 100,
         max_batch_s: int = 3600) -> None:
    """ Initialize before any measured function called
    url              : InfluxDb server API url
    organ            : InfluxDb organization
    token            : InfluxDb auth token
    bucket           : InfluxDb destination bucket
    delay_s          : seconds between consecutive reports
    latency_accuracy : number of digits after point for latency
    batch_size       : minimum number of records in batch to send
    sparse           : send record when measured, not every period
    max_batch_s      : maximum duration of batch in seconds
    """
    now = time.time()

    global _influx, _bucket, _delays, _format, _log, _period, _sparse
    _log    = logging.getLogger('⏱️')
    _log.info(f'Report measured calls every {delay_s} seconds')
    _client  = InfluxDBClient(url=url, org=organ, token=token)
    _influx = _client.write_api(write_options=SYNCHRONOUS)
    _bucket = bucket
    _delays = delay_s
    _format = f'.{latency_accuracy}f'

    global _batch, _batchs, _batch_end, _out
    _batch  = batch_size
    _batchs = max_batch_s
    _period = int(now / _delays)
    _batch_end = now + _batchs
    _out    = []

    # write pending output on shutdown
    if loop is None:
        loop = asyncio.get_event_loop()

    def wrap_handler(handler):
        def shutdown():
            if len(_out) > 0:
                _influx.write(bucket=_bucket, record=_out, write_precision=WritePrecision.S)
                _out.clear()
            handler()
        return shutdown

    for sig in (signal.SIGINT, signal.SIGTERM):
        handler = signal.getsignal(sig)
        loop.add_signal_handler(sig, wrap_handler(handler))


_bucket     : str
_delays     : int
_format     : str
_batch      : int
_batchs     : int
_batch_end  : float
_influx     : Any
_log        : logging.Logger
_out        : List[str]
_decors     : List[Any] = []
_period     : int

class measured:
    """ Measure async function calls
    """
    count : int = 0     # number of calls
    spent : float = 0   # seconds spent in call
    period: int = 0     # for sparse measurements


    def __init__(self, label:str=None, *, sparse:bool=True) -> None:
        """ Decorator generator
        """
        self._label = label
        self._sparse = sparse
        if not sparse:
            global _decors
            _decors.append(self)


    def __call__(self, fn: F) -> F:
        """ Decorating method, returns wrapped function
        """
        # use function name as label by default
        if self._label is None:
            self._label = fn.__name__

        # select reporting strategy
        report = self._report_sparse if self._sparse else self._report_dense

        # declare wrapper function
        @wraps(fn)
        async def wrapper(*args, **kwds):
            start = time.time()
            result = await fn(*args, **kwds)
            finish = time.time()
            report(start, finish)
            return result

        return cast(F, wrapper)


    def _report_sparse(self, start:float, finish:float) -> None:
        """ Record measured call
        """
        period = int(finish / _delays)

        #         D   C       B   A 
        # ------c-|---|---|---|-c-|------->
        #         p   0       0   p

        if period > self.period:
            global _out
            if self.count > 0:
                # write D
                ts = self.period * _delays
                _out.append(self._linear(ts))

                if period > self.period + 1:
                    # write C
                    ts = (self.period + 1) * _delays
                    _out.append(self._empty(ts))
        
            if period > self.period + 2:
                # write B
                ts = (period - 1) * _delays
                _out.append(self._empty(ts))

            self.period = period
            _send(finish)

        # save this call
        self.count += 1
        self.spent += finish - start
        #_log.info(f'report {self._label} {format(finish - start, _format)} at {dt.fromtimestamp(period * _delays):%H:%M}')


    def _report_dense(self, start:float, finish:float) -> None:
        """ Record measured call
        Fill gaps in periods when wrapped function was not called
        """
        period = int(finish / _delays)

        global _period
        if period > _period:
            global _out
            while period > _period:
                #_log.info(f'work on {len(_decors)=}, {_period=}')
                sec = _period * _delays
                for d in _decors:
                    _out.append(d._empty(sec) if d.count==0 else d._linear(sec))
                _period += 1

            _send(finish)

        # save this call
        self.count += 1
        self.spent += finish - start
        #_log.info(f'report {self._label} {format(finish - start, _format)} at {dt.fromtimestamp(period * _delays):%H:%M}')


    def _empty(self, ts:int) -> str:
        return f'{self._label} tps=0,latency=0 {ts}'


    def _linear(self, ts:int) -> str:
        tps = self.count / _delays
        latency = self.spent / self.count
        self.count = 0
        self.spent = 0
        return f'{self._label} tps={tps:.3f},latency={format(latency, _format)} {ts}'


def _send(now:float) -> None:
    """ Optionally send records to influx
    """
    global _out, _batch_end

    if len(_out) >= _batch or now >= _batch_end:
        _log.info(f'send batch size {len(_out)}')
        
        # send records to influx 
        _influx.write(bucket=_bucket, record=_out, write_precision=WritePrecision.S)
        _out.clear()

        # calculate when batch will end next time
        _batch_end = now + _batchs 
