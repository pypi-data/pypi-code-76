import pandas as pd


DF = pd.DataFrame


def input_type_validation(dataframe: DF, similarity_threshold: int) -> None:
    """Validate run input type.
    
    :param dataframe: A dataframe containing `CSR` scales and the `amount` per scale.
    :type: ``pandas.DataFrame``
    :param similarity_threshold: Minimum similarity for str matching.
    :type similarity_threshold: ``int``
    :raise TypeError: if any input is not instance of expected type.
    """
    if not isinstance(dataframe, DF):
        raise TypeError("`dataframe` input must be type `pandas.DataFrame` type")
    
    if not isinstance(similarity_threshold, int):
        raise ValueError("`similarity_threshold` input must be type `int`")