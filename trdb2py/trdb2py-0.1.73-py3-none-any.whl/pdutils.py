# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from trdb2py.utils import str2asset, asset2str
from datetime import datetime
import time
import pandas as pd


def buildPNLReport(lstpnl: list) -> pd.DataFrame:
    """
    buildPNLReport - 将PNL列表转换为pandas.DataFrame，方便计算
    """
    fv0 = {
        'title': [],
        'asset': [],
        'maxDrawdown': [],
        'maxDrawdownStart': [],
        'maxDrawdownEnd': [],
        'maxDrawup': [],
        'maxDrawupStart': [],
        'maxDrawupEnd': [],
        'sharpe': [],
        'annualizedReturns': [],
        'annualizedVolatility': [],
        'totalReturns': [],
        'variance': [],
        'buyTimes': [],
        'sellTimes': [],
        'stoplossTimes': [],
        'maxUpDay': [],
        'maxPerUpDay': [],
        'maxDownDay': [],
        'maxPerDownDay': [],
        'maxUpWeek': [],
        'maxPerUpWeek': [],
        'maxDownWeek': [],
        'maxPerDownWeek': [],
        'maxUpMonth': [],
        'maxPerUpMonth': [],
        'maxDownMonth': [],
        'maxPerDownMonth': [],
        'maxUpYear': [],
        'maxPerUpYear': [],
        'maxDownYear': [],
        'maxPerDownYear': [],
        'perWinRate': [],
        'values': [],
    }

    for v in lstpnl:
        fv0['title'].append(v['title'])

        fv0['asset'].append(asset2str(v['pnl'].asset))

        fv0['maxDrawdown'].append(v['pnl'].maxDrawdown)
        fv0['maxDrawdownStart'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawdownStartTs).strftime('%Y-%m-%d'))
        fv0['maxDrawdownEnd'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawdownEndTs).strftime('%Y-%m-%d'))

        fv0['maxDrawup'].append(v['pnl'].maxDrawup)
        fv0['maxDrawupStart'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawupStartTs).strftime('%Y-%m-%d'))
        fv0['maxDrawupEnd'].append(datetime.fromtimestamp(
            v['pnl'].maxDrawupEndTs).strftime('%Y-%m-%d'))

        fv0['sharpe'].append(v['pnl'].sharpe)
        fv0['annualizedReturns'].append(v['pnl'].annualizedReturns)
        fv0['annualizedVolatility'].append(v['pnl'].annualizedVolatility)
        fv0['totalReturns'].append(v['pnl'].totalReturns)
        fv0['variance'].append(v['pnl'].variance)

        fv0['buyTimes'].append(v['pnl'].buyTimes)
        fv0['sellTimes'].append(v['pnl'].sellTimes)
        fv0['stoplossTimes'].append(v['pnl'].stoplossTimes)

        fv0['maxUpDay'].append(datetime.fromtimestamp(
            v['pnl'].maxUpDayTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpDay'].append(v['pnl'].maxPerUpDay)
        fv0['maxDownDay'].append(datetime.fromtimestamp(
            v['pnl'].maxDownDayTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownDay'].append(v['pnl'].maxPerDownDay)

        fv0['maxUpWeek'].append(datetime.fromtimestamp(
            v['pnl'].maxUpWeekTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpWeek'].append(v['pnl'].maxPerUpWeek)
        fv0['maxDownWeek'].append(datetime.fromtimestamp(
            v['pnl'].maxDownWeekTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownWeek'].append(v['pnl'].maxPerDownWeek)

        fv0['maxUpMonth'].append(datetime.fromtimestamp(
            v['pnl'].maxUpMonthTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpMonth'].append(v['pnl'].maxPerUpMonth)
        fv0['maxDownMonth'].append(datetime.fromtimestamp(
            v['pnl'].maxDownMonthTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownMonth'].append(v['pnl'].maxPerDownMonth)

        fv0['maxUpYear'].append(datetime.fromtimestamp(
            v['pnl'].maxUpYearTs).strftime('%Y-%m-%d'))
        fv0['maxPerUpYear'].append(v['pnl'].maxPerUpYear)
        fv0['maxDownYear'].append(datetime.fromtimestamp(
            v['pnl'].maxDownYearTs).strftime('%Y-%m-%d'))
        fv0['maxPerDownYear'].append(v['pnl'].maxPerDownYear)

        fv0['values'].append(len(v['pnl'].values))

        if v['pnl'].sellTimes + v['pnl'].stoplossTimes == 0:
            fv0['perWinRate'].append(0)
        else:
            fv0['perWinRate'].append(
                v['pnl'].winTimes * 1.0 / (v['pnl'].sellTimes + v['pnl'].stoplossTimes))

    return pd.DataFrame(fv0)
