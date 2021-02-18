# supp_create.py
# Dependencies: pandas

import pandas as pd
import numpy as np
from motocustomsolutions.motocustomsolutionspkg.errors import DataError


def create_supplement(df, dealership_col, vin_col, stock_col, trim_col, jato_col='',
                      chrmstyle_col='', discount_col='', misc1_col='', misc2_col=''):

    if str(type(df)) != '<class \'pandas.core.frame.DataFrame\'>':
        raise TypeError('Must pass a DataFrame Object.')

    # List of supplement columns
    supp_columns = ["Dealership", "VIN", "Stock", "Jato ID", "ChrmStyleID", "Trim", "Discount", "Misc 1", "Misc 2"]

    # List of column variables
    fill_data = ['dealership_col', 'vin_col', 'stock_col', 'trim_col', 'jato_col',
        'chrmstyle_col', 'discount_col', 'misc1_col', 'misc2_col']

    # Mapping column variables to column names
    match_dict = {
    'dealership_col': 'Dealership',
    'vin_col': 'VIN',
    'stock_col': 'Stock',
    'trim_col': 'Trim',
    'jato_col': 'Jato ID',
    'chrmstyle_col': 'ChrmStyleID',
    'discount_col': 'Discount',
    'misc1_col': 'Misc 1',
    'misc2_col': 'Misc 2'
    }

    # Create list of passed variables, empty variables, and mapping those variables to header names
    header_list = []
    missing_header_list = []
    header_map = []

    # Iterate through local variables to determine which variables are passed and which are empty strings
    for arg in locals().items():
        if arg[0] in fill_data:
            if arg[1] != '':
                header_list.append(arg[1])
                header_map.append(arg)
            else:
                missing_header_list.append(arg[0])

    # Create new dataframe using only GIVEN parameterslem
    try:
        supp_df = df[header_list].copy()
    except KeyError:
        raise KeyError('Passed columns names do not match columns in passed DataFrame')

    # Rename columns using mapping list and respective dict entries
    for i in range(supp_df.shape[1]):
        supp_df = supp_df.rename(columns={header_map[i][1]:match_dict.get(header_map[i][0])})

    # Add columns to data frame from list of empty headers
    i = 0
    for entry in missing_header_list:
        supp_df[match_dict.get(entry)] = ''
        i+=1

    # Change order of columns to match supplement file
    supp_df = supp_df[supp_columns]

    return supp_df
