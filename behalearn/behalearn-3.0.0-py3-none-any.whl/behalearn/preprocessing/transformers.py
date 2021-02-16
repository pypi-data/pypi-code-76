from sklearn.base import TransformerMixin

from .columns import calculate_angular_speed_columns
from .columns import calculate_speed_columns
from .segment import split
from .segment import split_by_counts
from .segment import split_by_start_and_end


class SegmentSplitter(TransformerMixin):
    """Transformer wrapping the :func:`behalearn.preprocessing.segment.split`
    function.
    
    Parameters
    ----------
    column_name: string
        Name of the new column to assign segment labels to.
    
    group_by : string or list of strings
        Column name(s) to group data by.
    
    criteria : list of tuples (function, function kwargs)
        Criteria containing functions and their keyword arguments used to
        determine segment labels per each row in input data.
    
    See Also
    --------
    behalearn.preprocessing.segment.split
    """

    def __init__(self, column_name, group_by, criteria):
        self._column_name = column_name
        self._group_by = group_by
        self._criteria = criteria

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Assign segment labels to the specified input data.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Input data  to assign segment labels to.
        
        **transform_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        X : :class:`pandas.DataFrame`
            Original data including a new column containing assigned labels
            (having the name ``column_name``).
        """
        X = X.copy()
        X.sort_values(by=self._group_by, kind='mergesort', inplace=True)

        segment_res = []
        for name, data in X.groupby(self._group_by):
            segment_num = split(data, self._criteria)
            segment_res.extend([f'{name}-{i}' for i in segment_num])

        X[self._column_name] = segment_res

        return X


class CountSegmentSplitter(TransformerMixin):
    """Transformer wrapping the
    :func:`behalearn.preprocessing.segment.split_by_counts` function.
    
    Parameters
    ----------
    column_name: string
        Name of the new column to assign segment labels to.
    
    segment_column_name: string
        Name of the column to be used in assigning segment labels.
    
    counts : iterable
        Percentages or counts.
    
    See Also
    --------
    behalearn.preprocessing.segment.split_by_counts
    """

    def __init__(self, column_name, segment_column_name, counts):
        self._column_name = column_name
        self._segment_column_name = segment_column_name
        self._counts = counts

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Assign segment labels to the specified input data.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Input data  to assign segment labels to.
        
        **transform_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        X : :class:`pandas.DataFrame`
            Original data including a new column containing assigned labels
            (having the name ``column_name``).
        """
        X[self._column_name] = split_by_counts(
            X[self._segment_column_name].values, self._counts)

        return X


class StartEndSegmentSplitter(TransformerMixin):
    """Transformer wrapping the
    :func:`behalearn.preprocessing.segment.split_by_start_and_end` function.
    
    Parameters
    ----------
    column_name: string
        Name of the new column to assign segment labels to.
    
    start_criterion : dict
        Beginning split criterion where a column name (key) equals to the
        specified value.
    
    end_criterion : dict
        Ending split criterion where a column name (key) equals to the
        specified value.
    
    time_threshold : float
        Threshold in the same units as the ``'timestamp'`` column in the input
        data.
    
    See Also
    --------
    behalearn.preprocessing.segment.split_by_start_and_end
    """

    def __init__(
            self,
            column_name,
            start_criterion,
            end_criterion,
            time_threshold=0):
        self._column_name = column_name
        self._start_criterion = start_criterion
        self._end_criterion = end_criterion
        self._time_threshold = time_threshold

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Assign segment labels to the specified input data.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Input data to assign segment labels to.
        
        **transform_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        X : :class:`pandas.DataFrame`
            Original data including a new column containing assigned labels
            (having the name ``column_name``).
        """
        X[self._column_name] = split_by_start_and_end(
            X,
            self._start_criterion,
            self._end_criterion,
            self._time_threshold)

        return X


class SpeedColumnsCalculator(TransformerMixin):
    """Transformer wrapping the
    :func:`behalearn.preprocessing.calculate_speed_columns` function.
    
    Parameters
    ----------
    group_by : string or list of strings
        Column name(s) to group data by.
    
    prefix : string
        Prefix of the names of the created columns.
    
    columns : list of strings
        Column names in input data used for calculating the new columns.
    
    combinations : integer or ``None``
        Combinations of columns to consider to calculate magnitudes.
    
    See Also
    --------
    behalearn.preprocessing.calculate_speed_columns
    """

    def __init__(self, group_by, prefix, columns, combinations=None):
        self._group_by = group_by
        self._prefix = prefix
        self._columns = columns
        self._combinations = combinations

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Compute features given the input data.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Data to compute features from.
        
        Returns
        -------
        X : :class:`pandas.DataFrame`, shape (n_feature_vectors, n_features)
            A dataframe containing computed features.
        """
        return X.groupby(self._group_by).apply(self._calculate_columns)

    def _calculate_columns(self, X):
        data, _ = calculate_speed_columns(
            X, self._prefix, self._columns, self._combinations)

        return data


class AngularSpeedColumnsCalculator(TransformerMixin):
    """Transformer wrapping the
    :func:`behalearn.preprocessing.calculate_angular_speed_columns` function.
    
    Parameters
    ----------
    group_by : string or list of strings
        Column name(s) to group input data by.
    
    prefix : string
        Prefix of the names of the created columns.
    
    columns : list of strings
        Column names in input data used for calculating the new columns.
    
    See Also
    --------
    behalearn.preprocessing.calculate_angular_speed_columns
    """

    def __init__(self, group_by, prefix, columns):
        self._group_by = group_by
        self._prefix = prefix
        self._columns = columns

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Compute features given the input data.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Data to compute features from.
        
        Returns
        -------
        X : :class:`pandas.DataFrame`, shape (n_feature_vectors, n_features)
            A dataframe containing computed features.
        """
        return X.groupby(self._group_by).apply(self._calculate_columns)

    def _calculate_columns(self, X):
        data, _ = calculate_angular_speed_columns(
            X, self._prefix, self._columns)

        return data
