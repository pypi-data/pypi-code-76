import pandas as pd

from .run_input_validation import input_type_validation


def data_validation(dataframe: pd.DataFrame) -> None:
    """Main function of validation layer.
    
    This method call all other validation that must exist on beginning of run.

    ::param dataframe: A dataframe containing daily resolution and DAUs.
    :type: ``pandas.DataFrame``
    """
    input_type_validation(dataframe=dataframe)
