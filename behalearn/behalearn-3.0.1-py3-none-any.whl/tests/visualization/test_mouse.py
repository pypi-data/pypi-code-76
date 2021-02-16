from behalearn.visualization import visualize_mouse_data
import pandas as pd

import pytest


@pytest.fixture
def df():
    return pd.DataFrame(data={
        'input': ['cursor', 'cursor', 'cursor'],
        'timestamp': [17327, 17451, 17459],
        'session_id': ['a1', 'a1', 'a1'],
        'event_type': ['down', 'move', 'up'],
        'x': [1, 2, 3],
        'y': [3, 2, 1],
        'button': ['left', 'left', 'left']
    })


def test_visualize_mouse_data(df):
    plot = visualize_mouse_data(
        df,
        view_mode='both_axes',
        width=800,
        height=800,
        resolution_height=500,
        resolution_width=500)

    assert plot.discrete is False
    assert plot.highlight is False
    assert plot.width == 800
    assert plot.height == 800
    assert plot.resolution_height == 500
    assert plot.resolution_width == 500
