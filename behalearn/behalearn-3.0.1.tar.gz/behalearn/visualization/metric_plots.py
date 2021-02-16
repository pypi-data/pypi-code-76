from bokeh.io import show
from bokeh.plotting import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import HoverTool
import numpy as np

from behalearn.config import config
from behalearn.metrics import fmr_score
from behalearn.metrics import fnmr_score
from behalearn.metrics import tpr_score
from behalearn.metrics import eer_score


def plot_fmr_fnmr(data, thresholds=None):
    """Plot the values of FMR, FNMR and EER for each user the specified
    dataframe was trained for.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing the following columns: ``'user'``, ``'proba1'``
        and ``'y_test'``.
    
    thresholds : array-like or ``None``
        Threshold values (prediction scores). If ``None``, the thresholds are
        derived from the ``'proba1'`` column in ``data``.
    """
    users = data[config['column_user']].unique()
    thresholds = _get_thresholds(thresholds, data)
    plt = None

    for user in users:
        fmrs = []
        fnmrs = []
        user_data = data[data[config['column_user']] == user]
        for threshold in thresholds:
            y_pred_thr = user_data[config['column_proba_1']].apply(
                lambda x: 1 if x > threshold else 0)
            fmrs.append(
                fmr_score(user_data[config['column_y_test']], y_pred_thr))
            fnmrs.append(fnmr_score(
                user_data[config['column_y_test']], y_pred_thr))
        eer_thr, eer = eer_score(thresholds, fmrs, fnmrs)

        plt = figure(
            tools='pan,box_zoom,reset,save',
            x_axis_label=config['visualization_metrics_threshold'],
            y_axis_label=config['visualization_metrics_error_rate'])

        curve_data_source = ColumnDataSource(data={
            'threshold': thresholds,
            'fmr': fmrs,
            'fnmr': fnmrs,
        })

        eer_data_source = ColumnDataSource(data={
            'eer_thr': [eer_thr],
            'eer': [eer],
        })

        hover = HoverTool(names=['fmr', 'fnmr'], tooltips=[
            (config['visualization_metrics_threshold'], '@threshold'),
            (config['visualization_metrics_fmr'],
             _get_percentage_tooltip('fmr')),
            (config['visualization_metrics_fnmr'],
             _get_percentage_tooltip('fnmr')),
        ])

        hover_eer = HoverTool(names=['eer'], tooltips=[
            (config['visualization_metrics_threshold'], '@eer_thr'),
            (config['visualization_metrics_eer'],
             _get_percentage_tooltip('eer')),
        ])

        plt.add_tools(hover)
        plt.add_tools(hover_eer)

        plt.line(
            'threshold',
            'fmr',
            name='fmr',
            line_color='red',
            legend_label=config['visualization_metrics_fmr'],
            source=curve_data_source)
        plt.line(
            'threshold',
            'fnmr',
            name='fnmr',
            line_color='blue',
            legend_label=config['visualization_metrics_fnmr'],
            source=curve_data_source)
        plt.circle(
            'eer_thr',
            'eer',
            name='eer',
            fill_color='green',
            size=10,
            legend_label=config['visualization_metrics_eer'],
            source=eer_data_source)

    if plt is not None:
        show(plt)


