import math
from collections import OrderedDict
from copy import copy

import numpy as np
import skimage.morphology
import scipy.integrate
from typing import Union, Tuple

from raytils.display.utils import write_text_cv2
from raytils.perception.polygon import get_polygon_area, scale_polygon, sortpts_clockwise

__all__ = ["get_circle_blob", "get_mask_contour", "get_orientation_from_blob", "get_square_blob",
           "get_volume_from_blob"]

CITATION_FIRST_RUN_MESSAGE = False


def get_oval_blob(width: int = 100, height=50) -> np.array:
    """ Returns (max(width, height), max(width, height)) np.array filled with 0s and an oval of width*height

    Args:
        width: Width of the oval blob required
        height: Height of the oval blob required

    Returns:
        Numpy array with a oval around its center filled with 1s
    """
    canvas_size = max(width, height)
    mask, _ = get_circle_blob(canvas_size)
    mask = np.asarray([[mask[int(len(mask) * r / height)][int(len(mask[0]) * c / width)]
                        for c in range(width)] for r in range(height)])
    contour = get_mask_contour(mask)
    return mask, contour


def get_circle_blob(size: int = 100) -> np.array:
    """ Returns (size, size) np.array filled with 0s and a circle of radius=size of 1s

    Args:
        size: Diameter of the circle blob required

    Returns:
        Numpy array with a circle around its center filled with 1s
    """
    radius = size / 2
    diameter = radius * 2
    mask_size = (int(diameter), int(diameter))
    mid_point = np.array([[radius], [radius]])

    mask = np.zeros(mask_size, dtype=np.uint8)
    coords = np.asarray(np.where(mask == 0))
    distances = np.sum((coords - mid_point) ** 2, axis=0) ** 0.5
    mask[(distances <= radius).reshape(mask_size)] = 1

    # contour = np.asarray(list(zip(*np.where((np.abs(distances - radius) <= 1).reshape(mask_size)))))
    contour = get_mask_contour(mask)

    return mask, contour


def get_strawberry_blob(height=100):
    """ Returns (height, height) np.array filled with 0s and 1s of a rough strawberry blob shape

    Args:
        height: Height of the berry blob required

    Returns:
        Numpy array with a oval around its center filled with 1s
    """
    mask = np.zeros((height, height), dtype=np.uint8)
    rows = height
    mid = int(height / 2)
    min_width_top = 0.35 * rows
    max_width_top = 0.85 * rows
    top_step = (max_width_top - min_width_top) / (rows * 0.35)
    max_width_bottom = 0.85 * rows
    min_width_bottom = 0.2 * rows
    bottom_step = (max_width_bottom - min_width_bottom) / (rows * 0.65)

    for i in range(rows):
        ip = i / rows
        if ip <= 0.35:
            t = min_width_top + (top_step * i)
            t2 = t / 2
            ts = int(mid - t2)
            te = int(mid + t2)
            mask[i, ts:te] = 1.0
        else:
            t = min_width_bottom + (bottom_step * (rows - i))
            t2 = t / 2
            ts = int(mid - t2)
            te = int(mid + t2)
            mask[i, ts:te] = 1.0

    contour = get_mask_contour(mask)

    return mask, contour


def get_square_blob(size: int = 500, padding: int = 25) -> np.array:
    """ Returns (size+padding*2, size+padding*2) np.array filled with 0s and a square of 1s of size

    Args:
        size: Required square size of the blob
        padding: Required padding around the edge of the blob

    Returns:
        A Numpy array (size+padding*2, size+padding*2) filled with a square blob of 1.0s
    """
    mask_size = (int(size + padding * 2), int(size + padding * 2))
    # mid_point = np.array([[int(size + padding * 2) / 2], [int(size + padding * 2) / 2]])
    mask = np.zeros(mask_size, dtype=np.uint8)
    mask[padding:size + padding, padding:size + padding] = 1

    contour = get_mask_contour(mask)

    return mask, contour


def get_mask_contour(mask: np.array, method: str = "skimage") -> np.array:
    """ Takes a binary image (N, M) and returns the edge of the blobs in XY format

    Args:
        mask: (N, M) binary image with 1.0 indicating object pixel and 0.0 background pixel
        method: 'erosion' the method to extract the contour locations

    Returns:
        Numpy array of size (contour_length, 2) where contour length is the number of x, y points
    """
    if method not in ["erosion", "skimage"]:
        raise NotImplementedError("Method '{}' not implemented".format(method))
    if method == "skimage":
        contours = skimage.measure.find_contours(mask, 0.5)
        cnt = contours[0].astype(np.int)
        return cnt
    pad = 1
    width, height = mask.shape
    padded_mask = np.zeros((width + (pad * 2), height + (pad * 2)))
    padded_mask[pad:width + pad, pad:height + pad] = mask != 0
    return np.asarray(list(zip(*np.where(padded_mask - skimage.morphology.binary_erosion(padded_mask))))) - pad


