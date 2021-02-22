import typing as tp
import pandas as pd

from satisfaction_config import Config
from take_satisfaction.preprocess import remove_manual, convert_scale
from take_satisfaction.core import calculate_satisfaction_rate
from take_satisfaction.data_validation import dataframe_validation, data_validation


def run(dataframe: pd.DataFrame, scale_column: str, amount_column: str, similarity_threshold: int = 83) -> tp.Dict[str, tp.Any]:
    """Run Take Satisfaction

    :param dataframe: A dataframe containing `CSR` scales and the `amount` per scale.
    :type: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type: ``str``
    :param amount_column: Name of column with amount per scale.
    :type: ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :return: Satisfaction rate in report mode.
    :rtype:  ``typing.Dict[str, typing.Any]``
    """
    data_validation(dataframe=dataframe,
                    scale_column=scale_column,
                    amount_column=amount_column,
                    similarity_threshold=similarity_threshold)
    
    preprocessed_df = remove_manual(df=dataframe,
                                    known_manual_inputs=Config.KNOWN_MANUAL_INPUTS,
                                    similarity_threshold=similarity_threshold,
                                    scale_column=scale_column)
    
    dataframe_validation(df=preprocessed_df,
                         scale_column=scale_column,
                         amount_column=amount_column)
    
    converted_df = convert_scale(df=preprocessed_df,
                                 scale_column=scale_column,
                                 scale_translations=Config.SCALE_TRANSLATIONS,
                                 similarity_threshold=similarity_threshold)
    
    satisfaction_rate = calculate_satisfaction_rate(df=converted_df,
                                                    scale_column=scale_column,
                                                    amount_column=amount_column)
    
    return {
        "rate": satisfaction_rate,
        "similarity_threshold": similarity_threshold,
        "operation": {
            "input": dataframe,
            "preprocessed": preprocessed_df,
            "converted": converted_df
            }
        }
