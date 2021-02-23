# coding: utf-8

import datetime as dt
import os as os

class Constants:
    PATH = os.path.abspath (os.path.join (os.path.dirname (__file__), '..'))
    DATA_PATH = PATH + '\\data\\'
    CODE_DATE = '%d/%m/%Y'
    TODAY = dt.datetime.today ().strftime (CODE_DATE)
    BASIS = 360
    ONE_DAY = 1 / 252
    ONE_WEEK = 5 / 252
    ONE_BASIS_POINT = 0.0001 
    ONE_PERCENT = 0.01
    MINIMUM_MATURITY = 1 / 12

