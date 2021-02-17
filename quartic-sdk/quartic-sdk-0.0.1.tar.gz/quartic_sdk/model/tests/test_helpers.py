import sys
from unittest import TestCase
import pandas as pd

from quartic_sdk.exceptions import InvalidPredictionException
from quartic_sdk.model.helpers import Validation
from quartic_sdk.model.tests import ModelThatReturnsString, SlowModel


class TestModelValidations(TestCase):

    def test_validate_prediction_output(self):
        with self.assertRaises(InvalidPredictionException):
            Validation.validate_prediction_output("test output")
            Validation.validate_prediction_output(pd.Series())
            Validation.validate_prediction_output(pd.Series([None, None]))
            Validation.validate_prediction_output(pd.Series(["A", "B"]))
            Validation.validate_prediction_output(pd.Series([False, True]))
            Validation.validate_prediction_output(pd.Series([1, "A", True]))
        Validation.validate_prediction_output(pd.Series([1, 2]))
        Validation.validate_prediction_output(pd.Series([1, 2.0]))
        Validation.validate_prediction_output(pd.Series([sys.float_info.min,
                                                         sys.float_info.max, 1, 2]))

    def test_validate_model(self):
        with self.assertRaises(InvalidPredictionException):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validation.validate_model(ModelThatReturnsString(), pd.DataFrame(data=data))

        with self.assertRaises(InvalidPredictionException):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validation.validate_model(SlowModel(), pd.DataFrame(data=data))


