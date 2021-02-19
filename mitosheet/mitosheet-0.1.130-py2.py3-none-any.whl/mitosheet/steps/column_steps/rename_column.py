#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A rename_column step, which allows you to rename a column
in a dataframe.
"""
from mitosheet.parser import safe_replace
from mitosheet.utils import is_valid_header
from mitosheet.steps.column_steps.set_column_formula import _update_column_formula_in_curr_step

from mitosheet.errors import (
    make_invalid_column_headers_error,
    make_column_exists_error, make_no_sheet_error,
)

RENAME_COLUMN_DISPLAY_NAME = 'Renamed a Column'

RENAME_COLUMN_EVENT = 'rename_column_edit'
RENAME_COLUMN_STEP_TYPE = 'rename_column'

RENAME_COLUMN_PARAMS = [
    'sheet_index', # the sheet to delete the column from
    'old_column_header', # the column to rename
    'new_column_header', # the new name for the column
]

    
def execute_rename_column_step(
        wsc,
        sheet_index: int, 
        old_column_header: str, 
        new_column_header: str,
    ):
    """
    Renames the column from df at sheet_index from old_column_header to new_column_header.

    The majority of the work in this function is to update all the references to this other 
    column in all other areas of the step!
    """

    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    if not is_valid_header(new_column_header):
        raise make_invalid_column_headers_error([new_column_header])

    if new_column_header in wsc.curr_step['dfs'][sheet_index].keys():
        raise make_column_exists_error(new_column_header)

    # Create and checkout a rename step
    wsc._create_and_checkout_new_step(RENAME_COLUMN_STEP_TYPE)

    # Execute the rename
    wsc.curr_step['dfs'][sheet_index].rename(columns={old_column_header: new_column_header}, inplace=True)

    # Then, we update the current step to be valid, namely by deleting the old column (wherever it is)
    # and replacing it with the new column. 
    sheet_column_metatype = wsc.curr_step['column_metatype'][sheet_index]
    sheet_column_metatype[new_column_header] = sheet_column_metatype[old_column_header]

    sheet_column_type = wsc.curr_step['column_type'][sheet_index]
    sheet_column_type[new_column_header] = sheet_column_type[old_column_header]

    sheet_column_spreadsheet_code = wsc.curr_step['column_spreadsheet_code'][sheet_index]
    sheet_column_spreadsheet_code[new_column_header] = sheet_column_spreadsheet_code[old_column_header]

    sheet_column_python_code = wsc.curr_step['column_python_code'][sheet_index]
    sheet_column_python_code[new_column_header] = sheet_column_python_code[old_column_header].replace(
        f'df[\'{old_column_header}\']',
        f'df[\'{new_column_header}\']'
    )
    
    sheet_column_evaluation_graph = wsc.curr_step['column_evaluation_graph'][sheet_index]
    sheet_column_evaluation_graph[new_column_header] = sheet_column_evaluation_graph[old_column_header]

    sheet_column_filters = wsc.curr_step['column_filters'][sheet_index]
    sheet_column_filters[new_column_header] = sheet_column_filters[old_column_header]

    # We also have to go over _all_ the formulas in the sheet that reference this column, and update
    # their references to the new column. 
    for column_header in sheet_column_evaluation_graph[new_column_header]:
        old_formula = sheet_column_spreadsheet_code[column_header]
        new_formula = safe_replace(
            old_formula,
            old_column_header,
            new_column_header
        )

        # NOTE: this does not update the evaluation graph for columns that are descendents
        # of this column, so we do that below.
        _update_column_formula_in_curr_step(wsc, sheet_index, column_header, old_formula, new_formula)

    # We then have to go through and update the evaluation graphs
    # for the columns the renamed column relied on.
    for dependents in sheet_column_evaluation_graph.values():
        if old_column_header in dependents:
            dependents.remove(old_column_header)
            dependents.add(new_column_header)

    # We delete all references to the old_column header
    # NOTE: this has to happen after the above formula setting, so that
    # the dependencies can be updated properly!
    del sheet_column_metatype[old_column_header]
    del sheet_column_type[old_column_header]
    del sheet_column_spreadsheet_code[old_column_header]
    del sheet_column_python_code[old_column_header]
    del sheet_column_evaluation_graph[old_column_header]
    del sheet_column_filters[old_column_header]


def transpile_rename_column_step(
        widget_state_container,
        step,
        sheet_index,
        old_column_header,
        new_column_header
    ):
    df_name = step["df_names"][sheet_index]
    rename_dict = "{\"" + old_column_header + "\": \"" + new_column_header + "\"}"
    return [f'{df_name}.rename(columns={rename_dict}, inplace=True)']


def describe_rename_column_step(
        widget_state_container,
        step,
        sheet_index,
        old_column_header,
        new_column_header
    ):
    df_name = step["df_names"][sheet_index]
    return f'Renamed {old_column_header} to {new_column_header} in {df_name}'


RENAME_COLUMN_STEP = {
    'step_version': 1,
    'step_display_name': RENAME_COLUMN_DISPLAY_NAME,
    'event_type': RENAME_COLUMN_EVENT,
    'step_type': RENAME_COLUMN_STEP_TYPE,
    'params': RENAME_COLUMN_PARAMS,
    'saturate': None,
    'execute': execute_rename_column_step,
    'transpile': transpile_rename_column_step,
    'describe': describe_rename_column_step
}