def raw_moment(mask: np.array, i_order: int, j_order: int) -> float:
    """Get moments from mask

    Args:
        mask: (N, M) binary image with 1.0 indicating object pixel and 0.0 background pixel
        i_order: ith moment to return
        j_order: jth moment to return

    Returns:
        Returns the moment[i, j] for the given mask
    """
    nrows, ncols = mask.shape
    y_indices, x_indicies = np.mgrid[:nrows, :ncols]
    return (mask * x_indicies ** i_order * y_indices ** j_order).sum()


def get_orientation_from_blob(mask: np.array, method: str = "moments") -> Tuple[float, float, float, float]:
    """Detect Orientation From Blob

    https://alyssaq.github.io/2015/computing-the-axes-or-orientation-of-a-blob/

    Calculates orientation from the covariance matrix C:

    .. math::

        C = \\left[\\begin{array}{cc} variance(x, x) & variance(x, y)\\\\ variance(x, y) & variance(y, y) \\end{array}\\right]

    Args:
        mask: (N, M) binary image with 1.0 indicating object pixel and 0.0 background pixel
        method: 'moments' or 'eigen' decides how the covariance matrix for x, y will be calculated

    Returns:
        Tuple of x_v1, y_v1, x_v2, y_v2 (Eigen Vector of minor and major axis)
    """
    if method == "moments":
        mask_sum = mask.sum()
        m10 = raw_moment(mask, 1, 0)
        m01 = raw_moment(mask, 0, 1)
        x_centroid = m10 / mask_sum
        y_centroid = m01 / mask_sum
        u11 = (raw_moment(mask, 1, 1) - x_centroid * m01) / mask_sum
        u20 = (raw_moment(mask, 2, 0) - x_centroid * m10) / mask_sum
        u02 = (raw_moment(mask, 0, 2) - y_centroid * m01) / mask_sum
        cov = np.array([[u20, u11], [u11, u02]])
    elif method == "eigen":
        y, x = np.nonzero(mask)
        x = x - np.mean(x)
        y = y - np.mean(y)
        coords = np.vstack([x, y])
        cov = np.cov(coords)
    else:
        raise NotImplementedError("Method '{}' not yet implemented")

    eigen_values, eigen_vectors = np.linalg.eig(cov)
    sort_indices = np.argsort(eigen_values)[::-1]
    x_v1, y_v1 = eigen_vectors[:, sort_indices[0]]  # Eigenvector with the largest eigenvalue
    x_v2, y_v2 = eigen_vectors[:, sort_indices[1]]

    return x_v1, y_v1, x_v2, y_v2


