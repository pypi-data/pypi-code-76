"""
Calculation of the transient climate response (TCR)
"""
import scmdata

from .base import Calculator
from .utils import _add_index_level, _time_mean


class CalculatorTCRE(Calculator):
    """
    Calculator of the transient climate response to emissions (TCRE)
    """

    @classmethod
    def _can_calculate_metric(cls, metric):
        return metric == "Transient Climate Response to Emissions"

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

        common_filters = dict(scenario="1pctCO2", region="World",)
        gsat_var = "Surface Air Temperature Change"
        cumulative_emms_var = "Cumulative Emissions|CO2"
        temperatures = res_calc_normed.filter(variable=gsat_var, **common_filters)
        cumulative_emissions = res_calc_normed.filter(
            variable=cumulative_emms_var, **common_filters
        )

        tcre = []
        for temperatures_cm in temperatures.groupby("climate_model"):
            climate_model = temperatures_cm.get_unique_meta("climate_model")
            cumulative_emissions_cm = cumulative_emissions.filter(
                climate_model=climate_model
            )
            if cumulative_emissions_cm.empty:
                continue

            tcre_cm = temperatures_cm.divide(
                cumulative_emissions_cm, op_cols={"variable": "TCRE"}
            )
            tcre.append(tcre_cm)

        tcre = scmdata.run_append(tcre)

        out = _time_mean(tcre.filter(year=range(1920, 1921)).convert_unit(unit))

        out = _add_index_level(
            out.reset_index("variable", drop=True),
            ",".join([gsat_var, cumulative_emms_var]),
            "variable",
        )

        return out
