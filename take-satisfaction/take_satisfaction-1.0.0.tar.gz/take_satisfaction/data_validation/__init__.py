"""Data Validation module.

The main function on this method is `data_validation`, called on the beginning of run code.
Every other validation method is for between process.

Methods:
____________
    * data_validation - Main function of validation layer.
    * dataframe_validation - Perform a content and structure validation.
"""


__all__ = ["data_validation",
           "dataframe_validation"]

from .main import data_validation
from .df_validation import dataframe_validation
