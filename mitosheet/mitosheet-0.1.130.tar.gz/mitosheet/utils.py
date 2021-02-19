#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions
"""
import json
import pandas as pd
import numpy as np
import numbers
from string import ascii_letters, digits
import subprocess
import os

ALLOWED_CHARS = ascii_letters + digits + '_'


def make_valid_header(column_header):
    """
    Takes a header, and performs replaces against common characters
    to make the column_header valid!
    """
    # If it's just numbers, turn it into a string (with an underscore)
    if isinstance(column_header, numbers.Number):
        return str(column_header).replace('.', '_') + '_'

    # If it's just numbers in a string, add an underscore
    if column_header.isdigit():
        return column_header + "_"

    # Replace common invalid seperators with valid seperators
    replace_dict = {
        ' ': '_',
        '-': '_',
        '(': '_',
        ')': '_',
        '/': '_',
        '#': 'num',
        ',': '_',
        '.': '_',
        '!': '_',
        '?': '_'
    }
    for find, replace in replace_dict.items():
        column_header = column_header.replace(find, replace)
    
    if not is_valid_header(column_header):
        # If our reasonable replacements don't work, we just ban any character not from a set
        new_header = ''.join([
            c for c in column_header if c in ALLOWED_CHARS
        ])
        if not is_valid_header(new_header):
            # And then append an underscore, for good measure, and this should fix it!
            new_header = new_header + '_'

        return new_header
    return column_header

def is_valid_header(column_header):
    """
    A header is valid if:
    0. It has a non-zero length
    1. It is a string
    2. It only contains alphanumic characters (including the russian alphabet), or _
    3. It has at least one non-numeric character.

    Valid examples: A, ABC, 012B, 213_bac, 123_123
    Invalid examples: 123, 123!!!, ABC!, 123-123

    This is a result of not being able to distingush column headers from constants
    otherwise, and would not be necessary if we had a column identifier!
    """

    # Condition (0)
    if isinstance(column_header, str) and len(column_header) == 0:
        return False

    valid_chars = set(ascii_letters) \
        .union(set(digits)) \
        .union(set(['_'])) \
        .union(set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'))
        # NOTE: we have russian users, hence we support the russian alphabet! 
        # List taken from https://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic/17587364

    return isinstance(column_header, str) and ( # Condition (1)
        set(column_header).issubset(valid_chars) and # Condition (2)
        not column_header.isdigit() # Condition (3)
    )


def get_invalid_headers(df: pd.DataFrame):
    """
    Given a dataframe, returns a list of all the invalid headers this list has. 
    """
    return [
        header for header in df.columns.tolist()
        if not is_valid_header(header)
    ]

def get_header_renames(column_headers):
    """
    Given a list of column headers, returns a mapping from old, invalid headers to
    new, valid headers. Empty if no renames are necessary.
    """
    renames = dict()
    for column_header in column_headers:
        if not is_valid_header(column_header):
            valid_header = make_valid_header(column_header)
            renames[column_header] = valid_header

    return renames


def dfs_to_json(dfs):
    return json.dumps([df_to_json_dumpsable(df) for df in dfs])


def df_to_json_dumpsable(df: pd.DataFrame):
    """
    Returns a dataframe represented in a way that can be turned into a 
    JSON object with json.dumps
    """
    # We make a copy, as we modify the df below
    df = df.copy(deep=True).head(n=2000) # we only show the first 2k rows!
    
    # First, we figure out which of the columns contain dates, and we
    # convert them to string columns (for formatting reasons).
    # NOTE: we don't use date_format='iso' in df.to_json call as it appends seconds to the object, 
    # see here: https://stackoverflow.com/questions/52730953/pandas-to-json-output-date-format-in-specific-form
    date_columns = df.select_dtypes(include=['datetime64'])
    for key in date_columns:
        df[key] = date_columns[key].dt.strftime('%Y-%m-%d %X')

    json_obj = json.loads(df.to_json(orient="split"))
    # Then, we go through and find all the null values (which are infinities),
    # and set them to 'NaN' for display in the frontend.
    for d in json_obj['data']:
        for idx, e in enumerate(d):
            if e is None:
                d[idx] = 'NaN'

    return json_obj


def get_column_filter_type(series):
    """
    Given a series, take's the series dtype and catergorizes the correct
    column_filter_type so that the filter modal can display only
    valid filtering options
    
    TODO: unify this with the other Mito types!
    """
    try: 
        if series.dtype == np.float64 or series.dtype == np.int64:
            return 'number'
        elif series.dtype == 'datetime64[ns]':
            return 'datetime'
        elif series.dtype == np.object:
            return 'string'
    except:
        # If there is an error, we just call this a string column. In the wild, we have
        # seen errors where dtype is not defined on the df object, but we have been
        # unable to replicate this or figure out when it occurs.
        return 'string'
    
    # TODO: what do we do if it's none? for now just return string, for no reason.
    return 'string'

def get_app_directory_from_jupyter_lab_path_output(output):
    """
    Takes the string output of `jupyter lab path` and returns the application folder for jupyter lab.

    The output looks like:
    Application directory:   <application path (depends on what system you are on)>
    User Settings directory: <user settings path (depends on what system you are on)>
    Workspaces directory: <workspace directory path (depends on what system you are on)>
    
    NOTE: this _should_ be able to handle any path we might want, including spaces, or Linux
    or Windows or Mac paths.
    """
    return [x for x in output.split('\n') if x.startswith('Application directory:')][0][len('Application directory:'):].strip()


def is_imported_correctly():
    """
    Helper function to determine if Mito is imported correctly. For this to be the case, 
    Mito must be installed and enabled on a JupyterLab 2.0 instance, along with 
    @jupyter-widgets/jupyterlab-manager.

    We check this by finding out where jupyter lab is installed, and then seeing what 
    extensions are installed. This is not perfect, but should detect most common cases
    """
    try:
        # First, we get the directory that Jupyter is installed in
        result = subprocess.run(["jupyter", "lab", "path"], capture_output=True)
        stdout = result.stdout.decode()
        app_directory = get_app_directory_from_jupyter_lab_path_output(stdout)
        extension_directory = os.path.join(app_directory, 'extensions')
        # Then, we check if the correct extensions are in the extension directory
        if os.path.exists(extension_directory):
            extensions = os.listdir(extension_directory)
            includes_mito = len([extension for extension in extensions if extension.startswith('mitosheet')]) > 0
            includes_jupyter_widgets = len([extension for extension in extensions if extension.startswith('jupyter-widgets-jupyterlab-manager')]) > 0
            return includes_mito and includes_jupyter_widgets
        
        return False
    except:
        return False
    