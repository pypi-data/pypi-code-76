import pytz
import pandas as pd
import dateutil.parser
from enum import IntEnum
from datetime import datetime
from ..defines.column_names import *
from ..defines.enums import RuleType


class DateFormatter:
    """日期格式处理"""

    @staticmethod
    def convert_local_date_to_timestamp(date):
        """Date -> Timestamp(ms)"""
        return int(date.timestamp()) * 1000

    @staticmethod
    def convert_timestamp_to_local_date(timestamp, tz=None):
        """Timestamp(ms) -> Date, tz=None 默认走本地时区"""
        date = datetime.fromtimestamp(timestamp / 1000, tz=tz).astimezone(tz)
        return date

    @staticmethod
    def convert_local_date_to_string(date, format="%Y-%m-%d %H:%M:%S"):
        """Date -> String"""
        return date.strftime(format)

    @staticmethod
    def convert_string_to_local_date(date_string, format="%Y-%m-%d %H:%M:%S", replace_tz=None):
        """String -> Date"""
        return datetime.strptime(date_string, format).replace(tzinfo=replace_tz)

    @staticmethod
    def convert_timestamp_to_string(timestamp, format="%Y-%m-%d %H:%M:%S"):
        """Timestamp(ms) -> Date -> String"""
        return DateFormatter.convert_local_date_to_string(DateFormatter.convert_timestamp_to_local_date(timestamp), format)

    @staticmethod
    def convert_string_to_timestamp(date_string, format="%Y-%m-%d %H:%M:%S", replace_tz=None):
        """String -> Date -> Timestamp(ms)"""
        return DateFormatter.convert_local_date_to_timestamp(DateFormatter.convert_string_to_local_date(date_string, format, replace_tz))

    @staticmethod
    def convert_date_to_iso8601(date):
        """Date -> ISO8601"""
        return date.isoformat()

    @staticmethod
    def now_without_seconds():
        """当前时间，忽略秒"""
        date = datetime.now()
        date = date.replace(second=0, microsecond=0)
        return date

    @staticmethod
    def now_date_string(format="%Y-%m-%d %H:%M:%S"):
        """当前时间字符串"""
        return DateFormatter.convert_local_date_to_string(datetime.now(), format)


class CandleDateFromType(IntEnum):
    Timestamps = 0
    ISO8601 = 1


class CandleFormatter:
    """K 线格式处理"""

    @staticmethod
    def convert_raw_data_to_data_frame(data,
                                       date_name=COL_CANDLE_BEGIN_TIME,
                                       from_type=CandleDateFromType.Timestamps,
                                       extra_columns_mapping={}):
        """
        Raw Data:
        [[1503386100000, 300.23, 300.24, 294.38, 297.76, 125.53231],
         ...]

        DataFrame:
            candle_begin_time    open    high     low   close     volume
        0   2017-08-17 12: 00: 00  301.13  301.13  298.00 298.00   5.80167
        ...
        """
        df = pd.DataFrame(data, dtype=float)
        if df.shape[0] > 0:
            column_mapping = {0: 'MTS', 1: COL_OPEN, 2: COL_HIGH, 3: COL_LOW, 4: COL_CLOSE, 5: COL_VOLUME}
            column_mapping.update(extra_columns_mapping)
            df.rename(columns=column_mapping,
                      inplace=True)
            if from_type == CandleDateFromType.ISO8601:
                df[date_name] = df['MTS'].apply(lambda x: dateutil.parser.parse(x).replace(tzinfo=pytz.utc))
            else:
                df[date_name] = pd.to_datetime(df['MTS'], unit='ms', utc=pytz.utc)
            columns = [date_name, COL_OPEN, COL_HIGH, COL_LOW, COL_CLOSE, COL_VOLUME]
            for extra_key in sorted(extra_columns_mapping.keys()):
                columns.append(extra_columns_mapping[extra_key])
            df = df[columns]
        return df

    @ staticmethod
    def convert_json_timestamp_to_date(json_list, column_name=COL_CANDLE_BEGIN_TIME, tz=None):
        """Convert timestamp to Date"""
        for doc in json_list:
            if not isinstance(column_name, list):
                doc[column_name] = DateFormatter.convert_timestamp_to_local_date(doc[column_name], tz)
            else:
                for c in column_name:
                    doc[c] = DateFormatter.convert_timestamp_to_local_date(doc[c], tz)
        return json_list

    @ staticmethod
    def resample(df, rule_type=RuleType.Minute_15):
        """
        Resample date
        : param df:
        : param rule_type:
        : return:
        """

        # =====转换为其他分钟数据
        agg_dict = {
            COL_OPEN: 'first',
            COL_HIGH: 'max',
            COL_LOW: 'min',
            COL_CLOSE: 'last',
            COL_VOLUME: 'sum',
        }
        columns = list(df.columns)
        if 'quote_volume' in columns:
            agg_dict['quote_volume'] = 'sum'
        if 'trade_num' in columns:
            agg_dict['trade_num'] = 'sum'
        if 'taker_buy_base_asset_volume' in columns:
            agg_dict['taker_buy_base_asset_volume'] = 'sum'
        if 'taker_buy_quote_asset_volume' in columns:
            agg_dict['taker_buy_quote_asset_volume'] = 'sum'
        period_df = df.resample(rule=rule_type.value, on=COL_CANDLE_BEGIN_TIME, label='left', closed='left').agg(agg_dict)
        period_df.dropna(subset=[COL_OPEN], inplace=True)  # 去除一天都没有交易的周期
        period_df = period_df[period_df[COL_VOLUME] > 0]  # 去除成交量为0的交易周期
        period_df.reset_index(inplace=True)
        df = period_df[columns]

        return df
