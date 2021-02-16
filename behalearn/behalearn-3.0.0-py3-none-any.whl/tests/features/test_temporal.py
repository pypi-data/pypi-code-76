import numpy as np
import pandas as pd

import pytest
from pandas.testing import assert_frame_equal

from behalearn.features import temporal


@pytest.fixture
def df_acc_expected():
    return pd.DataFrame(data={
        'acceleration__x': [
            np.nan, np.nan, 0.0075, -0.01875, 0.070, 0.0],
        'acceleration__y': [
            np.nan, np.nan, -0.015, 0.0375, -0.22, 0.11],
        'acceleration__z': [
            np.nan, np.nan, -0.005, -0.00234375, -0.0925, 0.01],
        'acceleration__x_y': [
            np.nan, np.nan, 0.01675, -0.041875, 0.2298, -0.0927],
        'acceleration__x_z': [
            np.nan, np.nan, 0.0055901, -0.018875, 0.0928, -0.00502],
        'acceleration__y_z': [
            np.nan, np.nan, 0.014, -0.0375625, 0.2292, -0.1066],
        'acceleration__x_y_z': [
            np.nan, np.nan, 0.01585, -0.0419375, 0.2384, -0.0918],
    })


@pytest.fixture
def df_jerk_expected():
    return pd.DataFrame(data={
        'jerk__x': [
            np.nan, np.nan, np.nan, -0.00164, 0.01775, -0.007],
        'jerk__y': [
            np.nan, np.nan, np.nan, 0.00328125, -0.0515, 0.033],
        'jerk__z': [
            np.nan, np.nan, np.nan, 0.000166015625, -0.018, 0.01025],
        'jerk__x_y': [
            np.nan, np.nan, np.nan, -0.0036640625, 0.054335, -0.03225],
        'jerk__x_z': [
            np.nan, np.nan, np.nan, -0.0015296875, 0.022335, -0.00979],
        'jerk__y_z': [
            np.nan, np.nan, np.nan, -0.00322265625, 0.0533525, -0.03358],
        'jerk__x_y_z': [
            np.nan, np.nan, np.nan, -0.00361171875, 0.0560675, -0.03302],
    })


@pytest.fixture
def df_ang_acc_expected():
    return pd.DataFrame(data={
        'angular_acceleration__x_y': [
            np.nan, np.nan, 0.002768, -0.000865, -0.034642, 0.017293],
        'angular_acceleration__x_z': [
            np.nan, np.nan, -0.0018685, 0.000395, -0.026582, 0.007124],
        'angular_acceleration__y_z': [
            np.nan, np.nan, -0.006856, 0.002251875, -0.153578, 0.031921],
    })


def test_acceleration(df_temporal, df_acc_expected):
    df_acc = temporal.acceleration(df_temporal, ['x', 'y', 'z'])

    assert_frame_equal(df_acc, df_acc_expected, check_less_precise=2)


def test_jerk(df_temporal, df_jerk_expected):
    df_jerk = temporal.jerk(df_temporal, ['x', 'y', 'z'])

    assert_frame_equal(df_jerk, df_jerk_expected, check_less_precise=2)


def test_angular_acceleration(df_temporal, df_ang_acc_expected):
    df_ang_acc = temporal.angular_acceleration(df_temporal, ['x', 'y', 'z'])

    assert_frame_equal(df_ang_acc, df_ang_acc_expected, check_less_precise=2)
