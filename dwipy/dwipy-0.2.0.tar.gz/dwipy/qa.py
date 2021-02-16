import os

import numpy as np

import dwipy.constants
import dwipy.IO.gradient_table


def check_grad_file_status(grad_file: str) -> dwipy.constants.GRADSTATUS:
    """
    Check the status of the gradients from a gradient file.

    Args:
        grad_file (str): Path to gradient file

    Returns:
        dwipy.constants.GRADSTATUS: The gradient status
    """
    if os.path.exists(grad_file):
        return check_grads_status(dwipy.IO.gradient_table.load_mrtrix_grads(grad_file))
    else:
        return dwipy.constants.GRADSTATUS.GRADS_NOT_FOUND


def check_grads_status(grads: np.ndarray) -> dwipy.constants.GRADSTATUS:
    bvals, bvecs = dwipy.IO.gradient_table.get_mrtrix_bvals_and_bvecs(grads)

    if any(np.isnan(bvals)):
        return dwipy.constants.GRADSTATUS.BVALS_HAS_NAN

    unique_bvals = np.unique(bvals)
    n_unique_bvals = len(unique_bvals)

    bvecs_non_zero = bvecs[bvals != 0, :]
    bvecs_total_per_direction = np.sum(np.abs(bvecs_non_zero), axis=0)

    if any(bvecs_total_per_direction == 0) and any(bvecs_total_per_direction > 0):
        return dwipy.constants.GRADSTATUS.DTI_ONE_DIRECTION
    if n_unique_bvals < 2:
        return dwipy.constants.GRADSTATUS.ONE_BVAL
    if any(unique_bvals > 3500):
        return dwipy.constants.GRADSTATUS.BVALS_TOO_HIGH
    else:
        return dwipy.constants.GRADSTATUS.VALID_GRADS


def grad_file_is_valid(grad_file: str) -> bool:
    """
    Check the validity of a gradient file.

    Args:
        grad_file (str): Path to gradient file

    Returns:
        bool: True if gradients are valid, False otherwise
    """
    return check_grad_file_status(grad_file) is dwipy.constants.GRADSTATUS.VALID_GRADS


def get_dwi_type(grad_file: str) -> dwipy.constants.DWITYPE:
    grad_matrix = dwipy.IO.gradient_table.load_mrtrix_grads(grad_file)

    bvecs = dwipy.IO.gradient_table.get_mrtrix_bvecs(grad_matrix)
    bvals = dwipy.IO.gradient_table.get_mrtrix_bvals(grad_matrix)

    bvec_total_value = np.sum(np.power(bvecs, 2), axis=1)

    if len(bvals) == 2 and np.count_nonzero(bvecs) == 0:
        return dwipy.constants.DWITYPE.DWI_SINGLE_TRACE
    elif len(bvals) > 2 and np.count_nonzero(bvecs) == 0:
        return dwipy.constants.DWITYPE.DWI_MULTI_TRACE
    elif np.count_nonzero(np.unique(bvals)) == np.count_nonzero(bvec_total_value):
        # We have bvecs but with just one corresonding bval for each
        # Not really a DTI, probably error in extraction
        return dwipy.constants.DWITYPE.DWI_TRACE_NONZERO_BVAL
    elif np.count_nonzero(bvecs) == 0:
        return dwipy.constants.DWITYPE.UNKNOWN
    else:
        # Bvec values for non-zero b values
        max_bvec = np.amax(np.abs(bvecs[bvals != 0, :]), axis=1)
        is_zero = np.isclose(bvec_total_value[bvals != 0], 0)

        if len(np.unique(bvals[bvals != 0])) * 3 == np.count_nonzero(max_bvec):
            # We can have multiple bvals that each a single x/y/z bvec
            # We do not consider this DTI
            return dwipy.constants.DWITYPE.DWI_MULTI_B_VECS
        elif np.sum(is_zero) != 0:
            # Some non-zero bvals are actually trace images
            return dwipy.constants.DWITYPE.DWI_MULTI_B_VECS_AND_TRACE
        else:
            return dwipy.constants.DWITYPE.DTI
