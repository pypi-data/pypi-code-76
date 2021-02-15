from sklearn.base import BaseEstimator, TransformerMixin


class MergeTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer to merge two pandas Data Frames

    Attributes:
    -----------
    get_right_df : callable
        Returns the DataFrame to be used as `right` argument on `merge`
        method.
    keep_index : bool
        Whether you want to keep the same index of the input DataFrame.
        Defaults to True.
    merge_kwargs : dict
        kwargs for `merge` method. Defaults to None.
    copy: bool
        Whether to copy input on `transform` method. This option is
        recommended if memory savings need tobe made. Defaults to True
    """

    def __init__(
            self, get_right_df, keep_index=True, merge_kwargs=None, copy=True):
        if merge_kwargs is None:
            merge_kwargs = {}
        self.get_right_df = get_right_df
        self.keep_index = keep_index
        self.merge_kwargs = merge_kwargs.copy()
        self.copy = copy

    def fit(self, df):
        return self

    def transform(self, df):

        df_ = df.copy() if self.copy else df
        right_df = self.get_right_df()

        if self.keep_index:
            index_names = df_.index.names

            # handle unnamed index
            is_unnamed_index = (
                    (index_names[0] is None) and
                    (len(index_names) == 1)
            )
            index_names = ['index'] if is_unnamed_index else index_names

            # merge respecting index and `merge_kwargs`
            df_ = df_.reset_index().merge(right_df, **self.merge_kwargs
                                          ).set_index(index_names)
            if is_unnamed_index:
                df_.index.names = [None]

        else:
            df_ = df_.merge(right_df, **self.merge_kwargs)

        return df_
