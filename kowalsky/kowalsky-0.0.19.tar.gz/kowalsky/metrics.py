from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score, f1_score, make_scorer


def rmsle(actual, pred):
    pred[pred < 0] = 0
    return mean_squared_log_error(actual, pred) ** 0.5


def rmse(actual, pred):
    return mean_squared_error(actual, pred) ** 0.5


scorers = {
    'acc': accuracy_score,
    'f1': f1_score,
    'rmse': rmse,
    'rmsle': rmsle
}


def get_scorer(name, greater_is_better=True):
    return make_scorer(scorers[name], greater_is_better=greater_is_better)


def get_score_fn(name):
    return scorers[name]
