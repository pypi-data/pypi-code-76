from typing import List, Tuple

import numpy as np


def get_heatmap_from_points(image_shape: Tuple[int, int], points: List[Tuple[int, int]]):
    points = np.array(points)
    yy, xx = np.meshgrid(np.arange(image_shape[0]), np.arange(image_shape[1]))
    xd = np.array([(xx - points[i, 1]) ** 2 for i in range(len(points))])
    yd = np.array([(yy - points[i, 0]) ** 2 for i in range(len(points))])
    d = np.min(xd + yd, axis=0) ** 0.5
    return d / d.ptp()


def __main():
    pass


if __name__ == '__main__':
    __main()
