import pandas as pd

from .df_validation import dataframe_validation
from .run_input_validation import input_type_validation


def data_validation(dataframe: pd.DataFrame,
                    scale_column: str,
                    amount_column: str,
                    similarity_threshold: int = 83) -> None:
    """
    
    :param dataframe: A dataframe containing `CSR` scales and the `amount` per scale.
    :type: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type: ``str``
    :param amount_column: Name of column with amount per scale.
    :type: ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    """
    input_type_validation(dataframe=dataframe,
                          similarity_threshold=similarity_threshold)
    
    dataframe_validation(df=dataframe,
                         scale_column=scale_column,
                         amount_column=amount_column)