def plot_det(data, thresholds=None, scale_log=False):
    """Plot the detection error trade-off (DET) curve along with the equal
    error rate (EER) for each user the specified dataframe was trained for.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing the following columns: ``'user'``, ``'proba1'``
        and ``'y_test'``.
    
    thresholds : array-like or ``None``
        Threshold values (prediction scores). If ``None``, the thresholds are
        derived from the ``'proba1'`` column in ``data``.
    
    scale_log : boolean
        If ``True``, use a logarithmic scale. If ``False``, use a linear scale.
    """
    users = data[config['column_user']].unique()
    thresholds = _get_thresholds(thresholds, data)
    plt = None

    for user in users:
        fmrs = []
        fnmrs = []
        user_data = data[data[config['column_user']] == user]
        for threshold in thresholds:
            y_pred_thr = user_data[config['column_proba_1']].apply(
                lambda x: 1 if x > threshold else 0)
            fmrs.append(
                fmr_score(user_data[config['column_y_test']], y_pred_thr))
            fnmrs.append(
                fnmr_score(user_data[config['column_y_test']], y_pred_thr))
        eer_thr, eer = eer_score(thresholds, fmrs, fnmrs)

        if (scale_log):
            plt = figure(
                tools='pan,box_zoom,reset,save',
                x_axis_type='log',
                y_axis_type='log',
                x_axis_label=config['visualization_metrics_fmr_full'],
                y_axis_label=config['visualization_metrics_fnmr_full'])
        else:
            plt = figure(
                tools='pan,box_zoom,reset,save',
                x_axis_label=config['visualization_metrics_fmr_full'],
                y_axis_label=config['visualization_metrics_fnmr_full'])
            plt.line([0, 1], [0, 1], line_dash=[1, 5], line_color='gray')

        curve_data_source = ColumnDataSource(data={
            'threshold': thresholds,
            'fmr': fmrs,
            'fnmr': fnmrs,
        })

        eer_data_source = ColumnDataSource(data={
            'eer_thr': [eer_thr],
            'eer': [eer],
        })

        hover = HoverTool(names=['fmr'], tooltips=[
            (config['visualization_metrics_threshold'], '@threshold'),
            (config['visualization_metrics_fmr'],
             _get_percentage_tooltip('fmr')),
            (config['visualization_metrics_fnmr'],
             _get_percentage_tooltip('fnmr')),
        ])

        hover_eer = HoverTool(names=['eer'], tooltips=[
            (config['visualization_metrics_threshold'], '@eer_thr'),
            (config['visualization_metrics_eer'],
             _get_percentage_tooltip('eer')),
        ])

        plt.add_tools(hover)
        plt.add_tools(hover_eer)

        plt.line(
            'fmr',
            'fnmr',
            name='fmr',
            line_color='red',
            legend_label=config['visualization_metrics_det'],
            source=curve_data_source)
        plt.circle(
            'eer',
            'eer',
            name='eer',
            fill_color='green',
            size=10,
            legend_label=config['visualization_metrics_eer'],
            source=eer_data_source)

    if plt is not None:
        show(plt)


def plot_roc(data, thresholds=None):
    """Plot the receiver operating characteristic (ROC) curve along with the
    EER for each user the specified dataframe was trained for.

    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Dataframe containing the following columns: ``'user'``, ``'proba1'``
        and ``'y_test'``.
    
    thresholds : array-like or ``None``
        Threshold values (prediction scores). If ``None``, the thresholds are
        derived from the ``'proba1'`` column in ``data``.
    """
    users = data[config['column_user']].unique()
    thresholds = _get_thresholds(thresholds, data)
    plt = None

    for user in users:
        true_positive_rates = []
        false_match_rates = []
        user_data = data[data[config['column_user']] == user]
        for threshold in thresholds:
            y_pred_thr = user_data[config['column_proba_1']].apply(
                lambda x: 1 if x > threshold else 0)
            true_positive_rates.append(
                tpr_score(user_data[config['column_y_test']], y_pred_thr))
            false_match_rates.append(
                fmr_score(user_data[config['column_y_test']], y_pred_thr))

        plt = figure(
            tools='pan,box_zoom,reset,save',
            x_axis_label=config['visualization_metrics_fmr_full'],
            y_axis_label=config['visualization_metrics_tpr_full'])

        curve_data_source = ColumnDataSource(data={
            'threshold': thresholds,
            'fmr': false_match_rates,
            'tpr': true_positive_rates,
        })

        hover = HoverTool(tooltips=[
            (config['visualization_metrics_threshold'], '@threshold'),
            (config['visualization_metrics_fmr'],
             _get_percentage_tooltip('fmr')),
            (config['visualization_metrics_tpr'],
             _get_percentage_tooltip('tpr')),
        ])

        plt.add_tools(hover)

        plt.line(
            'fmr',
            'tpr',
            line_color='blue',
            legend_label=config['visualization_metrics_roc'],
            source=curve_data_source)

    if plt is not None:
        show(plt)


def _get_percentage_tooltip(metric):
    return '@{}{{0.{}%}}'.format(
        metric, '0' * config['visualization_accuracy_metrics'])


def _get_thresholds(thresholds, data):
    if thresholds is not None:
        return thresholds.unique()
    else:
        data_thresholds = np.unique(data['proba1'].values)
        data_thresholds.sort()
        return data_thresholds
