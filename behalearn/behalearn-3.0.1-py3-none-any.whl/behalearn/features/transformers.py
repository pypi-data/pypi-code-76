from sklearn.base import TransformerMixin

from .extraction import extract_features


class FeatureExtractor(TransformerMixin):
    """Transformer wrapping the :func:`behalearn.features.extract_features`
    function.
    
    Parameters
    ----------
    features : list of func, (func,), (func, dict), str, (str,) or (str, dict)
        Features to extract.
    
    group_by_columns : list of strings or ``None``
        Column names to group rows in input data by.

    See Also
    --------
    behalearn.features.extract_features
    """

    def __init__(self, features, group_by_columns=None):
        self._features = features
        self._group_by_columns = group_by_columns

    def fit(self, X, y=None, **fit_params):
        """This method does nothing and merely returns the class instance.
        
        Returns
        -------
        self : object
        """
        return self

    def transform(self, X, **transform_params):
        """Apply :func:`behalearn.features.extract_features` on input samples.
        
        Parameters
        ----------
        X : :class:`pandas.DataFrame`
            Dataframe to compute feature vectors from.
        
        **transform_params : dict
            (Ignored) Additional parameters.
        
        Returns
        -------
        T : :class:`pandas.DataFrame`
            Dataframe with computed features.
        """
        return extract_features(
            X, self._features, group_by_columns=self._group_by_columns)
