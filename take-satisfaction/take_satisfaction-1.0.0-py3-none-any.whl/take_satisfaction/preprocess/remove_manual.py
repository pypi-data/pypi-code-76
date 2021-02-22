import typing as tp

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

DF = pd.DataFrame
S = pd.Series


def __match_manual(series: S, known_manual_inputs: tp.List[str], similarity_threshold: int) -> np.ndarray:
    """Returns a series describing whether each element in the series is a manual entry.
    
    :param series: The scales list to match.
    :type series: ``pandas.Series``
    :param known_manual_inputs: Manual entry variations.
    :type known_manual_inputs: ``list`` of ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :return: Series describing whether each element is a manual entry.
    :rtype: ``numpy.ndarray`` of ``bool``
    """
    return np.array([
        (isinstance(sample, str) and
         any(fuzz.ratio(sample.lower(), entry.lower()) >= similarity_threshold for entry in known_manual_inputs))
        for sample in series
    ])


def remove_manual(df: DF, known_manual_inputs: tp.List[str], similarity_threshold: int, scale_column: str) -> DF:
    """Checks for a manual entry row in the scale and removes it.

    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param known_manual_inputs: Manual entry variations.
    :type known_manual_inputs: ``list`` of ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :param scale_column: Target column to be analysed.
    :type scale_column: ``str``
    :return: Dataframe with the bot scale without manual entries.
    :rtype: ``pandas.DataFrame``
    """
    return df[~__match_manual(series=df[scale_column],
                              known_manual_inputs=known_manual_inputs,
                              similarity_threshold=similarity_threshold)]
