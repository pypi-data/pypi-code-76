import typing as tp
import numpy as np

from blipscore_config import Config
from take_blipscore.processing.metrics import blip_metric
from take_blipscore.data_validation import data_validation

MapData = tp.Dict[str, tp.Any]
Output = tp.Dict[str, MapData]


def run(satisfaction_rate: tp.Union[int, float],
        resolution_rate: tp.Union[int, float]) -> Output:
    """Run BLiP Score.
    
    :param satisfaction_rate: Represents a value between 0 and 1 that from satisfaction_rate package.
    :type  satisfaction_rate: ``tp.Union[int, float]``
    :param resolution_rate: Represents a value between 0 and 1 that from resolution_rate package
    :type resolution_rate:  ``tp.Union[int, float]``
    :return: The intelligent contact blip_score.
    :rtype: ``typing.Dict[str, typing.Any]``
    """
    data_validation(satisfaction_rate=satisfaction_rate,
                    resolution_rate=resolution_rate)
    
    x_list = __to_array(satisfation_rate=satisfaction_rate,
                        resolution_rate=resolution_rate)
    
    w_list = __to_array(satisfaction_weight=Config.SATISFACTION_WEIGHT,
                        resolution_weight=Config.RESOLUTION_WEIGHT)

    blip_score = blip_metric(weight=w_list, x=x_list)
    
    return {
        "rate": blip_score,
        "operation": {
            "input": {"satisfaction_rate": satisfaction_rate,
                      "resolution_rate": resolution_rate}
            }
        }


def __to_array(**kwargs) -> np.array:
    """Transform params and rates into arrays.

    :param params: Project params.
    :type params: ``dict`` from ``str`` to ``str``
    :param rates: Metrics rates.
    :type rates: ``dict`` from ``str`` to ``float``
    :return: Weight and rate arrays.
    :rtype: ``list`` from ``numpy.ndarray``
    """
    return np.array(list(kwargs.values()))
