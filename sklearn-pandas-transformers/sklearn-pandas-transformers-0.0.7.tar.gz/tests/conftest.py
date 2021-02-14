# -*- coding: utf-8 -*-
import pandas as pd
from pytest import fixture


@fixture(scope="function")
def sample_df():
    df = pd.DataFrame([["a", "b"], [0, 1]]).T
    df.columns = ["letter", "number"]
    return df


@fixture(scope="function")
def sample_df_with_additional_column():
    df = pd.DataFrame([["a", "b"], [0, 1], [0, 1]]).T
    df.columns = ["letter", "number", "number2"]
    return df
