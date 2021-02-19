#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A add_column step, which allows you to add a column to 
a dataframe. 
"""

from mitosheet.errors import (
    make_column_exists_error,
    make_no_sheet_error
)

ADD_COLUMN_DISPLAY_NAME = 'Added a Column'

ADD_COLUMN_EVENT = 'add_column_edit'
ADD_COLUMN_STEP_TYPE = 'add_column'

ADD_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # the new column to create
]

def execute_add_column_step(
        wsc,
        sheet_index,
        column_header
    ):
    """
    The function responsible for updating the widget state container
    with a new add_column step.
    """
    
    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    if column_header in wsc.curr_step['column_metatype'][sheet_index]:
        raise make_column_exists_error(column_header)

    # We add a new step with the added column
    wsc._create_and_checkout_new_step(ADD_COLUMN_STEP_TYPE)

    # Update the state variables
    wsc.curr_step['column_metatype'][sheet_index][column_header] = 'formula'
    wsc.curr_step['column_type'][sheet_index][column_header] = 'number'
    wsc.curr_step['column_spreadsheet_code'][sheet_index][column_header] = '=0'
    wsc.curr_step['column_python_code'][sheet_index][column_header] = f'df[\'{column_header}\'] = 0'
    wsc.curr_step['column_evaluation_graph'][sheet_index][column_header] = set()
    wsc.curr_step['column_filters'][sheet_index][column_header] = {'operator': 'And', 'filters': []}

    # Update the dataframe
    wsc.curr_step['dfs'][sheet_index][column_header] = 0


def transpile_add_column_step(
        widget_state_container,
        step,
        sheet_index,
        column_header
    ):
    """
    Transpiles an add column step to python code!
    """

    return [
        f'{step["df_names"][sheet_index]}[\'{column_header}\'] = 0'
    ]


def describe_add_column_step(
        widget_state_container,
        step,
        sheet_index,
        column_header
    ):
    return f'Added column {column_header} to {step["df_names"][sheet_index]}'


ADD_COLUMN_STEP = {
    'step_version': 1,
    'step_display_name': ADD_COLUMN_DISPLAY_NAME,
    'event_type': ADD_COLUMN_EVENT,
    'step_type': ADD_COLUMN_STEP_TYPE,
    'params': ADD_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_add_column_step,
    'transpile': transpile_add_column_step,
    'describe': describe_add_column_step
}