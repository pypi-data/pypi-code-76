#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A change_column_type step, which allows you to cast a single column
to a different type.

NOTE: this is a bit of a wonky step, as it has to handle both formula
columns and non-formula columns. See comments below for information 
on how this is done. 

NOTE NOTE NOTE NOTE

THIS CODE HAS NO CORRESPONDING UI COMPONENT AND HAS NOT BEEN
TESTED THOROUGHLY. BEFORE USING THIS CODE, MAKE SURE IT HAS 
BEEN UPDATED TO MAKE SENSE WITH THE NEW CODEBASE.

We left the UI component for this out, because of how this step
interacts with Filter strangely, as filter steps can get deleted
and then remade again.

NOTE NOTE NOTE NOTE
"""

from mitosheet.errors import make_invalid_column_type_change_error
from mitosheet.utils import get_column_filter_type
from mitosheet.sheet_functions.types import SERIES_CONVERSION_FUNCTIONS
from mitosheet.steps.column_steps.set_column_formula import SET_COLUMN_FORMULA_STEP, _execute

CHANGE_COLUMN_TYPE_EVENT = 'change_column_type_edit'
CHANGE_COLUMN_TYPE_STEP_TYPE = 'change_column_type'

CHANGE_COLUMN_TYPE_PARAMS = [
    'sheet_index',
    'column_header',
    'old_column_type', # This is saturated
    'new_column_type'
]

def saturate_change_column_type(
        wsc,
        event
    ):
    """
    Fills in the old_column_type.
    """
    sheet_index = event['sheet_index']
    column_header = event['column_header']
    event['old_column_type'] = get_column_filter_type(
        wsc.dfs[sheet_index][column_header]
    )

# For each type, the sheet function name that converts to this type
SHEET_FUNCTION_NAME = {
    'boolean_series': 'BOOL',
    'string_series': 'TEXT',
    'number_series': 'VALUE',
    'datetime_series': 'DATEVALUE'
}

def execute_change_column_type(
        wsc,
        sheet_index, 
        column_header,
        old_column_type,
        new_column_type
    ):
    """
    Responsible for executing the change_column_type_edit. Note that if
    the column that is having its type changed is a formula column, then
    this function will delegate it's step creation responsibility to the
    the SET_COLUMN_FORMULA_STEP.
    """

    # We first check if the column that is having it's type changed is a formula
    # column, and if so, we just wrap it's current formula with a sheet function
    # that changes it into the correct type
    old_formula = wsc.curr_step['column_spreadsheet_code'][sheet_index][column_header]
    if old_formula != '':
        sheet_function_wrapper = SHEET_FUNCTION_NAME[new_column_type]
        # Handle the optional equals sign
        if old_formula.startswith('='):
            new_formula = f'{sheet_function_wrapper}({old_formula[1:]})'
        else:
            new_formula = f'{sheet_function_wrapper}({old_formula})'

        SET_COLUMN_FORMULA_STEP['execute'](
            wsc,
            sheet_index,
            column_header,
            old_formula,
            new_formula
        )
        # Save the params, as they aren't saved in the case
        wsc.curr_step['sheet_index'] = sheet_index
        wsc.curr_step['column_header'] = column_header
        wsc.curr_step['old_formula'] = old_formula
        wsc.curr_step['new_formula'] = new_formula
        # NOTE: we need to return here, we only want to create one step
        return
            
    # Otherwise, if this is not a formula column, we create a new step
    wsc._create_and_checkout_new_step(CHANGE_COLUMN_TYPE_STEP_TYPE)

    # Look up the conversion function we need
    conversion_function = SERIES_CONVERSION_FUNCTIONS[new_column_type]
    # and convert the column
    converted_column = conversion_function(wsc.curr_step['dfs'][sheet_index][column_header])
    if converted_column is None:
        # If the conversion fails, we throw an error
        raise make_invalid_column_type_change_error(column_header, old_column_type, new_column_type)
    wsc.curr_step['dfs'][sheet_index][column_header] = converted_column

    # Execute all downstream functions from this column
    # NOTE: this execute is from the set_column_formula
    _execute(wsc, wsc.curr_step['dfs'][sheet_index], sheet_index)

    # Finially, update the type of the filters of this column, for all the filters
    # TODO: fix bug where the downsteam column types are not updated
    new_type = get_column_filter_type(wsc.curr_step['dfs'][sheet_index][column_header])
    wsc.curr_step['column_type'][sheet_index][column_header] = new_type
    wsc.curr_step['column_filters'][sheet_index][column_header]['filters'] = [
        {'type': new_type, 'condition': filter_['condition'], 'value': filter_['value']} 
        for filter_ in wsc.curr_step['column_filters'][sheet_index][column_header]['filters']
    ]


def transpile_change_column_type(
        widget_state_container,
        step,
        sheet_index, 
        column_header,
        old_column_type,
        new_column_type
    ):
    """
    Transpiles a change_column_formula step. 

    NOTE: we do not need to handle transpiling the case where the column with the type
    being changed is a formula column, as the step that is created in this case is just 
    a pure set_column_formula step, and so that step handles the transpiling in that 
    case!
    """
    # Write the code that uses the mito function to do the conversion
    conversion_function_name = SERIES_CONVERSION_FUNCTIONS[new_column_type].__name__
    df_name = step['df_names'][sheet_index]
    code = [f'{df_name}[\'{column_header}\'] = {conversion_function_name}({df_name}[\'{column_header}\'])']
    
    # Furthermore, we _always_ include the transpiled code from the SET_COLUMN_FORMULA_STEP, as we
    # need to run the "downstream" columns of the column with the changed type. 
    return code + SET_COLUMN_FORMULA_STEP['transpile'](
        widget_state_container,
        step,
        sheet_index,
        column_header,
        # NOTE: we pass in invalid values, as they aren't needed in transpile, and they are hard to get
        None,
        None
    )


CHANGE_COLUMN_TYPE_STEP = {
    'step_version': 1,
    'event_type': CHANGE_COLUMN_TYPE_EVENT,
    'step_type': CHANGE_COLUMN_TYPE_STEP_TYPE,
    'params': CHANGE_COLUMN_TYPE_PARAMS,
    'saturate': saturate_change_column_type,
    'execute': execute_change_column_type,
    'transpile': transpile_change_column_type
}