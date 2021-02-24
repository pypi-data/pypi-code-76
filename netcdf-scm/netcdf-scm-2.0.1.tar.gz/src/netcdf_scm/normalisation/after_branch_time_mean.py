"""
Module for the normaliser which calculates anomalies from a mean of a fixed number of years in the pre-industrial control run
"""

import logging

import pandas as pd

from .base import Normaliser

LOGGER = logging.getLogger(__name__)


class AfterBranchTimeMean(Normaliser):
    """
    Normaliser which calculates anomalies from a mean of a fixed number of years after the branch time in the pre-industrial control run

    At present, only a 31-year mean after the branch time is implemented.
    """

    def __init__(self):
        self._method_name = "31-yr-mean-after-branch-time"

    @staticmethod
    def _get_reference_values(indata, picontrol, picontrol_branching_time):
        branch_year = picontrol_branching_time.year
        normalise_series = picontrol.filter(year=range(branch_year, branch_year + 31))

        if (
            normalise_series["time"].max().year - normalise_series["time"].min().year
        ) != 30:
            error_msg = (
                "Only `{:04d}{:02d}` to `{:04d}{:02d}` is available after the "
                "branching time `{:04d}{:02d}` in {} data in {}".format(
                    normalise_series["time"].min().year,
                    normalise_series["time"].min().month,
                    normalise_series["time"].max().year,
                    normalise_series["time"].max().month,
                    picontrol_branching_time.year,
                    picontrol_branching_time.month,
                    picontrol.metadata["experiment_id"],
                    picontrol.metadata["netcdf-scm crunched file"],
                )
            )
            raise ValueError(error_msg)

        normalise_mean = normalise_series.timeseries().mean(axis=1)
        # normalisation is uniform for all timepoints
        normalise_df = pd.concat([normalise_mean] * indata["time"].shape[0], axis=1)
        normalise_df.columns = indata["time"]

        return normalise_df