def get_volume_from_blob(mask: np.array, method: str = "surface_area", limit_method: str = "contour",
        integration_method: str = "quad", n_slices: int = 100, return_slices: bool = False, radius=None, n_radius=None,
        depth=None, intrinsics=None) \
        -> Union[float, Tuple[float, list]]:
    """ Calculates volume from a 2D blob plane

    Volume comes from integration of the surface area through minor axis height

    https://doi.org/10.31256/Uk4Td6I

    Args:
        intrinsics:
        mask: (N, M) binary image with 1.0 indicating object pixel and 0.0 background pixel
        method: str 'surface_area' or 'ellipsoid'
        limit_method: 'width', 'radius', or 'contour' decides how the radius parameter is calculated
        integration_method: 'trapz' (trapezoidal rule) or 'simps' (simpsons rule)
        n_slices: The number of steps to integrate over (larger more accurate, lower faster computation)
        return_slices: If true the contours of the integral slices are returned
        radius: If limit method is radius this parameter must not be None
        n_radius: If limit method is radius and method is ellipsoid this parameter used for ellipsoidal computation

    Returns:
        Volume of the 2D binary blob in mask or (Volume, Contour Slice Locations) if return_slices is true
    """
    global CITATION_FIRST_RUN_MESSAGE
    if not CITATION_FIRST_RUN_MESSAGE:
        print("Please cite https://doi.org/10.31256/Uk4Td6I if using this work")
        CITATION_FIRST_RUN_MESSAGE = True
    contour = get_mask_contour(mask, method="erosion")

    # How to calculate the radius parameter for integration
    if limit_method == "width":  # Take the width of the mask image
        width = mask.shape[0]
        height = mask.shape[1]
        n_radius = height / 2
        radius = width / 2
    elif limit_method == "height":  # Take the width of the mask image
        width = mask.shape[0]
        height = mask.shape[1]
        n_radius = width / 2
        radius = height / 2
    elif limit_method == "contour":  # Contour take the widest section of the x and y contours
        radius = (np.ptp(contour[:, 0])) / 2
        height = (np.ptp(contour[:, 1]))
        n_radius = height / 2
    elif limit_method == "radius":
        if radius is None:
            raise ValueError("Cannot use method radius when parameter radius=None")
        radius = radius
    else:
        raise NotImplementedError("Method '{}' not yet implemented".format(limit_method))

    contour = get_mask_contour(mask, method="erosion")

    my, mx = np.mean(np.where(mask != 0), axis=1)
    center_of_mass = np.asarray([[mx, my]])

    if intrinsics is not None:
        fx, fy, cx, cy = intrinsics

        depth[np.logical_not(mask)] = 0

        y, x = np.where(mask != 0)
        z = depth[np.logical_and(depth != 0, mask != 0)]
        z_max = np.max(z)
        x = (x - cx) * z_max / fx
        y = (y - cy) * z_max / fy
        minor = np.ptp(x)
        major = np.ptp(y)
        cross = np.ptp(z) * 2

        contour = contour.astype(np.float)
        contour[:, 0] = np.abs((contour[:, 0] - cy) * z_max / fy)
        contour[:, 1] = np.abs((contour[:, 1] - cx) * z_max / fx)

        center_of_mass = np.abs(np.asarray([[np.mean(x), np.mean(y)]]))
        radius = minor / 2
        n_radius = major / 2
        height = major
        # if integration_method == "quad":
        #     print(f"Minor = {minor:.2f}, Major = {major:.2f}, Cross = {cross:.2f}")

    if method == "disc":
        if intrinsics is not None:
            fa = 1
            px2x = lambda _x: (_x - cx) * z_max / fx
            py2y = lambda _y: (_y - cy) * z_max / fy
        else:
            fa = 0
            px2x = lambda _x: _x
            py2y = lambda _y: _y
        binary = mask != 0
        row_sums = binary.sum(axis=fa)
        row_start = (binary != 0).argmax(axis=fa)
        sample_rate = 1

        row_start = row_start[row_sums != 0]
        row_sums = row_sums[row_sums != 0]
        idxs = range(0, len(row_start), sample_rate)
        row_start = row_start[idxs]
        row_sums = row_sums[idxs]

        row_sum_starts = row_start
        row_sum_ends = row_start + row_sums
        rows_radius = (px2x(row_sum_ends) - px2x(row_sum_starts)) / 2.0
        dy_distance = (py2y(sample_rate) - py2y(0))

        disc_areas = (np.pi * (rows_radius ** 2))
        disc_volumes = (np.pi * (rows_radius ** 2) * dy_distance)

        polygon_volume = disc_volumes.sum()

        if return_slices:
            contours = [contour]
            return polygon_volume, contours
        return polygon_volume
    elif method == "surface_area":
        # Derivative of Area is Perimeter, Derivative of Volume is Surface Area
        # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.598.3691&rep=rep1&type=pdf
        # Setup the integration arrays (x=radius at each slice, y=area function at each slice (f(x)))
        # TODO: Use sets to represent the contours so unique points aren't duplicated
        contours = []
        dy = radius / n_slices
        radius_steps = np.arange(0, radius, dy)  # x=r at each step
        actual_steps = []  # Array for quad integration step tracking

        # y = f(x), where f(x) is the surface area at a radius x
        def f(_x):
            actual_steps.append(_x)
            p = scale_polygon(contour, center_of_mass, _x / radius)
            a = get_polygon_area(p)
            contours.append(p)
            return 4 * a

        # Summation to solve for volume
        if integration_method == "quad":
            polygon_volume, polygon_error = scipy.integrate.quad(f, 0, radius)
            radius_steps = actual_steps
        elif integration_method == "trapz":
            y = [f(x) for x in radius_steps]
            polygon_volume = scipy.integrate.trapz(y, radius_steps)
        elif integration_method == "simps":
            y = [f(x) for x in radius_steps]
            polygon_volume = scipy.integrate.simps(y, radius_steps)
        else:
            raise NotImplementedError("Integration method '{}' is not yet implemented".format(integration_method))

        if return_slices:
            return polygon_volume, contours
        return polygon_volume
    elif method == "ellipsoid":
        polygon_volume = (4 / 3) * np.pi * n_radius * radius ** 2
        if n_radius is None:
            raise ValueError("You must pass n_radius")
        if return_slices:
            contours = [contour]
            return polygon_volume, contours
        return polygon_volume
    else:
        raise NotImplementedError("Method '{}' not yet implemented".format(method))
