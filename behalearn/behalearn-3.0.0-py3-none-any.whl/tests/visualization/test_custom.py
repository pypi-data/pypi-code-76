from behalearn.visualization import visualize_custom_data
import pandas as pd

import pytest


@pytest.fixture
def df():
    return pd.DataFrame(data={
        'input': ['custom', 'custom', 'custom'],
        'timestamp': [17327, 25146, 45796],
        'session_id': ['a1', 'a1', 'a1'],
        'x': [124, 147, 195],
        'y': [252, 454, 751],
        'html_element': ['h1', 'p', 'div'],
    })


def test_visualize_custom_data_both_axes(df):
    plot = visualize_custom_data(
        df,
        view_mode='both_axes',
        x_columns=['x'],
        y_columns=['y'],
        width=800,
        height=800,
        title='Test title',
        x_axis_label='x',
        y_axis_label='y')

    assert plot.plot_width == 800
    assert plot.plot_height == 800


def test_visualize_custom_data_time_axis(df):
    plot = visualize_custom_data(
        df,
        view_mode='time_axis',
        x_columns=['timestamp'],
        y_columns=['y'],
        width=800,
        height=800,
        title='Test title',
        x_axis_label='x',
        y_axis_label='y')

    assert plot.plot_width == 800
    assert plot.plot_height == 800
