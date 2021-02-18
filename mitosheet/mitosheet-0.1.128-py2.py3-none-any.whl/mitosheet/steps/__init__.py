#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
See mito/mitosheet/steps/README.md for more information about 
how to add a step!

NOTE: this new step refactor is a WIP, and will not be finished
until we remove all the manual step casing that occurs throughout the 
codebase. This is an incremental process that will take time!
"""

from mitosheet.steps.pivot import PIVOT_STEP
from mitosheet.steps.filter import FILTER_STEP
from mitosheet.steps.sort import SORT_STEP
from mitosheet.steps.column_steps.reorder_column import REORDER_COLUMN_STEP
from mitosheet.steps.column_steps.add_column import ADD_COLUMN_STEP
from mitosheet.steps.column_steps.set_column_formula import SET_COLUMN_FORMULA_STEP
from mitosheet.steps.column_steps.change_column_type import CHANGE_COLUMN_TYPE_STEP
from mitosheet.steps.merge import MERGE_STEP
from mitosheet.steps.column_steps.delete_column import DELETE_COLUMN_STEP
from mitosheet.steps.column_steps.rename_column import RENAME_COLUMN_STEP
from mitosheet.steps.import_steps.simple_import import SIMPLE_IMPORT_STEP
from mitosheet.steps.import_steps.raw_python_import import RAW_PYTHON_IMPORT_STEP
from mitosheet.steps.dataframe_steps.dataframe_delete import DATAFRAME_DELETE_STEP
from mitosheet.steps.dataframe_steps.dataframe_duplicate import DATAFRAME_DUPLICATE_STEP
from mitosheet.steps.dataframe_steps.dataframe_rename import DATAFRAME_RENAME_STEP

# All steps must be listed in this variable.
STEPS = [
    PIVOT_STEP,
    REORDER_COLUMN_STEP,
    FILTER_STEP,
    SORT_STEP,
    ADD_COLUMN_STEP,
    SET_COLUMN_FORMULA_STEP,
    CHANGE_COLUMN_TYPE_STEP,
    MERGE_STEP,
    DELETE_COLUMN_STEP,
    RENAME_COLUMN_STEP,
    SIMPLE_IMPORT_STEP,
    RAW_PYTHON_IMPORT_STEP,
    DATAFRAME_DELETE_STEP,
    DATAFRAME_DUPLICATE_STEP,
    DATAFRAME_RENAME_STEP
]