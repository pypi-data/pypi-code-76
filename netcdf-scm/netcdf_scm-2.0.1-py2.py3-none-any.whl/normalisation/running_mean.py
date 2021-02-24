"""
Module for the normaliser which calculates anomalies from a running mean in the pre-industrial control run
"""
import logging

from scmdata import ScmRun

from ..cli_utils import _check_timesteps_are_monthly
from .base import Normaliser

LOGGER = logging.getLogger(__name__)


class NormaliserRunningMean(Normaliser):
    """
    Normaliser which calculates anomalies from a running mean in the pre-industrial control run

    Each normalisation value is an n-year mean, centred on the equivalent point in the
    pre-industrial control simulation. If there is insufficient data to create a full n-year
    window at the edge of the simulation then a linear extrapolation of the running-mean is used
    to extend the normalisation values to cover the required full range.
    """

    def __init__(self, nyears=21):
        """
        Intialise

        Parameters
        ----------
        nyears : int
            Number of years to use in the running-mean.
        """
        self._nyears = nyears
        self._method_name = "{}-yr-running-mean".format(nyears)

    def _get_reference_values(self, indata, picontrol, picontrol_branching_time):
        running_mean_n_years = self._nyears
        months_per_year = 12
        window_width = running_mean_n_years * months_per_year
        window_roll_back = window_width // 2
        # the window extends one step fewer forward because the centre time point
        # is also included
        window_roll_forward = window_roll_back - 1

        branch_year = picontrol_branching_time.year
        branch_month = picontrol_branching_time.month
        picontrol_branch_col = picontrol.filter(year=branch_year, month=branch_month)[
            "time"
        ][0]
        picontrol_time = picontrol["time"]
        picontrol_branch_idx = (picontrol_time == picontrol_branch_col).idxmax()

        # relevant times go from the branch point minus the number of steps each
        # rolling mean window extends backward up to the branch point plus the
        # length of ``indata`` plus the number of steps the rolling mean window
        # extends forward
        relevant_time_points = picontrol_time[
            max(picontrol_branch_idx - window_roll_back, 0) : picontrol_branch_idx
            + indata["time"].shape[0]
            + window_roll_forward
        ].tolist()

        _check_timesteps_are_monthly(picontrol)  # quick sanity check

        # super slow option below, would be good to have direct functionality in scmdata
        # normalise_ts = picontrol.filter(time=relevant_time_points.tolist()).timeseries()

        picontrol_times = (picontrol["time"] >= relevant_time_points[0]) & (
            picontrol["time"] <= relevant_time_points[-1]
        )
        normalise_ts = picontrol.timeseries().iloc[:, picontrol_times.values]

        normalise_df = normalise_ts.rolling(
            window=window_width, center=True, axis="columns",
        ).mean()

        keep_time_points = picontrol_time[
            picontrol_branch_idx : picontrol_branch_idx + indata["time"].shape[0]
        ].tolist()

        raise_error = False
        try:
            normalise_df = normalise_df[keep_time_points]
        except KeyError:
            raise_error = True

        if normalise_df.isnull().any().any():
            LOGGER.info(
                "Filling gaps in running mean (where not enough values were available to create a full "
                "window) with linear extrapolations."
            )

            target_times = normalise_df.columns
            normalise_df = (
                ScmRun(normalise_df)
                .interpolate(target_times=target_times, extrapolation_type="linear")
                .timeseries()
            )

        if normalise_df.isnull().any().any():
            # if there are any remaining gaps, raise
            raise_error = True

        try:
            normalise_df.columns = indata["time"]
        except ValueError:
            raise_error = True

        if raise_error:
            error_msg = (
                "Only `{:04d}{:02d}` to `{:04d}{:02d}` is available in the "
                "{} data. Given the branching time, `{:04d}{:02d}`, we need "
                "data from ~`{:04d}` to `{:04d}`. {} data in {}".format(
                    picontrol["time"].min().year,
                    picontrol["time"].min().month,
                    picontrol["time"].max().year,
                    picontrol["time"].max().month,
                    picontrol.metadata["experiment_id"],
                    picontrol_branching_time.year,
                    picontrol_branching_time.month,
                    picontrol_branching_time.year - 11,
                    picontrol_branching_time.year
                    + indata["year"].max()
                    - indata["year"].min()
                    + 11,
                    picontrol.metadata["experiment_id"],
                    picontrol.metadata["netcdf-scm crunched file"],
                )
            )
            raise ValueError(error_msg)

        return normalise_df
