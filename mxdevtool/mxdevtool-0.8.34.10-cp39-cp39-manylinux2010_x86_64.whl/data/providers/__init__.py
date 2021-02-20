import mxdevtool as mx

from .sample import *
import mxdevtool.termstructures as ts


class MetaInfoMarketDataProvider(mx.MarketDataProvider):
    def __init__(self, meta=None):
        self.meta = meta
        self.data = None

    def with_meta(self, data: dict) -> dict:
        pass


def is_available_bloomberg() -> bool:
    import importlib
    blpapi = importlib.util.find_spec('blpapi')
    return blpapi is not None
    

def check_bloomberg():
    if is_available_bloomberg():
        from .bloomberg import request_sample
        request_sample()


# def calibrate_correlation_hist(*args):
#     for arr in args:

