import typing as tp

import unidecode as uni
import emoji
import pandas as pd
from fuzzywuzzy import fuzz

from take_satisfaction.custom_exceptions import NoSuitableTranslationError

DF = pd.DataFrame
SR = pd.Series


def __convert_numeric_answer_column(df: DF, scale_column: str) -> DF:
    """Converts the target column's answers to integers by casting.

    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type df: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type scale_column: ``str``
    :return: Dataframe with the target column's answers converted into integers.
    :rtype: ``pandas.Dataframe``
    """
    df.loc[:, scale_column] = pd.to_numeric(df[scale_column])
    return df


def __convert_answer(answer: str, scale_translations: tp.List[str], similarity_threshold: int) -> int:
    """Converts answer to the index of its best match on the reference scale.

    Answer is like "Gostei", "Muito ruim"...
    And index range from negative to positive as they appear on the reference.
    Raises an exception if there is no reference similar enough.

    :param answer: String with scale answer.
    :type answer: ``str``
    :param scale_translations: List with answer variations appearing from negative to positive.
    :type scale_translations: ``list`` from ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :return: Index of the best match on the reference scale.
    :rtype: ``int``
    """
    answer = emoji.demojize(answer)
    similarity = [
        (fuzz.ratio(uni.unidecode(answer.lower()), uni.unidecode(value.lower())), idx)
        for idx, value in enumerate(scale_translations)
    ]
    
    max_similarity, position = max(similarity)
    
    if max_similarity >= similarity_threshold:
        return position
    raise NoSuitableTranslationError('Scale not found for: `' + str(answer) + '`')


def __convert_scale_to_indexes(df: DF,
                               scale_column: str,
                               scale_translations: tp.List[str],
                               similarity_threshold: int) -> DF:
    """Converts df column answers to the index of its best match on the reference scale.

    Raises an exception if the scale_conversion fails.

    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type df: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type scale_column: ``str``
    :param scale_translations: List with answer variations appearing from negative to positive.
    :type scale_translations: ``list`` from ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe`
    """
    df_converted = df.copy()
    df_converted.loc[:, scale_column] = df[scale_column].apply(__convert_answer,
                                                               args=(scale_translations, similarity_threshold))
    return df_converted


def __normalizes_scale_answers(df: DF, scale_column: str) -> DF:
    """Normalizes df column answers to an integer scale with a step of one.

    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type df: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type scale_column: ``str``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe`
    """
    sorted_df = df.sort_values(by=scale_column, axis=0)
    sorted_df.loc[:, scale_column] = [i for i in range(len(sorted_df))]
    return sorted_df


def is_numeric_scale(df: DF, column: str) -> bool:
    """Validates whether the answers in the target column of the df are numeric.

    Returns True if the column's items are numeric.

    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type df: ``pandas.Dataframe``
    :param column: Column to assert data is numeric type.
    :type column: ``str``
    :return: Boolean indicating whether the column is numeric or not.
    :rtype: ``bool``
    """
    return pd.to_numeric(df[column], errors='coerce').notnull().all()


def convert_scale(df: DF, scale_column: str, scale_translations: tp.List[str], similarity_threshold: int) -> DF:
    """Converts df column answers to its satisfaction levels.

    :param df: A dataframe containing `CSR` scales and the `amount` per scale.
    :type: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type: ``str``
    :param scale_translations: List with answer variations appearing from negative to positive.
    :type scale_translations: ``list`` from ``str``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe``
    """
    if is_numeric_scale(df, column=scale_column):
        return __convert_numeric_answer_column(df=df, scale_column=scale_column) \
            .sort_values(by=scale_column, axis=0) \
            .reset_index(drop=True)

    converted_scale = __convert_scale_to_indexes(df,
                                                 scale_column=scale_column,
                                                 scale_translations=scale_translations,
                                                 similarity_threshold=similarity_threshold)
    return __normalizes_scale_answers(df=converted_scale,
                                      scale_column=scale_column)
