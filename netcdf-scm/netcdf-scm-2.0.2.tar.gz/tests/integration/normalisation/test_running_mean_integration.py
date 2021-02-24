import datetime as dt
import logging
import re

import pandas as pd
import pytest
import scipy.interpolate
from base_normalisation_integration import NormaliserIntegrationTester

from netcdf_scm.normalisation import NormaliserRunningMean
from netcdf_scm.stitching import get_branch_time


class TestRunningMean(NormaliserIntegrationTester):
    tclass = NormaliserRunningMean

    @pytest.mark.parametrize("nyears", (21, 30))
    @pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
    @pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
    def test_get_reference_values(
        self,
        historical_data_normalisation,
        picontrol_data_normalisation,
        nyears,
        member_id,
        activity_id,
    ):
        # shorten the data so our picontrol data is long enough to be useable
        historical_data_to_use = historical_data_normalisation.filter(
            year=range(1850, 1950)
        ).copy()

        picontrol_branch_time = get_branch_time(historical_data_to_use)

        either_side = nyears // 2 + 1  # ensure we have enough data
        first_relevant_year = picontrol_branch_time.year - either_side
        last_relevant_year = (
            picontrol_branch_time.year
            + historical_data_to_use["year"].max()
            - historical_data_to_use["year"].min()
            + either_side
        )

        ref_ts = picontrol_data_normalisation.filter(
            year=range(first_relevant_year, last_relevant_year + 1)
        ).timeseries()
        ref_values = ref_ts.rolling(
            window=nyears * 12, center=True, axis="columns"
        ).mean()

        relevant_cols = ref_values.columns[
            ref_values.columns.map(
                lambda x: (x.year >= picontrol_branch_time.year)
                and (x.year <= last_relevant_year - either_side)
            )
        ]
        expected = ref_values[relevant_cols]

        expected = expected.reset_index()
        idx = historical_data_to_use.meta.columns.tolist()
        for c in idx:
            if c in ["region", "variable", "unit"]:
                continue

            expected[c] = historical_data_to_use.get_unique_meta(c, no_duplicates=True)

        expected = expected.set_index(idx)
        expected.columns = historical_data_to_use["time"]

        picontrol_data_to_use = picontrol_data_normalisation.copy()
        picontrol_data_to_use["member_id"] = member_id
        picontrol_data_to_use["activity_id"] = activity_id

        res = self.tclass(nyears=nyears).get_reference_values(
            historical_data_to_use, picontrol_data_to_use, picontrol_branch_time,
        )

        pd.testing.assert_frame_equal(res, expected, check_like=True)

    @pytest.mark.parametrize("nyears", (21, 30))
    @pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
    @pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
    def test_get_reference_values_with_extension(
        self,
        historical_data_normalisation,
        picontrol_data_normalisation,
        nyears,
        member_id,
        activity_id,
        caplog,
    ):
        # shorten the data so our picontrol data is long enough to be useable
        historical_data_to_use = historical_data_normalisation.filter(
            year=range(1850, 2000)
        ).copy()

        picontrol_branch_time = get_branch_time(historical_data_to_use)

        either_side = nyears // 2 + 1
        first_relevant_year = (
            picontrol_branch_time.year
            - either_side
            - 5  # don't give quite enough data so some has to be filled
        )
        last_relevant_year = (
            picontrol_branch_time.year
            + historical_data_to_use["year"].max()
            - historical_data_to_use["year"].min()
            + either_side
        )

        picontrol_data_to_use = picontrol_data_normalisation.filter(
            year=range(first_relevant_year, last_relevant_year + 1)
        ).copy()

        ref_ts = picontrol_data_to_use.timeseries()
        ref_values = ref_ts.rolling(
            window=nyears * 12, center=True, axis="columns"
        ).mean()

        expected = ref_values.reset_index()
        idx = historical_data_to_use.meta.columns.tolist()
        for c in idx:
            if c in ["region", "variable", "unit"]:
                continue

            expected[c] = historical_data_to_use.get_unique_meta(c, no_duplicates=True)

        expected = expected.set_index(idx)

        relevant_cols = expected.columns[
            expected.columns.map(
                lambda x: (x.year >= picontrol_branch_time.year)
                and (x.year <= last_relevant_year - either_side)
            )
        ]
        expected = expected[relevant_cols]

        interp_base = expected.dropna(axis=1)

        def _convert_to_s(x):
            return (x - dt.datetime(1970, 1, 1)).total_seconds()

        time_axis_base = interp_base.columns.map(_convert_to_s)
        interpolater = scipy.interpolate.interp1d(
            time_axis_base, interp_base.values, fill_value="extrapolate"
        )

        nan_cols = sorted(list(set(expected.columns) - set(interp_base.columns)))
        time_nan_cols = [_convert_to_s(x) for x in nan_cols]

        expected.loc[:, expected.isnull().any()] = interpolater(time_nan_cols)
        expected.columns = historical_data_to_use["time"]

        picontrol_data_to_use["member_id"] = member_id
        picontrol_data_to_use["activity_id"] = activity_id

        with caplog.at_level(logging.INFO):
            res = self.tclass(nyears=nyears).get_reference_values(
                historical_data_to_use, picontrol_data_to_use, picontrol_branch_time,
            )

        pd.testing.assert_frame_equal(res, expected, check_like=True)
        info_str = (
            "Filling gaps in running mean (where not enough values were available to create a full "
            "window) with linear extrapolations."
        )
        fill_info = [r for r in caplog.record_tuples if r[2] == info_str]
        assert len(fill_info) == 1
        assert fill_info[0][1] == logging.INFO

    @pytest.mark.parametrize("nyears", (21, 30))
    @pytest.mark.parametrize(
        "start_cut,end_cut,expected_error",
        (
            (-(10 ** 3), 30, True),
            (-(10 ** 3), 20, True),
            (-(10 ** 3), 10, True),
            (-(10 ** 3), 5, True),
            (-(10 ** 3), 1, True),
            (-(10 ** 3), 0, False),
            (0, -(10 ** 3), False),
            (-(10 ** 3), -5, False),
            (-5, -(10 ** 3), False),
            (0, 1, True),
            (0, 0, False),
            (-1, 0, False),
            (-1, 1, True),
        ),
    )
    def test_get_reference_values_not_enough_data_error(
        self,
        historical_data_normalisation,
        picontrol_data_normalisation,
        start_cut,
        end_cut,
        expected_error,
        nyears,
        caplog,
    ):
        # shorten the data so our picontrol data is long enough to be useable
        historical_data_to_use = historical_data_normalisation.filter(
            year=range(1850, 1950)
        ).copy()

        picontrol_branch_time = get_branch_time(historical_data_to_use)
        pi_data_to_use = picontrol_data_normalisation.filter(
            year=range(
                picontrol_branch_time.year + start_cut,
                picontrol_branch_time.year
                + historical_data_to_use["year"].max()
                - historical_data_to_use["year"].min()
                - end_cut
                + 1,
            )
        )

        error_msg = re.escape(
            "Only `{:04d}01` to `{:04d}12` is available in the piControl data. "
            "Given the branching time, `084101`, we need data from ~`0830` to `0951`. "
            "piControl data in "
            "{}".format(
                pi_data_to_use["year"].min(),
                pi_data_to_use["year"].max(),
                pi_data_to_use.metadata["netcdf-scm crunched file"],
            )
        )

        def call():
            self.tclass(nyears=nyears).get_reference_values(
                historical_data_to_use, pi_data_to_use, picontrol_branch_time,
            )

        if expected_error:
            with pytest.raises(ValueError, match=error_msg):
                call()

        else:
            with caplog.at_level(logging.INFO):
                call()

            info_str = (
                "Filling gaps in running mean (where not enough values were available to create a full "
                "window) with linear extrapolations."
            )
            info_msg = [r for r in caplog.record_tuples if r[2] == info_str]
            assert len(info_msg) == 1
            assert info_msg[0][1] == logging.INFO
