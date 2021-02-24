import datetime as dt
import re
from abc import ABC, abstractmethod
from unittest.mock import patch

import pandas as pd
import pytest

from netcdf_scm.stitching import get_branch_time


@pytest.mark.usefixtures("junk_data_normalisation", "junk_data_picontrol_normalisation")
class NormaliserTester(ABC):
    tclass = None

    @abstractmethod
    def test_method_name(self):
        """
        assert self.tclass().method_name == expected_name
        """

    def test_get_reference_values_no_branch_time_data(
        self, junk_data_normalisation, junk_data_picontrol_normalisation
    ):
        picontrol_branch_time = get_branch_time(junk_data_normalisation)
        pi_data_to_use = junk_data_picontrol_normalisation.filter(
            year=picontrol_branch_time.year, keep=False
        )

        error_msg = re.compile(
            ".*Branching time `185001` not available in piControl data in "
            "{}".format(pi_data_to_use.metadata["netcdf-scm crunched file"])
        )

        with pytest.raises(ValueError, match=error_msg):
            self.tclass().get_reference_values(
                junk_data_normalisation, pi_data_to_use, picontrol_branch_time,
            )

    def test_normalise_against_picontrol(
        self, junk_data_normalisation, junk_data_picontrol_normalisation
    ):
        mock_ref_values = junk_data_normalisation.timeseries()
        mock_ref_values.iloc[:, :] = 1

        picontrol_branch_time = dt.datetime(2, 2, 2)  # mocked so irrelevant

        with patch.object(
            self.tclass, "get_reference_values", return_value=mock_ref_values
        ) as mock_get_reference_values:

            res = self.tclass().normalise_against_picontrol(
                junk_data_normalisation,
                junk_data_picontrol_normalisation,
                picontrol_branch_time,
            )

        mock_get_reference_values.assert_called_with(
            junk_data_normalisation,
            junk_data_picontrol_normalisation,
            picontrol_branch_time,
        )

        expected_metadata = {
            **{
                "(child) {}".format(k): v
                for k, v in junk_data_normalisation.metadata.items()
            },
            **{
                "(normalisation) {}".format(k): v
                for k, v in junk_data_picontrol_normalisation.metadata.items()
            },
        }
        expected_metadata["normalisation method"] = self.tclass().method_name

        assert res.metadata == expected_metadata

        # thanks to mocking, everything simply shifted down by 1
        pd.testing.assert_frame_equal(
            res.timeseries(),
            junk_data_normalisation.timeseries(meta=res.meta.columns) - 1,
        )

    @pytest.mark.parametrize(
        "picontrol_expt_name,error", (("esm-piControl", False), ("piC", True),)
    )
    def test_normalise_against_picontrol_name_error(
        self,
        picontrol_expt_name,
        error,
        junk_data_picontrol_normalisation,
        junk_data_normalisation,
    ):
        picontrol_branch_time = get_branch_time(junk_data_normalisation)
        tweaked_picontrol = junk_data_picontrol_normalisation.copy()
        tweaked_picontrol.metadata["experiment_id"] = picontrol_expt_name

        tweaked_picontrol = tweaked_picontrol.resample("MS")
        junk_data_normalisation = junk_data_normalisation.resample("MS")

        def call():
            self.tclass().normalise_against_picontrol(
                junk_data_normalisation, tweaked_picontrol, picontrol_branch_time,
            )

        if error:
            error_msg = re.escape(
                "If you would like to normalise against an experiment other than piControl, please raise an "
                "issue at https://gitlab.com/netcdf-scm/netcdf-scm/-/issues"
            )
            with pytest.raises(NotImplementedError, match=error_msg):
                call()

        else:
            # no error
            call()
