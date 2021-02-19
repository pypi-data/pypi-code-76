import numpy as np
from numba import njit, prange
from pykdtree.kdtree import KDTree


def inverse_mapping(map_x, map_y, image_shape):
    h, w = image_shape
    x_pos, y_pos = np.meshgrid(np.arange(w), np.arange(h))
    map_x = np.ndarray.astype(x_pos + map_x, np.float32)
    map_y = np.ndarray.astype(y_pos + map_y, np.float32)

    data = np.c_[map_y.ravel(), map_x.ravel()]
    tree = KDTree(data, leafsize=16)

    coords = np.c_[y_pos.ravel(), x_pos.ravel()]

    pts = np.array(np.c_[y_pos.ravel(), x_pos.ravel()], dtype=np.float32)
    distances, indices = tree.query(pts, k=5, distance_upper_bound=32.0)

    map_x_inverse = np.zeros((h, w))
    map_y_inverse = np.zeros((h, w))
    map_x_inverse, map_y_inverse = inverse_distance_weighting(pts.astype(np.int), distances, indices, coords, map_x_inverse, map_y_inverse)

    return map_x_inverse, map_y_inverse


@njit(parallel=True)
def inverse_distance_weighting(pts, distances, indices, values, map_x_inverse, map_y_inverse):
    for i in prange(pts.shape[0]):
        x = pts[i, 1]
        y = pts[i, 0]
        idxs = indices[i]

        wsum = 0
        map1_value = 0
        map2_value = 0
        for k in range(distances[i].shape[0]):
            weights = 1 / ((distances[i][k] + 1e-12) ** 2)
            wsum += weights
            map1_value += weights * values[idxs[k], 1]
            map2_value += weights * values[idxs[k], 0]

        map_x_inverse[y, x] = map1_value / wsum
        map_y_inverse[y, x] = map2_value / wsum

    return map_x_inverse, map_y_inverse
