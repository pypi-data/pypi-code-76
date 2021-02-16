import numpy as np
import pandas as pd

import pytest


@pytest.fixture
def df_temporal():
    return pd.DataFrame(data={
        'timestamp': [0, 10, 30, 46, 51, 61],
        'x': [65, 69, 80, 84, 87, 93],
        'y': [530, 522, 500, 492, 484, 479],
        'z': [102, 104, 106, 107, 105, 102],
    })


@pytest.fixture
def df_vel_expected():
    return pd.DataFrame(data={
        'timestamp': [0, 10, 30, 46, 51, 61],
        'x': [65, 69, 80, 84, 87, 93],
        'y': [530, 522, 500, 492, 484, 479],
        'z': [102, 104, 106, 107, 105, 102],
        'velocity__x': [np.nan, 0.4, 0.55, 0.25, 0.6, 0.6],
        'velocity__y': [np.nan, -0.8, -1.1, -0.5, -1.6, -0.5],
        'velocity__z': [np.nan, 0.2, 0.1, 0.0625, -0.4, -0.3],
        'velocity__x_y': [np.nan, 0.894, 1.229, 0.559, 1.708, 0.781],
        'velocity__x_z': [np.nan, 0.447, 0.559, 0.257, 0.721, 0.670],
        'velocity__y_z': [np.nan, 0.824, 1.104, 0.503, 1.649, 0.583],
        'velocity__x_y_z': [np.nan, 0.916, 1.233, 0.562, 1.754, 0.836],
    })


@pytest.fixture
def df_ang_vel_expected():
    return pd.DataFrame(data={
        'timestamp': [0, 10, 30, 46, 51, 61],
        'x': [65, 69, 80, 84, 87, 93],
        'y': [530, 522, 500, 492, 484, 479],
        'z': [102, 104, 106, 107, 105, 102],
        'angular_velocity__x_y': [
            np.nan, -0.11071, -0.05535, -0.06919, -0.24240, -0.06947],
        'angular_velocity__x_z': [
            np.nan, 0.04636, 0.00899, 0.01531, -0.11760, -0.04636],
        'angular_velocity__y_z': [
            np.nan, 0.28966, 0.15254, 0.18857, -0.57932, -0.26011],
    })
