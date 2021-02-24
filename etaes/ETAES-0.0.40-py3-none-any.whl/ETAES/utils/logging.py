#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :logging.py
# @Time     :2021/2/2
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

# import logging
#
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(format = LOG_FORMAT, filename = "my.log")
#
#
#
# def log(text):
#     def decorator(func):
#         def wrapper(*arg, **kw):
#             logging.error(text)
#             return func(*arg, **kw)
#         return wrapper
#     return decorator
#
# @log('test')
# def m():
#     print('done')
#
# m()