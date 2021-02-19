# Create class for creating a regression report later (inspired by sklearn/classification_report)
from collections import Callable

import numpy as np
import pandas as pd
from sklearn.metrics import (
    explained_variance_score,
    max_error,
    mean_absolute_error,
    mean_squared_error,
    mean_squared_log_error,
    median_absolute_error,
    r2_score,
    mean_poisson_deviance,
    mean_gamma_deviance,
    mean_tweedie_deviance,
)
import plotly.express as px
from io import StringIO


class Metrics:
    def __init__(self, drop_zeros=False):
        """A collection of regression metrics
        Args:
            drop_zeros: If true drop any zeros in y_true and the corresponding value in y_pred for percentage based
             metrics
        """
        self._drop_zeros = drop_zeros

    def calculate_all(self, y_true, y_pred):
        _computed_metrics = {}
        valid_class_functions = [
            x for x in dir(self) if x != "calculate_all" and not x.startswith("_") and "__" not in x and
            isinstance(getattr(self, x), Callable)
        ]
        for class_attribute in valid_class_functions:
            metric_name, metric_value = class_attribute, float("NaN")
            try:
                metric_value = getattr(self, class_attribute)(y_true, y_pred)
            except Exception:
                pass
            _computed_metrics[metric_name] = metric_value
        return _computed_metrics

    def residual_sum_of_squares(self, y_true, y_pred):
        rss = np.sum(np.square(y_true - y_pred))
        return rss

    def mean_squared_error(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        return mse

    def mean_squared_percentage_error(self, y_true, y_pred):
        idx = np.s_[:]
        if self._drop_zeros:
            idx = y_true != 0
        y, y_hat = y_true[idx], y_pred[idx]
        mspe = np.mean(np.divide(np.square(y - y_hat), np.square(y)))
        return mspe

    def root_mean_square_error(self, y_true, y_pred):
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        return rmse

    def root_mean_square_percentage_error(self, y_true, y_pred):
        idx = np.s_[:]
        if self._drop_zeros:
            idx = y_true != 0
        y, y_hat = y_true[idx], y_pred[idx]
        rmspe = np.square(np.mean(np.divide(np.square(y - y_hat), np.square(y))))
        return rmspe

    def mean_absolute_error(self, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        return mae

    def mean_absolute_percentage_error(self, y_true, y_pred):
        idx = np.s_[:]
        if self._drop_zeros:
            idx = y_true != 0
        y, y_hat = y_true[idx], y_pred[idx]
        mape = np.mean(np.abs(np.divide((y - y_hat), y)))
        return mape

    def relative_squared_error(self, y_true, y_pred):
        rse = np.divide(np.sum(np.square(y_true - y_pred)),
                        np.sum(np.square(y_true - np.mean(y_true))))
        return rse

    def relative_absolute_error(self, y_true, y_pred):
        rae = np.divide(np.sum(np.abs(y_true - y_pred)),
                        np.sum(np.abs(y_true - np.mean(y_true))))
        return rae

    def r2_score(self, y_true, y_pred):
        # Coefficient of determination
        r2 = r2_score(y_true, y_pred)
        return r2

    def explained_variance_score(self, y_true, y_pred):
        return explained_variance_score(y_true, y_pred)

    def max_error(self, y_true, y_pred):
        return max_error(y_true, y_pred)

    def min_error(self, y_true, y_pred):
        return np.min(np.abs(y_true - y_pred))

    def mean_squared_log_error(self, y_true, y_pred):
        return mean_squared_log_error(y_true, y_pred)

    def median_absolute_error(self, y_true, y_pred):
        return median_absolute_error(y_true, y_pred)

    def mean_poisson_deviance(self, y_true, y_pred):
        return mean_poisson_deviance(y_true, y_pred)

    def mean_gamma_deviance(self, y_true, y_pred):
        return mean_gamma_deviance(y_true, y_pred)

    def mean_tweedie_deviance(self, y_true, y_pred):
        return mean_tweedie_deviance(y_true, y_pred)


class RegressionReport:
    """Generate regression report for two arrays similar to sklearn classification report

    Examples:
        To run a report, plot and get specific metrics

        >>> report = RegressionReport(np.array([0.5, 1.0]), np.array([1.0, 0.5]))  # generate report for two arrays
        >>> fig = report.plot()  # plot using plotly express
        >>> report.print()  # print(report)
        Regression Report:
                 explained_variance_score:               -3.000
                                max_error:                0.500
                      mean_absolute_error:                0.500
           mean_absolute_percentage_error:                0.750
                      mean_gamma_deviance:                0.500
                    mean_poisson_deviance:                0.347
                       mean_squared_error:                0.250
                   mean_squared_log_error:                0.083
            mean_squared_percentage_error:                0.625
                    mean_tweedie_deviance:                0.250
                    median_absolute_error:                0.500
                                min_error:                0.500
                                 r2_score:               -3.000
                  relative_absolute_error:                2.000
                   relative_squared_error:                4.000
                  residual_sum_of_squares:                0.500
                   root_mean_square_error:                0.500
        root_mean_square_percentage_error:                0.391
        Percentiles:
                                        5:               -0.450
                                       25:               -0.250
                                       50:                0.000
                                       75:                0.250
                                       95:                0.450
        >>> r2 = report["r2_score"]  # get specific metric
        -3.000
    """

    def __init__(self, y_true, y_pred, drop_zeros=False, baselines=False):
        """

        Args:
            y_true: 1d np.array of actual y values example=np.array([1,2,3,4,5])
            y_pred: 1d np.array of predicted y values example=np.array([1,2,3,4,5])
            drop_zeros: If true drop any zeros in y_true and the corresponding value in y_pred for percentage based
             metrics
            baselines: If True RegressionReport will include the metrics using predictions as the last known value. If
             int then will use last (+ve int) or future known (-ve int) to calculate baseline achievable accuracy.
        """
        self._y_true, self._y_pred = self._check_arrays(y_true, y_pred)

        # Some forecasting models drop zeros https://ideas.repec.org/a/for/ijafaa/y2006i4p32-35.html
        metrics = Metrics(drop_zeros=drop_zeros)

        self._computed_metrics = metrics.calculate_all(self._y_true, self._y_pred)
        self._baselines = bool(baselines)
        self._baseline_metrics = None
        if self._baselines:
            shift_by = int(baselines)
            self._baseline_pred = self._shift_array(self._y_true, shift_by=shift_by, fill_value=None)
            self._baseline_metrics = metrics.calculate_all(self._y_true, self._baseline_pred)

    @staticmethod
    def _check_arrays(y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        return y_true, y_pred

    def __str__(self):
        report_str = []
        fmt_string = "{:>" + str(max([len(x) for x in self._computed_metrics.keys()])) + "s}: {: >20.3f}"
        if self._baselines:
            fmt_string += " ({:.3f})"
        report_str.append('Regression Report:')
        error_metrics = []

        for metric_name, metric_value in self._computed_metrics.items():
            if self._baselines:
                report_str.append(fmt_string.format(metric_name, metric_value, self._baseline_metrics[metric_name]))
            else:
                report_str.append(fmt_string.format(metric_name, metric_value))
            if metric_value == float("NaN"):
                error_metrics.append(metric_name)

        report_str.append('\nPercentiles:')
        percentile = [5, 25, 50, 75, 95]
        percentile_value = np.percentile(self._y_true - self._y_pred, percentile)
        baseline_percentile_value = np.empty_like(percentile_value)
        if self._baselines:
            baseline_percentile_value = np.percentile(self._y_true - self._baseline_pred, percentile)
        for p, pv, blv in zip(percentile, percentile_value, baseline_percentile_value):
            if self._baselines:
                report_str.append(fmt_string.format(str(p), pv, blv))
            else:
                report_str.append(fmt_string.format(str(p), pv))
        if len(error_metrics):
            report_str.append("\nCould not compute: {}".format(len(error_metrics), ", ".join(error_metrics)))
        return '\n'.join(report_str)

    def __repr__(self):
        return self.__str__()

    def print(self):
        print(self)

    def __getitem__(self, item):
        return self._computed_metrics[item]

    def plot(self, target_name=None, show=True):
        labels = ["y (Truth)", "ŷ (Prediction)"]
        title = "Ground Truth vs Predictions"
        yaxis_title = ""
        if target_name:
            target_name = target_name + (" " * (not target_name.endswith(" ")))
            labels = [target_name + x for x in labels]
            title = target_name + title
            yaxis_title = target_name
        labels = ["Time Index"] + labels
        data_array = [np.arange(len(self._y_true)), self._y_true, self._y_pred]
        if self._baselines:
            labels.append("y (Baseline)")
            data_array.append(self._baseline_pred)
        df = pd.DataFrame(dict(zip(labels, data_array)))
        fig = px.line(df, x=labels[0], y=labels[1:], title=title)
        fig.update_layout(yaxis_title=yaxis_title)
        if show:
            fig.show()
        return fig

    @staticmethod
    def _shift_array(data, shift_by, fill_value=None):
        """Shift array by n values, fill with first known value if fill_value is None"""
        result = np.empty_like(data)
        if shift_by > 0:
            if fill_value is None:
                fill_value = data[:-shift_by][0]
            result[:shift_by] = fill_value
            result[shift_by:] = data[:-shift_by]
        elif shift_by < 0:
            if fill_value is None:
                fill_value = data[-shift_by:][0]
            result[shift_by:] = fill_value
            result[:shift_by] = data[-shift_by:]
        else:
            result[:] = data
        return result
