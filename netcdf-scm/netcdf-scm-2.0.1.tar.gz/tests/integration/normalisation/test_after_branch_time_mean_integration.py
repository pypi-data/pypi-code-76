import re

import pandas as pd
import pytest
from base_normalisation_integration import NormaliserIntegrationTester

from netcdf_scm.normalisation import AfterBranchTimeMean
from netcdf_scm.stitching import get_branch_time


class TestRunningMean(NormaliserIntegrationTester):
    tclass = AfterBranchTimeMean

    @pytest.mark.parametrize("member_id", ("r1i1p1f1", "r10i1p1f1"))
    @pytest.mark.parametrize("activity_id", ("ScenarioMIP", "RFMIP"))
    def test_get_reference_values(
        self,
        historical_data_normalisation,
        picontrol_data_normalisation,
        member_id,
        activity_id,
    ):
        picontrol_branch_time = get_branch_time(historical_data_normalisation)

        ref_mean = (
            picontrol_data_normalisation.filter(
                year=range(picontrol_branch_time.year, picontrol_branch_time.year + 31)
            )
            .timeseries()
            .mean(axis=1)
        )
        expected = pd.concat(
            [ref_mean] * historical_data_normalisation["time"].shape[0], axis=1
        )
        expected.columns = historical_data_normalisation["time"]

        expected = expected.reset_index()
        idx = historical_data_normalisation.meta.columns.tolist()
        for c in idx:
            if c in ["region", "variable", "unit"]:
                continue

            expected[c] = historical_data_normalisation.get_unique_meta(
                c, no_duplicates=True
            )

        expected = expected.set_index(idx)

        picontrol_data_to_use = picontrol_data_normalisation.copy()
        picontrol_data_to_use["member_id"] = member_id
        picontrol_data_to_use["activity_id"] = activity_id

        res = self.tclass().get_reference_values(
            historical_data_normalisation, picontrol_data_to_use, picontrol_branch_time,
        )

        pd.testing.assert_frame_equal(res, expected, check_like=True)

    def test_get_reference_values_not_enough_data_error(
        self, historical_data_normalisation, picontrol_data_normalisation
    ):
        picontrol_branch_time = get_branch_time(historical_data_normalisation)
        pi_data_to_use = picontrol_data_normalisation.filter(
            year=range(picontrol_branch_time.year, picontrol_branch_time.year + 10)
        )

        error_msg = re.compile(
            ".*Only `084101` to `085012` is available after the branching time `084101` in piControl "
            "data in "
            "{}".format(pi_data_to_use.metadata["netcdf-scm crunched file"])
        )

        with pytest.raises(ValueError, match=error_msg):
            self.tclass().get_reference_values(
                historical_data_normalisation, pi_data_to_use, picontrol_branch_time,
            )
