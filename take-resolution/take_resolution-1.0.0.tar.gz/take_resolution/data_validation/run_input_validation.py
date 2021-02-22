import pandas as pd


DF = pd.DataFrame


def input_type_validation(dataframe: DF) -> None:
    """Validate run input type.
    
    :param dataframe: A dataframe containing daily resolution and DAUs.
    :type: ``pandas.DataFrame``
    :raise TypeError: if any input is not instance of expected type.
    """
    if not isinstance(dataframe, DF):
        raise TypeError("`dataframe` input must be type `pandas.DataFrame` type")
