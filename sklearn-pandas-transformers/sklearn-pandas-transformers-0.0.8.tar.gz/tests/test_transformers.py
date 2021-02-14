# -*- coding: utf-8 -*-
from transformers.transformers import SimilarColumns, SklearnPandasWrapper, SplitXY, EstimatorWithoutYWrapper
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


def test_SimilarColumns(sample_df, sample_df_with_additional_column):
    """ Test SimilarCOlumns
    """
    # When columns are the same
    df = sample_df
    similar_columns = SimilarColumns()
    similar_columns.fit(df)

    transformed_df = similar_columns.transform(df)

    pd.testing.assert_frame_equal(df, transformed_df)

    # When one column more in transform
    similar_columns = SimilarColumns()
    similar_columns.fit(df)

    transformed_df =\
        similar_columns.transform(sample_df_with_additional_column)

    pd.testing.assert_frame_equal(df, transformed_df)

    # When one column less in transform

    similar_columns = SimilarColumns()
    similar_columns.fit(sample_df_with_additional_column)

    transformed_df =\
        similar_columns.transform(df)

    sample_df_with_additional_column.loc[:, "number2"] = np.nan

    pd.testing.assert_frame_equal(sample_df_with_additional_column,
                                  transformed_df)


class TestSklearnPandasWrapper:
    input_df = pd.DataFrame([[0, 1, 2], [3, 4, 5], [1, 67, 8]])
    input_df.columns = ["a", "b", "c"]

    def test_standard_scaler(self):

        standard_scaler = StandardScaler(with_std=False)
        res1 = standard_scaler.fit_transform(self.input_df)

        standard_scaler2 = SklearnPandasWrapper(StandardScaler(with_std=False))
        res2 = standard_scaler2.fit_transform(self.input_df)

        assert list(res2.columns) == list(self.input_df.columns)

        np.testing.assert_equal(res1, res2)

    def test_knn_imputer(self):

        input_df_with_missing = self.input_df
        input_df_with_missing[2, 1] = np.nan

        knn_imputer = KNNImputer(n_neighbors=10, add_indicator=True)
        res1 = knn_imputer.fit_transform(input_df_with_missing)

        knn_imputer2 = SklearnPandasWrapper(
            KNNImputer(n_neighbors=10, add_indicator=True))
        res2 = knn_imputer2.fit_transform(input_df_with_missing)

        assert list(res2.columns) == list(self.input_df.columns)

        np.testing.assert_array_equal(res1, res2)


class TestSplitXY:
    input_df = pd.DataFrame([[0, 1, 2], [3, 4, 5], [1, 67, 8]])
    input_df.columns = ["a", "b", "c"]
    input_df.iloc[2, 1] = np.nan

    def test1(self):
        spliter = SplitXY("a")

        pipe = Pipeline([
            ("imputer", SklearnPandasWrapper(KNNImputer())),
            ("spliter", spliter), ("scaler", StandardScaler()),
            ("rf",
             EstimatorWithoutYWrapper(RandomForestRegressor(random_state=45),
                                      spliter))
        ])
        pipe.fit(self.input_df)

        res = pipe.predict(self.input_df)

        np.testing.assert_array_equal(res, np.array([0.65, 2.13, 1.04]))
