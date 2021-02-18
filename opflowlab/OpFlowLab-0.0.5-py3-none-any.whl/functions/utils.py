import glob
import os

import scipy.signal
import skimage.io
from scipy.io import loadmat

from .interpolation import *


def imadjust(image, in_bound=(0.001, 0.999), out_bound=(0, 1)):
    """
    See https://stackoverflow.com/questions/39767612/what-is-the-equivalent-of-matlabs-imadjust-in-python/44529776#44529776
    image : input one-layer image (numpy array)
    in_bound  : src image bounds
    out_bound : dst image bounds
    output : output img
    """

    assert len(image.shape) == 2, 'Input image should be 2-dims'
    image_dtype = image.dtype

    if image_dtype == 'uint8':
        range_value = 255
    elif image_dtype == 'uint16':
        range_value = 65535
    else:
        range_value = 1

    # Compute in and out limits
    in_bound = np.percentile(image, np.multiply(in_bound, 100))
    out_bound = np.multiply(out_bound, range_value)

    # Stretching
    scale = (out_bound[1] - out_bound[0]) / (in_bound[1] - in_bound[0])

    image = image - in_bound[0]
    image[image < 0] = 0

    output = image * scale + out_bound[0]
    output[output > out_bound[1]] = out_bound[1]

    output = output.astype(image_dtype)

    return output


def load_velocity_filelist(folder,
                           velocity_type='dense', xy_folder_list=('flowx', 'flowy'), file_ext='*.bin',
                           reverse_sort=False):
    velocity_type = velocity_type.lower()
    if velocity_type == 'dense':
        vector_x_filelist = glob.glob(os.path.join(folder, xy_folder_list[0], file_ext))
        vector_x_filelist.sort(reverse=reverse_sort)
        vector_y_filelist = glob.glob(os.path.join(folder, xy_folder_list[1], file_ext))
        vector_y_filelist.sort(reverse=reverse_sort)
        return [vector_x_filelist, vector_y_filelist]
    elif velocity_type == 'sparse':
        vector_filelist = glob.glob(os.path.join(folder, file_ext))
        vector_filelist.sort(reverse=reverse_sort)
        return [vector_filelist]


# tracer functions
def load_velocity_bin(vector_file, shape, bin_dtype="float32", kernel_size=5):
    bin_dtype = bin_dtype.lower()
    if bin_dtype == "float16":
        dtype = np.half
    else:
        dtype = np.float32

    vectors = np.fromfile(vector_file, dtype=dtype)

    # convert back to float32 for future calculations
    if bin_dtype == "float16":
        vectors = np.float32(vectors)

    vectors = np.reshape(vectors, shape)

    if kernel_size is not None:
        vectors = scipy.signal.medfilt2d(vectors, kernel_size=kernel_size)

    return vectors


def load_velocity_piv(vector_file, frame_no):
    piv_mat = loadmat(vector_file)
    x = piv_mat['x'][frame_no][0]
    y = piv_mat['y'][frame_no][0]
    flow_x = piv_mat['u_filtered'][frame_no][0]
    flow_y = piv_mat['v_filtered'][frame_no][0]

    return flow_x, flow_y, x, y


@njit(fastmath=True, parallel=True)
def replace_value(input_array, output_array, value, replacement):
    m = input_array.shape[0]
    n = input_array.shape[1]

    for i in prange(m):
        for j in prange(n):
            if input_array[i, j] == value:
                output_array[i, j] = replacement
    return output_array


@njit(fastmath=True, parallel=True)
def numba_replace(input_array, output_array, keys, values):
    ind_sort = np.argsort(keys)
    keys_sorted = keys[ind_sort]
    values_sorted = values[ind_sort]
    s_keys = set(keys)

    for i in prange(input_array.shape[0]):
        for j in prange(input_array.shape[1]):
            if input_array[i, j] in s_keys:
                ind = np.searchsorted(keys_sorted, input_array[i, j])
                output_array[i, j] = values_sorted[ind]
    return output_array


def save_output(array, filename, save_velocity_as_tif=False, save_dtype="float16"):
    if save_velocity_as_tif:
        skimage.io.imsave('{}.tif'.format(filename), array)
    else:
        if save_dtype == "float16":
            array = array.astype(np.half)

        with open('{}.bin'.format(filename), 'wb') as file:
            array.tofile(file)
        file.close()
