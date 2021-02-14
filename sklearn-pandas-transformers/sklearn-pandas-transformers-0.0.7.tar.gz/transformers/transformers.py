""" Custom transformers module - Compatible with sklearn Pipeline
"""
# -*- coding: utf-8 -*-
from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np
import pandas as pd


class SklearnPandasWrapper(TransformerMixin, BaseEstimator):
    """ Class used to wrap SKLEARN transformer to use them
    but keep pandas format and columns name
    """
    def __init__(self, transformer):
        # self.__class__ = type(transformer.__class__.__name__,
        #                       (self.__class__, transformer.__class__), {})
        self.__dict__ = transformer.__dict__
        self.transformer = transformer

    def fit(self, df, y=None, **fit_params):
        """fit
        """
        # pylint: disable=unused-argument
        self.transformer.fit(df, fit_params)
        return self

    def transform(self, df, **transform_params):
        """ Transform
        """
        # pylint: disable=unused-argument
        if transform_params:
            res = self.transformer.transform(df, transform_params)
        else:
            res = self.transformer.transform(df)
        res = pd.DataFrame(res, columns=df.columns)
        return res


class SimilarColumns(BaseEstimator, TransformerMixin):
    """ Ensure that similar columns are in test and train dataset.
    If a column is in test but not in train, then the column will be created in
    train dataset with missing value everywhere.

    Parameters
    ----
    None

    Attributes
    ----
    after transform return pandas dataframe with same columns name
    as in fitted dataset.
    """
    def __init__(self):
        self.col = None

    def fit(self, df, y=None, **fit_params):
        """ Fit transformer
        """
        # pylint: disable=unused-argument
        self.col = df.columns
        return self

    def transform(self, df, **transform_params):
        """ Transform / Apply transformer
        """
        # pylint: disable=unused-argument
        for col in self.col:
            if col not in df.columns:
                df[col] = np.nan
        # reorder columns
        df = df.loc[:, self.col]
        return df


class SplitXY(BaseEstimator, TransformerMixin):
    """ Transformer used to split X and Y and keep Y as attributes.

    Can be used by EstimatorWithoutYWrapper later


    Examples:

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
    """
    def __init__(self, ycol):
        self.ycol = ycol
        self.target = None

    def fit(self, df, y=None, **fit_params):
        """ Fit transformer
        """
        # pylint: disable=unused-argument
        self.target = df[self.ycol]
        return self

    def transform(self, df, **transform_params):
        """ Transform / Apply transformer
        """
        # pylint: disable=unused-argument
        if self.ycol in df.columns:
            self.target = df[self.ycol]
        return df.drop(self.ycol, axis=1, errors="ignore")


class EstimatorWithoutYWrapper(TransformerMixin, BaseEstimator):
    """ Class used to wrap SKLEARN estimator without y using another transformer
     (Most of the time using SplitXY transformer)

    Examples:

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
    """
    def __init__(self, estimator, transformer_with_target):
        # self.__class__ = type(estimator.__class__.__name__,
        #                       (self.__class__, estimator.__class__), {})
        self.__dict__ = estimator.__dict__
        self.estimator = estimator
        self.transformer_with_target = transformer_with_target

    def _target(self, y=None):
        return y if y is not None else self.transformer_with_target.target

    def fit(self, df, y=None, **fit_params):
        """fit
        """
        # pylint: disable=unused-argument
        if fit_params:
            self.estimator.fit(df, self._target(y), fit_params)
        else:
            self.estimator.fit(df, self._target(y))
        return self

    def predict_proba(self, df, **transform_params):
        """ predict proba
        """
        # pylint: disable=unused-argument
        if transform_params:
            res = self.estimator.predict_proba(df, transform_params)
        else:
            res = self.estimator.predict_proba(df)
        return res

    def predict(self, df, **transform_params):
        """ predict
        """
        # pylint: disable=unused-argument
        if transform_params:
            res = self.estimator.predict(df, transform_params)
        else:
            res = self.estimator.predict(df)
        return res

    def score(self, df, y=None, **score_params):
        """score
        """
        # pylint: disable=unused-argument
        if score_params:
            score = self.estimator.score(df, self._target(y), score_params)
        else:
            score = self.estimator.score(df, self._target(y))
        return score
