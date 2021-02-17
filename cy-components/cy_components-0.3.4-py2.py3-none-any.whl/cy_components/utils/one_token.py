import requests
import random
from .coin_pair import CoinPair
from ..defines.enums import TimeFrame
from ..defines.column_names import COL_CANDLE_BEGIN_TIME


class OneToken:

    def __init__(self, exchange_name, cfgs=[]):
        """根据配置初始化

        Parameters
        ----------
        cfgs : list, optional
            [{
                'key': 'abc',
                'secret': '123',
            },{...}], by default []
        """
        self.configs = cfgs
        self.exchange_name = exchange_name

    @property
    def inner_exchange_name(self):
        """映射到内部请求用的exchange_name"""
        return {
            "Binance": "binance",
            "HuobiPro": "huobip",
        }[self.exchange_name]

    def fetch_candle_data(self, coin_pair: CoinPair, timeframe: TimeFrame, limit=200, since=0):
        """Fetching"""
        headers = {'ot-key': random.choice(self.configs)['key']}
        contract = '{}/{}'.format(self.inner_exchange_name, coin_pair.formatted(sep='.').lower())
        base_url = 'https://hist-quote.1tokentrade.cn/candles'
        since /= 1000  # seconds
        until = since + limit * timeframe.time_interval(res_unit='s')
        k_line_url = f'{base_url}?since={since}&until={until}&contract={contract}&duration={timeframe.value}&format=json'

        candle_res = requests.get(k_line_url, headers=headers)
        candle_res.raise_for_status()

        print(candle_res.headers)
        data = candle_res.json()

        def rename_key(x):
            """back to milliseconds"""
            x[COL_CANDLE_BEGIN_TIME] = x.pop('timestamp') * 1000
            return x

        replaced_list = [rename_key(x) for x in data]
        return replaced_list
