import logging

import pandas as pd
import time

from quartic_sdk.model.ModelABC import ModelABC
from quartic_sdk.utilities import constants


class SupportedModel(ModelABC):
    """
    Example Model used for testing model
    This is a valid model that can be save to quartic platfrom
    """
    def __init__(self):
        super().__init__("test_modelABC")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return pd.Series([i for i in range(input_df.shape[0])])


class ModelThatReturnsList(ModelABC):
    """
    Example Model used for testing model
    This is a valid model that can be save to quartic platfrom
    """

    def __init__(self):
        super().__init__("test_modelABC")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return [i for i in range(input_df.shape[0])]


class ModelThatReturnsNone(ModelABC):
    """
    Example Model used for testing model
    This is a valid model that can be save to quartic platfrom
    """

    def __init__(self):
        super().__init__("test_modelABC")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return pd.Series([None for i in range(input_df.shape[0])])


class ModelThatReturnsString(ModelABC):
    """
    Example Model used for testing model
    This is a invalid model whose predict function returns data of type string
    """

    def __init__(self):
        super().__init__("test_model")

    def post_transform(self, data):
        data = data.astype(str)
        return data

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        output = pd.Series([i for i in range(input_df.shape[0])])
        return self.post_transform(output)


class SlowModel(ModelABC):
    """
    Example Model used for testing model
    This is a invalid model whose predict function takes longer processing time than that is supported by Quartic
    """

    def __init__(self):
        super().__init__("test_model")

    def pre_transform(self, df):
        """
        A simple transformation that sleeps for x secs before returning same
        """
        time.sleep(constants.MAX_PREDICTION_PROCESSING_TIME + 1)
        return df

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        """
            sample prediction
        """
        self.pre_transform(input_df)
        return pd.Series([i for i in range(input_df.shape[0])])


class ModelWithLog(ModelABC):
    """
    Example Model used for testing model
    This is a invalid model whose predict function takes longer processing time than that is supported by Quartic
    """

    def __init__(self):
        super().__init__("test_model")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        """
            sample prediction
        """
        self.log.info("This is a info Log for Testing the logger")
        self.log.debug("This is a debug Log for Testing the logger")
        self.log.error("This is an error log")
        return pd.Series([i for i in range(input_df.shape[0])])


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }
