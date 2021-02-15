import numpy as np
import warnings
from sklearn.base import BaseEstimator, TransformerMixin


class ReplaceTransformer(BaseEstimator, TransformerMixin):
    """Class for the transformations of inputs into a useful representations 
    for the Decision Support Platform.

    Attributes
    ----------
    names_map : dict of {str: dict}
        Contains column names as keys and values are dict's to be used
        as `pd.Series.map` argument.
    method : str in {'replace', 'map'}
        If set to 'replace', use the pandas replace method. If set to 
        'map', use pandas map method. The latter implies that values 
        which are not mapped, take `nan` as value.
    astype_dict : dict of {column_label: dtype}
        Indicates which are the column types of a user defined subset of
        columns.
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended if no memory savings need to
        be made.
    """
    allowed_methods = ['replace', 'map']

    def __init__(self, names_map, method='replace', astype_dict=None, copy=True):
        self.names_map = names_map
        assert method in self.allowed_methods, "`method` should take values " +\
        f"in {self.allowed_methods}"
        self.method = method
        self.astype_dict = astype_dict
        self.copy = copy

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        """
        # copy
        if self.copy:
            X_ = X.copy()
        else:
            X_ = X
        
        if self.method == 'map':
            for colname, map_dict in self.names_map.items():
    
                X_[colname] = X_[colname].map(map_dict)
        else:
            X_.replace(self.names_map, inplace=True)

        if not self.astype_dict is None:

            X_ = X_.astype(self.astype_dict)

        return X_


class NameTransformer(BaseEstimator, TransformerMixin):
    """Class used to select and rename the columns of a DataFrame.

    Attributes
    ----------
    names_map : dict
        Defines how columns are renamed
    keep_features : list or bool
        If list, indicates columns which are kept with the original
        name. If True, keeps all columns and if False, keep only renamed
        columns defined in `names_map`.
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended if no memory savings need to
        be made.
    """

    def __init__(self, names_map, keep_features, copy=True):

        if isinstance(keep_features, list):
            intersection_ = set(names_map.keys()).intersection(keep_features)
            assert len(intersection_) == 0, \
                f"""The following columns are defined both in `keep_features` as in `names_map.keys()`:
                {intersection_}
                """

        self.names_map = names_map
        self.keep_features = keep_features
        self.copy = copy

    def fit(self, X, y=None):

        return self

    def transform(self, X, y=None):
        """
        Transform dataset.
        Parameters
        ----------
        X : pandas DataFrame, shape=(n_samples, n_features)
            Input data to be transformed. Use ``dtype=np.float32`` for maximum
            efficiency.
        Returns
        -------
        X_transformed : pandas DataFrame, shape=(n_samples, n_out)
            Transformed dataset.
        """
        # if `keep_features` is list, keep only renamed and listed columns
        if isinstance(self.keep_features, list):
            if self.copy:
                X_ = X[list(self.names_map.keys()) + self.keep_features].copy()
            else:
                X_ = X[list(self.names_map.keys()) + self.keep_features]

        elif isinstance(self.keep_features, bool):
            # if `keep_features` is False, keep only renamed variables
            if not self.keep_features:
                if self.copy:
                    X_ = X[list(self.names_map.keys())].copy()
                else:
                    X_ = X[list(self.names_map.keys())]
            # if `keep_features` is True, keep all variables
            else:
                X_ = X.copy() if self.copy else X

        else:
            X_ = None

        X_ = X_.rename(self.names_map, axis=1)

        return X_


class AssignTransformer(BaseEstimator, TransformerMixin):
    """Class for applying `DataFrame.assign`, using a dict as
    unique parameter

    Attributes
    ----------
    assign_map : dict of {colname: udf},
        Its keys will  define the names of the generated columns. Its
        values are callables which must return a Series which is used as
        the new column.
    NOTE: `udf` must never modify input DataFrame. Pandas does not
    check this!
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended if no memory savings need to
        be made.
    Example
    -------
    To generate a new column called `'half_x'`to `df`, which is defined
    as half of its float column `'x'`:
    >>>AssignTransformer({'half_x': lambda df: df['x'] / 2}).transform(
    ...    df)
    """
    def __init__(self, assign_map, copy=True):

        self.assign_map = assign_map
        self.copy = copy

    def _assign_transform(self, X):

        # copy
        if self.copy:
            X_ = X.copy()
        else:
            X_ = X

        return X_.assign(**self.assign_map)

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        # apply transform method
        return self._assign_transform(X)


class SelectTransformer(BaseEstimator, TransformerMixin):
    """
    Class for applying `np.select` to DataFrames, using a dict as
    unique parameter

    Attributes
    ----------
    select_map: dict of {colname: dict of {`condlist`: `choicelist`}}
        where `condlist` and `choicelist` are the arguments of
        `np.select`. For setting `default` argument of `np.select`
         use the specific key `'default'` within the internal dict.
    copy: bool
        Whether to copy input on `transform` method. Will default to
        True and this option is recommended if no memory savings need to
        be made.
    Example
    -------
    To generate a new column called `'case_x'`to `df`, which is defined
    as `x / 2` when x is greater than 1, as `x ** 2` when it is smaller
    than `0.5` and as `1` otherwise:
    >>>SelectTransformer({'case_x': {
    ...    lambda df: df['x'] > 1: lambda df: df['x'] / 2,
    ...    lambda df: df['x'] < 0.5: lambda df: df['x'] ** 2,
    ...    'default': 1
    ...}}).transform(df)
    """

    def __init__(self, select_map, copy=True):

        self.select_map = select_map
        self.copy = copy

    def _select_transform(self, X):

        # copy
        if self.copy:
            X_ = X.copy()
        else:
            X_ = X

        for col_name, cond_choice_dict in self.select_map.items():

            # initialize np.select arguments
            default_value = cond_choice_dict.get('default', 0)
            default_value = default_value(X_) if callable(default_value) else default_value
            cond_list = []
            choice_list = []

            for cond, choice in cond_choice_dict.items():

                if cond != 'default':
                    # collect conditions and choices
                    cond_list.append(cond(X_) if callable(cond) else cond)
                    choice_list.append(choice(X_) if callable(
                        choice) else choice)

            # insert new column
            X_.loc[:, col_name] = np.select(cond_list, choice_list,
                                            default=default_value)

        return X_

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        # apply transform method
        return self._select_transform(X)