"""
~ helpers_columns.py

Collection of functions to use over Column.
"""
import re 
import pyspark.sql.functions as F

def without_tirets(col):
    return F.trim(F.regexp_replace(col, '-', ' '))

def single_space(col):
    return F.trim(F.regexp_replace(col, r"\s{2,}", " "))

def without_parentheses(col):
    return F.trim(F.regexp_replace(col, r"\(|\)", ''))

def without_parentheses_content(col):
    return F.trim(F.regexp_replace(col, r"\s\(.*\)", ''))