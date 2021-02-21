from qttp.tools.date_interval import DateInterval
from qttp.tools.date import HunDate
from qttp.tools.time_span import time_span
from qttp.tools.log import setup_custom_logger

from datetime import datetime, timedelta
import pandas as pd
import requests
import time
import os

pd.set_option('mode.chained_assignment',  None) # turn off the warning

logger = setup_custom_logger("Candles")

hun_date = HunDate()

class Candles:
    def candles_since(self, since, span='24h', base='9h'):
        self.today = hun_date.today_plus_1day()
        count_limit = self.__count_limit()

        dates = DateInterval(since, self.today, count_limit)[0]
        start_dates = dates[0]
        end_dates = dates[1]

        save_file_name = self.__save_file_name(self.exchange, since,
                                               span, base)
        # print(save_file_name)
        #
        # try:
        #     result_df = pd.read_csv(save_file_name, index_col=0,
        #                             parse_dates=True)
        #
        # except FileNotFoundError:
        #     new_df = pd.DataFrame()
        #     for to_date in to_dates:
        #         pass


    def real_time_candles_1h(self, since=None):
        url, path, params = self.__url_path_params("60m", since)
        page_json = requests.get(url + path, params=params).json()
        df = self.__dataframe_convert(page_json)
        df = self.preprocessing(df)
        return df

    def real_time_candles_24h(self):
        url, path, params = self.__url_path_params("1D")
        page_json = requests.get(url + path, params=params).json()
        df = self.__dataframe_convert(page_json)
        df = self.preprocessing(df)
        return df

    def __count_limit(self):
        if self.exchange == "upbit":
            return 200

    def __dataframe_convert(self, page_json):
        if self.exchange == "upbit":
            return pd.DataFrame(page_json)

    def __url_path_params(self, unit, since=None):
        if self.exchange == "upbit":
            url = "https://api.upbit.com"

            if unit == "60m":
                unit = "60"

            if unit == "1D":
                path = "/v1/candles/days"
            else:
                path = "/v1/candles/minutes/" + unit
            params = {
                "market" : self.market,
                "count" : 200,
            }

            if since:
                params['to'] = since

        if self.exchange == "deribit":
             url = "https://www.deribit.com"
             path = "/api/v2/public/get_tradingview_chart_data"
             params = {

             }

        if self.exchange == "bybit":
             url = "https://api.bybit.com"
             path = "/v2/public/kline/list"
             params = {
                 "symbol" : self.market,
                 "interval" : unit,
                 "from" : since
             }

        return url, path, params

    def __time_converter(self):
        pass

    def __save_file_name(self, exchange, since, span, base):
        exchange = exchange
        market   = self.market
        start    = since
        end      = self.today
        span     = span
        base     = base
        path = 'candles/'

        if not os.path.isdir(path):
            os.mkdir(path)

        file_name = f'{exchange}_{market}_{start}_{end}_{span}_{base}.csv'
        return path + file_name

class UpbitCandle(Candles):
    def __init__(self, market):
        self.exchange = "upbit"
        self.market = market
        self.preprocessing = self.__preprocessing

    def candle_since(self, since):
        super().candle_since(since)
        print(save_file_name)

    def __preprocessing(self, df):
        columns = [
            'candle_date_time_kst',
            'opening_price',
            'high_price',
            'low_price',
            'trade_price',
            'candle_acc_trade_volume'
        ]
        df['candle_acc_trade_volume'] = round(df['candle_acc_trade_volume'], 0)
        df = df[columns]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume' ]
        df = df.sort_values(by='date')
        df.index = df['date']
        df.drop('date', axis=1, inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        return df
