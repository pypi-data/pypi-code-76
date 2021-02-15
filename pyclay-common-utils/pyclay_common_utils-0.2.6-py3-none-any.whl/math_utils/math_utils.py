import math
import numpy as np
from logger import logger

def gaussian(x, mu, sigma):
    coeff = 1/(2*math.pi*sigma**2)**0.5
    power = (-(x - mu)**2)/(2*sigma**2)
    return coeff * math.exp(power)

def get_normal_vector(points: np.ndarray):
    """
    Note: Direction of normal vector depends on right hand rule.
    p0, p1, p2 = points
    v01, v12 = p1 - p0, p2 - p1
    """
    if points.shape != (3, 3):
        logger.error(f"Received points matrix of size {points.shape}. Expected (3, 3).")
        raise Exception
    p0, p1, p2 = points
    
    # These two vectors are in the plane
    v01 = p1 - p0
    v12 = p2 - p1

    # The cross product is a vector normal to the plane
    result = np.cross(v01, v12)
    return result
