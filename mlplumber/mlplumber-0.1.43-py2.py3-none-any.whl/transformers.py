import numpy as np
import pandas as pd
from baikal import Step
from sklearn.base import TransformerMixin


class PandasConcat(Step):
    def __init__(self, df_out=True, name=None):
        super().__init__(name=name)
        self.df_out = df_out

    def fit(self, *args, **kwargs):
        return self

    def transform(self, Xs):
        df = pd.concat(Xs, axis=1, ignore_index=False)
        return df if self.df_out else df.values


class To2D(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, **kwargs):
        return X.reshape(-1, 1)


class AsStr(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, **kwargs):
        return X.astype(np.str)


class ToDense(TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None, **kwargs):
        return X.todense()
