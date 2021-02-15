import numpy as np
from logger import logger
from ...utils import check_sequence

def get_points_mean(points: np.ndarray) -> np.ndarray:
    return np.mean(points, axis=0)

def get_points_std(points: np.ndarray) -> np.ndarray:
    return np.std(points, axis=0)

def normalize_points(points: np.ndarray, points_mean: np.ndarray, points_std: np.ndarray) -> np.ndarray:
    return np.divide((points - points_mean), points_std)

def get_points_stats(points: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    points_mean = get_points_mean(points)
    points_std = get_points_std(points)
    points_norm = normalize_points(
        points=points,
        points_mean=points_mean,
        points_std=points_std
    )
    return points_mean, points_std, points_norm

def unnormalize_points(points_norm: np.ndarray, points_mean: np.ndarray, points_std: np.ndarray) -> np.ndarray:
    return np.multiply(points_norm, points_std) + points_mean

def center_points(points: np.ndarray, center_point_index: int) -> (np.ndarray, np.ndarray):
    center_point = points[center_point_index]
    result = points.copy()
    for point in result:
        point -= center_point
    return center_point, result

def uncenter_points(points: np.ndarray, center_point: np.ndarray) -> np.ndarray:
    result = points.copy()
    for point in result:
        point += center_point
    return result

def process_points(
    points: np.ndarray, center_index: int,
    proc_seq: list=['norm', 'center']
) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    processed_points = points.copy()
    ref_point, point_mean, point_std = None, None, None
    valid_proc_seq_list = [['center', 'norm'], ['norm', 'center']]
    check_sequence(sequence=proc_seq, valid_sequence_list=valid_proc_seq_list, label='proc_seq')

    for proc in proc_seq:
        if proc == 'center':
            ref_point, processed_points = center_points(
                points=processed_points,
                center_point_index=center_index
            )
        elif proc == 'norm':
            point_mean, point_std, processed_points = get_points_stats(processed_points)
        else:
            raise Exception

    return ref_point, point_mean, point_std, processed_points

def unprocess_points(
    ref_point: np.ndarray, point_mean: np.ndarray, point_std: np.ndarray, processed_points: np.ndarray,
    proc_seq: list=['uncenter', 'unnorm']
) -> np.ndarray:
    unprocessed_points = processed_points.copy()
    valid_proc_seq_list = [['uncenter', 'unnorm'], ['unnorm', 'uncenter']]
    check_sequence(sequence=proc_seq, valid_sequence_list=valid_proc_seq_list, label='proc_seq')

    for proc in proc_seq:
        if proc == 'unnorm':
            unprocessed_points = unnormalize_points(
                points_norm=unprocessed_points,
                points_mean=point_mean,
                points_std=point_std
            )
        elif proc == 'uncenter':
            unprocessed_points = uncenter_points(
                points=unprocessed_points,
                center_point=ref_point
            )
        else:
            raise Exception
    
    return unprocessed_points