from numba import jit
import numpy as np
import functools


def _tuplify_majority_mask_filter(in_function):
    """
    Make sure that "block_replace_params" is tuple of tuple in order to keep jit alive, where python lists are
    not jey implemented.
    """
    @functools.wraps(in_function)
    def out_function(*args, **kwargs):
        if "block_replace_params" in kwargs:
            kwargs["block_replace_params"] = tuple([tuple(i) for i in kwargs["block_replace_params"]])
        return in_function(*args, **kwargs)

    return out_function


@_tuplify_majority_mask_filter  # ensure that [block_replace_params] is tuple of tuples
@jit(nopython=True)
def majority_mask_filter(mask, majority_width=2, block_replace=True, block_replace_params=((50, 5),), nodata_value=255):
    """
    Post processing of noisy masks of integer values. The set of values in mask are the same as in the result. Two
    filters are performed:

    1.) Majority filter: Take a window of size [majority_width] around each pixel (i,j) and replace the the local value
        with the most occuring one within that window. The nodata value is not taken. Filterung takes place if
        [majority_width] is larger than zero.

    2.) Block replace: If the pixel (i,j) is within [block_replace_params=((([id of classs],[area to be filled up]),)]
        then replace all pixels in a window of range [area to be filled up] with [id of classs]. The order is taken from
        the provided tuple ot list.

    :param nodata_value: for mask, should be integer
    :param mask: 2D numpy array of integer type
    :param majority_width: with of the 2D area for the majority search
    :param block_replace: whether to do a block replace
    :param block_replace_params: tuple of 2 parameters: (([id of class],[area to be filled up]),)
    :return: filtered mask
    """

    # set the ranges to loop over the mask
    i_min = 0
    j_min = 0
    i_max = mask.shape[0]
    j_max = mask.shape[1]

    # enable / disable filtering
    filter_2d = True if majority_width > 0 else False
    # initialize result
    res = np.empty((i_max, j_max), dtype=np.uint8)
    # start loop
    for i in np.arange(i_min, i_max):
        for j in np.arange(j_min, j_max):

            if mask[i, j] == nodata_value:  # copy nodata value areas
                res[i, j] = nodata_value
            else:
                if filter_2d is True:
                    # make sure to stay within bounds of array
                    i1, i2 = i - majority_width, i + majority_width
                    if i1 < i_min:
                        i1 = i_min
                    if i2 > i_max:
                        i2 = i_max

                    j1, j2 = j - majority_width, j + majority_width
                    if j1 < j_min:
                        j1 = j_min
                    if j2 > j_max:
                        j2 = j_max
                    # select most occurring value within window as new value
                    bc = np.bincount(mask[i1:i2, j1:j2].flatten())
                    res[i, j] = bc.argmax()
                    if res[i, j] == nodata_value:  # is nodata, then edge if area is concerned -> take next best one
                        bc[nodata_value] = 0
                        res[i, j] = bc.argmax()

                else:  # with no filtering, copy array
                    res[i, j] = mask[i, j]

                if block_replace is True:
                    for mask_id, dd_mask in block_replace_params:  # loop over provided set

                        if res[i, j] == mask_id:
                            # ensure to stay in range of the area
                            i1, i2 = i - dd_mask, i + dd_mask
                            if i1 < i_min:
                                i1 = i_min
                            if i2 > i_max:
                                i2 = i_max

                            j1, j2 = j - dd_mask, j + dd_mask
                            if j1 < j_min:
                                j1 = j_min
                            if j2 > j_max:
                                j2 = j_max
                            # fill up area with value -> this can leak to nodata value areas
                            res[i1:i2, j1:j2] = mask_id

    if block_replace is True:  # leaking into nodata value areas might have occurred -> clean up
        for i in np.arange(i_min, i_max):
            for j in np.arange(j_min, j_max):
                if mask[i, j] == nodata_value:
                    res[i, j] = nodata_value

    return res
