import pandas as pd

from take_satisfaction.custom_exceptions import (InvalidDataframeError,
                                                 AbsentColumnError)

DF = pd.DataFrame


def dataframe_content_validation(df: DF) -> None:
    """Validates if df is not empty.
    
    :raise InvalidDataframeError: if dataframe is empty

    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    """
    if df.empty:
        raise InvalidDataframeError('Cannot process empty scale')


def dataframe_has_columns(df: DF, scale_column: str, amount_column: str) -> None:
    """Validates if df is not empty, if it has an answer column and a quantity column.

    :raise AbsentColumnError: If `scale_column` or `amount_column` is not present on dataframe.
    
    :param df: Dataframe with satisfaction levels and its quantities.
    :type df: ``pandas.Dataframe``
    :param scale_column: Name of the scale column.
    :type: ``str``
    :param amount_column: Name of column with amount per scale.
    :type: ``str``
    """
    if scale_column not in df.columns:
        raise AbsentColumnError('Scale does not contain answer column `' + str(scale_column) + '`')
    
    if amount_column not in df.columns:
        raise AbsentColumnError('Scale does not contain quantity column `' + str(amount_column) + '`')
    
    
def dataframe_validation(df: DF, scale_column: str, amount_column: str) -> None:
    """Perform a content and structure validation.
    
    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type df: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type: ``str``
    :param amount_column: Name of column with amount per scale.
    :type: ``str``
    """
    dataframe_has_columns(df=df,
                          scale_column=scale_column,
                          amount_column=amount_column)
    
    dataframe_content_validation(df=df)
