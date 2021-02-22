"""
Calculation of the transient climate response (TCR)
"""
from .base import Calculator
from .utils import _time_mean


class CalculatorTCR(Calculator):
    """
    Calculator of the transient climate response (TCR)
    """

    @classmethod
    def _can_calculate_metric(cls, metric):
        return metric == "Transient Climate Response"

    @classmethod
    def _calculate(
        cls, assessed_ranges, res_calc, norm_period, evaluation_period, unit
    ):
        res_calc_normed = assessed_ranges._get_normed_res_calc(
            res_calc, norm_period=range(1850, 1850 + 1)
        )

        if evaluation_period is not None and (
            len(evaluation_period) != 1 or evaluation_period[0] != 1920
        ):
            raise NotImplementedError(
                "Evaluation period other than [1920], input: {}".format(
                    evaluation_period
                )
            )

        out = _time_mean(
            res_calc_normed.filter(
                scenario="1pctCO2",
                variable="Surface Air Temperature Change",
                unit=unit,
                region="World",
                year=range(1920, 1921),
            )
        )

        return out
