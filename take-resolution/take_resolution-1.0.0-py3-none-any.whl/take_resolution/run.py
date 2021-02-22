import typing as tp
import pandas as pd
import numpy as np

from take_resolution.core.metrics import resolution_metric, daily_resolution
from take_resolution.data_validation import data_validation


def run(dataframe: pd.DataFrame, amount: str, dau_column: str) -> tp.Dict[str, tp.Any]:
    """Run Take Resolution

    :param dataframe: A dataframe containing daily resolution and DAUs.
    :type: ``pandas.DataFrame``
    :param amount: Name of column that contains amount unique users per resolution node.
    :type amount: ``str``
    :param dau_column: Name of the column that contains DAUs
    :type dau_column: ``str``
    :return: Resolution rate in report mode.
    :rtype:  ``typing.Dict[str, typing.Any]``
    """
    data_validation(dataframe=dataframe)
    
    daily_array = daily_resolution(dataframe=dataframe,
                                   dau_column=dau_column,
                                   amount=amount)
    
    resolution_rate = resolution_metric(daily_resolution_rate=daily_array,
                                        DAU=np.array(dataframe[dau_column]))
    
    return {
        "rate": resolution_rate,
        "daily_resolution": daily_array,
        "operation": {
            "input": dataframe
            }
        }
