from behalearn.visualization import visualize_mobile_data
import pandas as pd

import pytest


@pytest.fixture
def df_touch():
    return pd.DataFrame(data={
        'input': ['touch', 'touch', 'touch', 'touch'],
        'timestamp': [17327, 17451, 17459, 17468],
        'session_id': ['a1', 'a1', 'a1', 'a1'],
        'event_type': ['down', 'move', 'move', 'up'],
        'event_type_detail': ['down', 'move', 'move', 'up'],
        'pointer_id': [0, 0, 0, 0],
        'x': [172.0, 170.0, 170.0, 169.3],
        'y': [426, 417, 414, 412],
        'pressure': [0.0039215, 0.0039216, 0.0039216, 0.003921],
        'gesture': [0, 0, 0, 0]
    })


@pytest.fixture
def df_accelerometer():
    return pd.DataFrame(data={
        'input': [
            'accelerometer',
            'accelerometer',
            'accelerometer',
            'accelerometer'],
        'timestamp': [16527, 16544, 16561, 16577],
        'session_id': ['a1', 'a1', 'a1', 'a1'],
        'x': [-0.00109, -0.00109, 0.00049, 0.00019],
        'y': [-0.023099, -0.023099, 0.0, 0.00829],
        'z': [0.03949, 0.03949, 0.078599, 0.197999]
    })


@pytest.fixture
def df_gyroscope():
    return pd.DataFrame(data={
        'input': ['gyroscope', 'gyroscope', 'gyroscope', 'gyroscope'],
        'timestamp': [16527, 16544, 16561, 16577],
        'session_id': ['a1', 'a1', 'a1', 'a1'],
        'x': [0.0, -0.0010646508, 0.00106465, 0.0],
        'y': [0.000351536, 0.0, 0.0010165, -0.0053515],
        'z': [0.0, 0.0, 0.00101561, 0.0068413]
    })


def test_visualize_mobile_data(df_touch, df_accelerometer, df_gyroscope):
    plot = visualize_mobile_data(
        df_touch,
        df_accelerometer,
        df_gyroscope,
        touch_width=400,
        touch_height=600,
        touch_resolution_width=800,
        touch_resolution_height=1200,
        acc_width=800,
        acc_height=1200,
        gyro_width=800,
        gyro_height=1200)

    assert plot.touch_width == 400
    assert plot.touch_height == 600
    assert plot.touch_resolution_width == 800
    assert plot.touch_resolution_height == 1200
    assert plot.acc_width == 800
    assert plot.acc_height == 1200
    assert plot.gyro_width == 800
    assert plot.gyro_height == 1200
