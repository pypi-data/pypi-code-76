from tsbase.metrics import *
import numpy as np


def comb(y_true, y_pred, metrics=None,
         pre_deal=None, pre_a=None, pre_b=None):

    n_models = None
    n_samples = len(y_true)
    if isinstance(y_pred, list):
        n_models = len(y_pred)
    if pre_a is not None and pre_b is not None:
        if pre_deal == 'std':
            y_true = re_standardize(y_true, _mean=pre_a, _std=pre_b)
            for k in range(n_models):
                value = re_standardize(y_pred[k], _mean=pre_a, _std=pre_b)
                y_pred[k] = value
    # Weights
    weights = np.zeros((n_samples, n_models), dtype=np.float)
    for t in range(n_samples):
        if t != 0:
            eval_values = list()
            for k in range(n_models):
                if metrics == 'mse':
                    eval_values.append(mean_squared_error(y_true[0:t], y_pred[k][0:t]))
                elif metrics == 'rmse':
                    eval_values.append(root_mean_squared_error(y_true[0:t], y_pred[k][0:t]))
                elif metrics == 'mae':
                    eval_values.append(mean_absolute_error(y_true[0:t], y_pred[k][0:t]))
                elif metrics == 'mape':
                    eval_values.append(mean_absolute_percentage_error(y_true[0:t], y_pred[k][0:t]))

            eval_values = np.array(eval_values)
            min_index = np.argmin(eval_values)
            max_index = np.argmax(eval_values)
            _sum = np.sum(eval_values)
            for k in range(n_models):
                if k == min_index:
                    weights[t, k] = eval_values[max_index] / _sum
                elif k == max_index:
                    weights[t, k] = eval_values[min_index] / _sum
                else:
                    weights[t, k] = 1 - (eval_values[max_index]+eval_values[min_index]) / _sum
        else:
            weights[t, :] = 1/n_models
    # Combined result
    final_pred = 0
    for k in range(n_models):
        final_pred += y_pred[k] * weights[:, k]

    return final_pred
