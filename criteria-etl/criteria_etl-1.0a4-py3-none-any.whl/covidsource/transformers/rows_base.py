import pandas as pd
import numpy as np
import warnings
from sklearn.base import BaseEstimator, TransformerMixin


class DropTransformer(BaseEstimator, TransformerMixin):
    """Class for the transformations of inputs into a useful
    representations for the Decision Support Platform.

    Attributes
    ----------
    drop_dict : dict of {str: list}
        contains column names as keys and a list of values that when
        observed the entire row is dropped.
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended is no memory savings need to
        be made.

    Example
    -------
    To drops rows on column 'VD2002' taking values in {15, 16, 17} on
    DataFrame `df`:
    >>>DropTransformer({'VD2002': [15, 16, 17]}).transform(df)
    """

    def __init__(self, drop_dict, copy=True):
        self.col_drop_dict = drop_dict
        self.copy = copy

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        """
        if self.copy:
            X_ = X.copy()
        else:
            X_ = X

        for colname, drop_list in self.col_drop_dict.items():
            drop_rows = X_[colname].isin(drop_list)
            X_ = X_.drop(X_[drop_rows].index)

        return X_


class AggregateTransformerMixin:
    """
    Mixin class for aggregating rows of the DataFrame using `~.groupby`,
    according to `aggregate_map`.

    Attributes
    ----------
    aggregate_map : dict of function labels -> iterable of column labels,
        all columns in the iterable are aggregated using its respective
        function. Function labels are added as suffixes for resulting
        columns to avoid name collisions.
    keep_first : iterable of column labels
        all columns referenced in this iterable are aggregated by using
        the first observation of each group. Note that `.nth(0)` is used
        and not `.first()`, implying that Nan values are retrieved if
        they correspond to the first observation per group.
    groupby_: column label or iterable of column labels,
        used as arguments for `~.groupby`.
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended is no memory savings need to
        be made.
    """

    def __init__(self, aggregate_map, keep_first, groupby_, copy=True):
        self.aggregate_map = aggregate_map
        # keep first is separated from aggregate_map because of
        # https://github.com/pandas-dev/pandas/issues/19598
        self.keep_first = keep_first
        self.groupby_ = groupby_
        self.copy = copy


    def _check_all_columns_are_present(self, X):

        # get list of all columns
        aggregated_columns = self.keep_first.copy()
        [aggregated_columns.extend(cols_list) for cols_list in \
         self.aggregate_map.values()]

        # check if there are columns nor present on `X`
        ind_agg_cols = pd.Index(aggregated_columns)
        ind_not_present_columns = ind_agg_cols.difference(X.columns)
        if len(ind_not_present_columns) > 0:
            raise ValueError(
                'The following columns are not present on `X`:\n'
                f'{ind_not_present_columns.to_list()}'
            )


    def aggregate_transform(self, X):
        if self.copy:
            X_ = X.copy()
        else:
            X_ = X
        
        self._check_all_columns_are_present(X_)

        groupped_X = X_.groupby(self.groupby_)
        agg_df_list = []

        # process keep first
        agg_df_list.append(groupped_X[self.keep_first].nth(0).add_suffix('_first'))

        for func_name, col_list in self.aggregate_map.items():
            # parse agggregate dict
            iter_agg_dict = {col: func_name for col in col_list}

            # calculate aggregated
            agg_df_list.append(groupped_X.agg(iter_agg_dict).add_suffix(f'_{func_name}'))

        ret = pd.concat(agg_df_list, axis=1).reset_index()

        return ret


class AggregateTransformer(AggregateTransformerMixin, BaseEstimator, TransformerMixin):
    """
    Class for aggregating rows of the DataFrame using `~.groupby`,
    according to `aggregate_map`.

    Attributes
    ----------
    aggregate_map : dict of function labels -> iterable of column labels,
        all columns in the iterable are aggregated using its respective
        function. Function labels are added as suffixes for resulting
        columns to avoid name collisions.
    keep_first : iterable of column labels
        all columns referenced in this iterable are aggregated by using
        the first observation of each group
    groupby_: column label or iterable of column labels,
        used as arguments for `~.groupby`.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return self.aggregate_transform(X)

