import numpy as np


def symmetrization(x):
    return np.multiply(np.random.choice([0.5, -0.5], x.size, replace=True), x)
