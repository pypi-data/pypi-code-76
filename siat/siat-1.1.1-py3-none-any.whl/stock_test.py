# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.stock import *

pricedf=get_price('^HSI',"1991-1-1","2021-2-28")


df=security_price('AAPL','2021-1-1','2021-1-31',datatag=True,power=4)

info=get_stock_profile("AAPL")
info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("AAPL",info_type='officers')
info=stock_info('AAPL')
sub_info=stock_officers(info)

div=stock_dividend('600519.SS','2011-1-1','2020-12-31')
split=stock_split('600519.SS','2000-1-1','2020-12-31')

ticker='AAPL'
info=stock_info(ticker)
info=get_stock_profile("AAPL",info_type='officers')

info=get_stock_profile("AAPL")

info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("GS",info_type='officers')

info=stock_info('JD')
sub_info=stock_officers(info)
info=get_stock_profile("JD",info_type='officers')

info=stock_info('BABA')
sub_info=stock_officers(info)
info=get_stock_profile("BABA",info_type='officers')

info=stock_info('0700.HK')
sub_info=stock_officers(info)
info=get_stock_profile("0700.HK",info_type='officers')

info=stock_info('600519.SS')
sub_info=stock_officers(info)
info=get_stock_profile("600519.SS",info_type='officers')

info=get_stock_profile("0939.HK",info_type='risk_esg')


market={'Market':('China','^HSI')}
stocks={'0700.HK':3,'9618.HK':2,'9988.HK':1}
portfolio=dict(market,**stocks)
esg=portfolio_esg2(portfolio)



