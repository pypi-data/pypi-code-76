"""
@author  : MG
@Time    : 2021/1/26 11:18
@File    : export.py
@contact : mmmaaaggg@163.com
@desc    : 用于将办公室与家里的数据通过邮件方式进行同步
"""
from datetime import date
from io import StringIO
from typing import TextIO

import pandas as pd

from vnpy_extra.db.orm import database
from vnpy_extra.utils.send_email import build_email, send_email_qq


def export_table_2_df(table_name) -> str:
    file_path = f'{table_name}.csv'
    df = pd.read_sql(f'select * from {table_name}', database)
    df.to_csv(file_path, encoding='GBK', index=False)
    return file_path


def export_table_2_df_io(table_name) -> TextIO:
    df = pd.read_sql(f'select * from {table_name}', database)
    io = StringIO()
    df.to_csv(io, encoding='GBK', index=False)
    return io


def export_tables_and_send_email():
    table_name_list = ['strategy_info', 'symbols_info', 'strategy_status', 'strategy_backtest_stats']
    io_dic = {table_name: export_table_2_df_io(table_name) for table_name in table_name_list}

    subject = f'exports {date.today()}'
    from_mail = '265590706@qq.com'
    to_mail_list = ['mmmaaaggg@163.com']
    # file_path = f'd:\github\quant_vnpy\scripts\output\各策略持仓状态_2021-01-25.csv'
    msg = build_email(from_mail, to_mail_list, subject, io_dic)

    password = '***'
    send_email_qq(from_mail, to_mail_list, password, msg)


if __name__ == "__main__":
    export_tables_and_send_email()
