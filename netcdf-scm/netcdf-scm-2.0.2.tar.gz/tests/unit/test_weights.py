import re
from unittest.mock import patch

import numpy as np
import pytest

from netcdf_scm.weights import (
    AreaSurfaceFractionWeightCalculator,
    InvalidWeightsError,
    get_land_weights,
    get_nh_weights,
    get_weights_for_area,
    multiply_weights,
    subtract_weights,
)


class _CubeWeightTester:
    # cube weight calculator
    cwc = None

    @pytest.mark.parametrize("inp", ["fail string", np.array([[1, 2], [3, 4]])])
    def test_get_land_mask_input_type_errors(self, test_all_cubes, inp):
        error_msg = re.escape(r"cube must be an ScmCube instance")
        masker = self.cwc(test_all_cubes)
        with pytest.raises(TypeError, match=error_msg):
            get_land_weights(masker, test_all_cubes, sftlf_cube=inp)

    def test_get_nh_mask(self, test_all_cubes):
        masker = self.cwc(test_all_cubes)
        result = get_nh_weights(masker, test_all_cubes)
        expected = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0]])

        np.testing.assert_array_equal(result, expected)

    def test_unknown_mask_error(self, test_all_cubes):
        masker = self.cwc(test_all_cubes)
        with pytest.raises(InvalidWeightsError, match="Unknown weights: junk"):
            masker.get_weights_array("junk")

        with pytest.raises(
            InvalidWeightsError, match="Unknown weights: World|AR6|junk"
        ):
            masker.get_weights_array("World|AR6|junk")

    @patch("netcdf_scm.weights.has_regionmask", False)
    def test_no_regionmask(self, test_all_cubes):
        masker = self.cwc(test_all_cubes)
        with pytest.raises(
            InvalidWeightsError,
            match="regionmask>=0.6 is not installed. Run `pip install regionmask>=0.6`",
        ):
            masker.get_weights_array("World|AR6|NZ")

    @patch(
        "netcdf_scm.weights.WEIGHTS_FUNCTIONS_WITHOUT_AREA_WEIGHTING",
        {
            "All zero": multiply_weights(
                get_weights_for_area(0, 220, 30, 250), "World|Land"
            ),
            "World|Land": get_land_weights,
            "Inverse": subtract_weights("All zero", 1),
        },
    )
    def test_no_match_error(self, test_all_cubes):
        tmask_name = "All zero"

        error_msg = re.escape(
            r"All weights are zero for region: `{}`".format(tmask_name)
        )
        weighter = self.cwc(test_all_cubes)
        for i in range(3):  # make sure multiple asks still raises
            # should be accessible without issue
            weighter.get_weights_array("World|Land")
            with pytest.raises(InvalidWeightsError, match=error_msg):
                weighter.get_weights_array(tmask_name)

            # should be able to get inverse without problem
            res = weighter.get_weights_array("Inverse")
            # inverse of Junk should all be non-zero
            assert not np.isclose(res, 0).any()


class TestAreaSurfaceFractionWeightCalculator(_CubeWeightTester):
    cwc = AreaSurfaceFractionWeightCalculator
