import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV


def get_model_name(clf):
    return str(clf.__class__)[1:-1].split()[1][1:-1].split('.')[-1]


def cross_val_for_estimators(estimators, X, y, **cross_val_score_kwargs):

    cv_scores = []
    for est in estimators:
        current_scores = cross_val_score(est, X, y, **cross_val_score_kwargs)
        cv_scores.append(current_scores)

    n_folds = len(cv_scores[0])

    col_names = ['fold_{}'.format(i+1) for i in range(n_folds)]

    summary = pd.DataFrame(cv_scores, columns=col_names)  
    summary['cv_score_mean'] = summary.mean(axis=1)

    return summary


def prepare_Xy(X_1, X_0):

    n1 = len(X_1)
    n0 = len(X_0)

    X = X_1.append(X_0)

    y = np.concatenate((np.ones(n1), np.zeros(n0)))

    return X, y


def run_gscv(X_shuffled, y_shuffled, setup, score_func):

    result = dict()

    for method_name, method_params in setup.items():

        gs = GridSearchCV(scoring=score_func, cv=4, iid=False, **method_params)
        gs.fit(X_shuffled, y_shuffled)

        result[method_name] = gs

    return result


def gather_best_hyperparams(gscv):

    mask = gscv.cv_results_['mean_test_score'] == gscv.best_score_
    indices = np.argwhere(mask).reshape(-1)
    params = [gscv.cv_results_['params'][i] for i in indices]

    return pd.DataFrame(params)


def gather_best_scores_for_all_gscv(gscv_res):

    def count_n_with_best(gscv):
        return np.sum(gscv.cv_results_['mean_test_score'] == gscv.best_score_)

    def count_grid_size(gscv):
        return len(gscv.cv_results_['mean_test_score'])

    d = {
        'best_score': {method: gscv.best_score_ for method, gscv in gscv_res.items()},
        'n_with_best': {method: count_n_with_best(gscv) for method, gscv in gscv_res.items()},
        'grid_size': {method: count_grid_size(gscv) for method, gscv in gscv_res.items()},
    }

    df = pd.DataFrame.from_dict(d)

    df = df.sort_values(['best_score'], ascending=False)
    df['share_with_best'] = df['n_with_best'] / df['grid_size']

    return df