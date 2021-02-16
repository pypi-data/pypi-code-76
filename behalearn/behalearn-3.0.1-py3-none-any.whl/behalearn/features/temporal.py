from behalearn.config import config
from behalearn.preprocessing.columns import calculate_angular_speed_columns
from behalearn.preprocessing.columns import calculate_speed_columns


def velocity(data, columns, combinations=None):
    data, new_columns = calculate_speed_columns(
        data,
        prefix=config['features_velocity'],
        columns=columns,
        combinations=combinations)

    return data.loc[:, new_columns]


def acceleration(data, columns, combinations=None):
    data, velocity_columns = calculate_speed_columns(
        data,
        prefix=config['features_velocity'],
        columns=columns,
        combinations=combinations,
        return_as_components=True)

    data, acceleration_columns = calculate_speed_columns(
        data,
        prefix=config['features_acceleration'],
        columns=velocity_columns,
        combinations=1)

    return data.loc[:, acceleration_columns]


def jerk(data, columns, combinations=None):
    data, velocity_columns = calculate_speed_columns(
        data,
        prefix=config['features_velocity'],
        columns=columns,
        combinations=combinations,
        return_as_components=True)

    data, acceleration_columns = calculate_speed_columns(
        data,
        prefix=config['features_acceleration'],
        columns=velocity_columns,
        combinations=1,
        return_as_components=True)

    data, jerk_columns = calculate_speed_columns(
        data,
        prefix=config['features_jerk'],
        columns=acceleration_columns,
        combinations=1)

    return data.loc[:, jerk_columns]


def angular_velocity(data, columns):
    data, new_columns = calculate_angular_speed_columns(
        data,
        prefix=config['features_angular_velocity'],
        columns=columns)

    return data.loc[:, new_columns]


def angular_acceleration(data, columns):
    data, angular_velocity_columns = calculate_angular_speed_columns(
        data,
        prefix=config['features_angular_velocity'],
        columns=columns,
        return_as_components=True)

    data, angular_acceleration_columns = calculate_speed_columns(
        data,
        prefix=config['features_angular_acceleration'],
        columns=angular_velocity_columns,
        combinations=1)

    return data.loc[:, angular_acceleration_columns]
