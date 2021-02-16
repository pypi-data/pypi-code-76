from typing import Tuple
import numpy as np


def load_mrtrix_grads(grad_file: str) -> np.ndarray:
    """
    Load a gradient file from the mrtrix3 format.

    Args:
        grad_file (str): File location

    Returns:
        np.ndarray: Gradients, [Nx4] matrix with N the number of entries
    """
    # Load the array with minimum of 2 dimension
    # Otherwise in case of a single line we get 1 dimensional array
    # Which is confusing for index
    grad_matrix = np.loadtxt(grad_file, delimiter=" ", comments="#", dtype=float, ndmin=2)

    # Round the bvals, they should be int
    # But in some cases, there are small floats
    grad_matrix[:, 3] = np.around(grad_matrix[:, 3])

    return grad_matrix


def get_mrtrix_bvals(grad_matrix: np.ndarray) -> np.ndarray:
    """
    Get the b-values from a gradient matrix.

    Args:
        grad_matrix (np.ndarray): Gradient matrix

    Returns:
        np.ndarray: The b-values
    """
    # Bvals are last column
    return grad_matrix[:, 3]


def load_mrtrix_bvals(grad_file: str) -> np.ndarray:
    """
    Load b-values from a gradient file.

    Args:
        grad_file (str): Path to gradient file

    Returns:
        np.ndarray: The b-values
    """
    grad_matrix = load_mrtrix_grads(grad_file)
    return get_mrtrix_bvals(grad_matrix)


def get_mrtrix_bvecs(grad_matrix: np.ndarray) -> np.ndarray:
    """
    Get the gradient vectors from a gradient matrix.

    Args:
        grad_matrix (np.ndarray): Gradient matrix

    Returns:
        np.ndarray: The gradient vectors
    """
    # Bvecs are everything up to last column
    return grad_matrix[:, 0:3]


def load_mrtrix_bvecs(grad_file: str) -> np.ndarray:
    """
    Load the gradient vectors from a gradient file

    Args:
        grad_file (str): Path to gradient file

    Returns:
        np.ndarray: The gradient vectors
    """
    grad_matrix = load_mrtrix_grads(grad_file)
    return get_mrtrix_bvecs(grad_matrix)


def get_mrtrix_bvals_and_bvecs(grad_matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the b-values and gradient vectors from a gradient matrix.

    Args:
        grad_matrix (np.ndarray): The gradient matrix

    Returns:
        Tuple[np.ndarray, np.ndarray]: The b-values and gradient vectors
    """
    return get_mrtrix_bvals(grad_matrix), get_mrtrix_bvecs(grad_matrix)


def write_mrtrix_grads(grad_file: str, grads: np.ndarray) -> str:
    """
    Write a gradient table to a mrtrix3 file.

    Args:
        grad_file (str): Path to the gradient file
        grads (np.ndarray): Gradient table to write

    Raises:
        ValueError: If gradient table does not have the right shape

    Returns:
        str: The path of the written gradient file
    """
    if grads.shape[1] != 4:
        raise ValueError(
            "Gradient table needs to have 4 columns. Your gradient table has {columns} instead".format(
                columns=grads.shape[1]
            )
        )

    np.savetxt(grad_file, grads, delimiter=" ", fmt=["%2.5f", "%2.5f", "%2.5f", "%d"])

    return grad_file
