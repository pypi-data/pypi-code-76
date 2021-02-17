# -*- coding: utf-8 -*-

import pandas as pd
from enum import Enum
from datetime import datetime, timedelta


class RuleType(Enum):
    """ Pandas Resample 规则枚举 """

    Day_1 = '1D'

    Minute_5 = '5T'
    Minute_15 = '15T'
    Minute_30 = '30T'

    Hour_1 = '1H'
    Hour_2 = '2H'
    Hour_4 = '4H'


class TimeFrame(Enum):
    """ CCXT 请求用的 K 线时间规则"""

    Minute_1 = '1m'
    Minute_3 = '3m'
    Minute_5 = '5m'
    Minute_15 = '15m'
    Minute_30 = '30m'
    Hour_1 = '1h'
    Hour_2 = '2h'
    Hour_3 = '3h'
    Hour_4 = '4h'
    Hour_6 = '6h'
    Hour_8 = '8h'
    Hour_12 = '12h'
    Day_1 = '1d'
    Day_3 = '3d'
    Week_1 = '1w'
    Month_1 = '1M'

    @classmethod
    def all_values(cls):
        """ 所有枚举项的实际值数组 """
        return [e.value for e in cls]

    @property
    def rule_type(self):
        if self in [TimeFrame.Minute_1, TimeFrame.Minute_3, TimeFrame.Minute_5, TimeFrame.Minute_15, TimeFrame.Minute_30]:
            value = self.value.replace("m", "T")
        else:
            value = self.value.upper()
        return RuleType(value)

    def time_interval(self, res_unit='ms'):
        """转为时间戳长度

        Parameters
        ----------
        res_unit : str, optional
            时间戳单位, by default 'ms'
        """
        amount = int(self.value[0:-1])
        unit = self.value[-1]
        if 'y' in unit:
            scale = 60 * 60 * 24 * 365
        elif 'M' in unit:
            scale = 60 * 60 * 24 * 30
        elif 'w' in unit:
            scale = 60 * 60 * 24 * 7
        elif 'd' in unit:
            scale = 60 * 60 * 24
        elif 'h' in unit:
            scale = 60 * 60
        else:
            scale = 60
        ti = amount * scale
        if res_unit == 'ms':
            ti *= 1000
        return ti

    def timestamp_backward_offset(self, timestamp, count, unit='ms'):
        """`timestamp` 回推 `count` 个 time_interval 后的时间戳
        ts -= count * time_interval"""
        ts = timestamp - count * self.time_interval(unit)
        return ts

    def next_date_time_point(self, ahead_seconds=5, debug=False):
        """计算下一个实际时间点

        Parameters
        ----------
        ahead_time : int, optional
            误差秒数，误差内忽略当前周期, by default 1
        debug : bool, optional
            调试模式，打开时设定 10s 后为下个周期, by default False

        Raises
        ------
        ValueError
            目前只支持 'm' 结尾的 Time Interval
        """

        ti = pd.to_timedelta(self.value)
        now_time = datetime.now()
        # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 修改now_time，可用于测试
        this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
        min_step = timedelta(minutes=1)

        target_time = now_time.replace(second=0, microsecond=0)

        while True:
            target_time = target_time + min_step
            delta = target_time - this_midnight
            if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
                # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
                break

        return target_time


class CrawlerType(Enum):
    """K线抓取的类型"""

    BNC_FUTURE = "binance_future"
    BNC_DELIVERY = "binance_delivery"
    OK_CONTRACT = "ok_contract"

    @property
    def separator(self):
        if self == CrawlerType.BNC_DELIVERY:
            return '_'
        elif self == CrawlerType.OK_CONTRACT:
            return '-'
        else:
            return '/'

    @property
    def sample(self):
        if self == CrawlerType.BNC_DELIVERY:
            return 'BTCUSD_201225'
        elif self == CrawlerType.OK_CONTRACT:
            return 'BTC-USD-201225'
        else:
            return 'BTC/USDT'

    @property
    def exchange_name(self):
        if self in [CrawlerType.BNC_DELIVERY, CrawlerType.BNC_FUTURE]:
            return 'binance'
        elif self == CrawlerType.OK_CONTRACT:
            return 'okex'
        else:
            return ''
