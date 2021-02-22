import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from itertools import product


class MeanEncoder(TransformerMixin, BaseEstimator):
    """
    MeanEncoder() deals with high-cardinality features, such as ZIP codes,
    IP address, and industry codes.

    Parameters
    ----------
    cat_features: list
        A list of categorical features.
    cv: int (default=10)
        Determines the cross-validation splitting strategy.
    target_type: str {"classification", "regression"}
        Type of the target.
    weight_func: lambda (default=lambda x: 1 / (1 + np.exp(-(x-k)/f)))
        Chosen as a parametric function with tunable parameters and could be
        optimised by the characteristics of the data.
    k: int (default=2)
        Min sample leaf.
    f: float (default=1.0)
        Smoothing constant.
        
    Examples
    --------
    >>> features = ['feat1', 'feat2', 'feat3']
    >>> encoder = MeanEncoder(cat_features=features, cv=10, target_type='regression')
    >>> me_features = me.fit_transform(df[features], df["target"])

    References
    ----------
    [1] http://helios.mm.di.uoa.gr/~rouvas/ssi/sigkdd/sigkdd.vol3.1/barreca.pdf
    """
    def __init__(self,
                 cat_features,
                 cv=10,
                 target_type='classification',
                 weight_func=None,
                 k=2,
                 f=1.0):
        self.cat_features = cat_features
        self.cv = cv
        self.k = k
        self.f = f
        self.learned_stats = {}
        if target_type == 'classification':
            self.target_type = target_type
            self.target_values = []
        elif target_type == 'regression':
            self.target_type = 'regression'
            self.target_values = None
        else:
            print("Label type could only be 'classification' or 'regression'.")
        # Calculate smoothing factor: 1 / (1 + np.exp(- (counts - min_samples_leaf) / smoothing_slope))
        if isinstance(weight_func, dict):
            self.weight_func = eval(
                'lambda x: 1 / (1 + np.exp(-(x-k)/f))', dict(weight_func, np=np, k=k, f=f))
        elif callable(weight_func):
            self.weight_func = weight_func
        else:
            self.weight_func = lambda x: 1 / (1 + np.exp(-(x-k)/f))

    # For training dataset
    def fit_transform(self, X, y):
        X_new = X.copy()
        if self.target_type == 'classification':
            skf = StratifiedKFold(self.cv)
        else:
            skf = KFold(self.cv)
        # Categorical label
        if self.target_type == 'classification':
            self.target_values = sorted(set(y))
            self.learned_stats = {
                '{}_pred_{}'.format(variable, target): [] for variable, target in
                                    product(self.cat_features, self.target_values)}
            for variable, target in product(self.cat_features, self.target_values):
                nf_name = '{}_pred_{}'.format(variable, target)
                X_new.loc[:, nf_name] = np.nan
                for large_ind, small_ind in skf.split(y, y):
                    nf_large, nf_small, prior, col_avg_y = MeanEncoder.mean_encode_blended(
                        X_new.iloc[large_ind],
                        y.iloc[large_ind],
                        X_new.iloc[small_ind],
                        variable,
                        target,
                        self.weight_func)
                    X_new.iloc[small_ind, -1] = nf_small
                    self.learned_stats[nf_name].append((prior, col_avg_y))
        # Continuous label
        else:
            self.learned_stats = {
                '{}_pred'.format(variable): [] for variable in self.cat_features
            }
            for variable in self.cat_features:
                nf_name = '{}_pred'.format(variable)
                X_new.loc[:, nf_name] = np.nan
                for large_ind, small_ind in skf.split(y, y):
                    nf_large, nf_small, prior, col_avg_y = MeanEncoder.mean_encode_blended(
                        X_new.iloc[large_ind],
                        y.iloc[large_ind],
                        X_new.iloc[small_ind],
                        variable,
                        None,
                        self.weight_func)
                    X_new.iloc[small_ind, -1] = nf_small
                    self.learned_stats[nf_name].append((prior, col_avg_y))
        X_new = X_new.drop(self.cat_features, axis=1)
        X_new.columns = self.cat_features
        return X_new

    # For testing dataset
    def transform(self, X):
        X_new = X.copy()
        # Categorical label
        if self.target_type == 'classification':
            for variable, target in product(self.cat_features, self.target_values):
                nf_name = '{}_pred_{}'.format(variable, target)
                X_new[nf_name] = 0
                for prior, col_avg_y in self.learned_stats[nf_name]:
                    X_new[nf_name] += X_new[[variable]].join(
                        col_avg_y, on=variable).fillna(prior, inplace=False)[
                        nf_name]
                X_new[nf_name] /= self.cv
        # Continuous label
        else:
            for variable in self.cat_features:
                nf_name = '{}_pred'.format(variable)
                X_new[nf_name] = 0
                for prior, col_avg_y in self.learned_stats[nf_name]:
                    X_new[nf_name] += X_new[[variable]].join(
                        col_avg_y, on=variable).fillna(prior, inplace=False)[
                        nf_name]
                X_new[nf_name] /= self.cv
        X_new = X_new.drop(self.cat_features, axis=1)
        X_new.columns = self.cat_features
        return X_new

    # Prior probability and posterior probability
    @staticmethod
    def mean_encode_blended(X_train, y_train, X_test, variable, target, weight_func):
        """
        S_i represents an estimate of the probability of Y=1 given X=X_i
        """
        X_train = X_train[[variable]].copy()
        X_test = X_test[[variable]].copy()

        if target is not None:
            nf_name = '{}_pred_{}'.format(variable, target)
            X_train['pred_temp'] = (y_train == target).astype(int)
        else:
            nf_name = '{}_pred'.format(variable)
            X_train['pred_temp'] = y_train
        # prior = n_Y / n_TR
        prior = X_train['pred_temp'].mean()
        # S_i['mean'] = n_iY/n_i and S_i['beta'] = lambda(n_i)
        S_i = X_train.groupby(by=variable, axis=0)['pred_temp'].agg(mean="mean", beta="size")
        S_i['beta'] = weight_func(S_i['beta'])
        # Empirical Bayes Estimation: S_i = lambda(n_i)*n_iY/n_i + (1-lambda(n_i))*n_Y/n_TR
        S_i[nf_name] = S_i['beta'] * S_i['mean'] + (1 - S_i['beta']) * prior
        S_i.drop(['beta', 'mean'], axis=1, inplace=True)
        nf_train = X_train.join(S_i, on=variable)[nf_name].values
        nf_test = X_test.join(S_i, on=variable).fillna(prior, inplace=False)[nf_name].values
        return nf_train, nf_test, prior, S_i

    def get_params(self, deep=True):
        return {
            "cat_features": self.cat_features,
            "target_type": self.target_type,
            "cv": self.cv,
            "k": self.k,
            "f": self.f}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
