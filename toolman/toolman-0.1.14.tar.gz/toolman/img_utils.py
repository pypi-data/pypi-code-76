"""

"""


# Built-in

# Libs
import cv2
import numpy as np
from skimage import measure

# Own modules
from .misc_utils import load_file


def get_img_channel_num(file_name):
    """
    Get #channels of the image file
    :param file_name: absolute path to the image file
    :return: #channels or ValueError
    """
    img = load_file(file_name)
    if len(img.shape) == 2:
        channel_num = 1
    elif len(img.shape) == 3:
        channel_num = img.shape[-1]
    else:
        raise ValueError('Image can only have 2 or 3 dimensions')
    return channel_num


def change_channel_order(data, to_channel_last=True):
    """
    Switch the image type from channel first to channel last
    :param data: the data to switch the channels
    :param to_channel_last: if True, switch the first channel to the last
    :return: the channel switched data
    """
    if to_channel_last:
        if len(data.shape) == 3:
            return np.rollaxis(data, 0, 3)
        else:
            return np.rollaxis(data, 1, 4)
    else:
        if len(data.shape) == 3:
            return np.rollaxis(data, 2, 0)
        else:
            return np.rollaxis(data, 3, 1)


def binarize_mask(img, thresh=3):
    """
    Binarize a given mask image
    :param img: the image to be binarized
    :param thresh: the threshold to binarize the segmenation map
    :return:
    """
    if len(img.shape) == 3:
        # get binary label map
        img = (img[:, :, 0] < thresh).astype(np.uint8)
    else:
        img = (img[:, :] < thresh).astype(np.uint8)
    return img


def seg_to_bbox(img, binarize=False, dilate=True, thresh=127, kernel_size=3):
    """
    Transform segmentation mask to bounding boxes
    :param img: the segmentation mask
    :param binarize: if True, the map will be binarized by a threshold
    :param dilate: if True, will dilate the segmentation images first, this is to create larger bounding boxes that
                   wraps up each object. Notice, this might also merge two nearby objects
    :param thresh: the threshold to binarize the segmenation map
    :param kernel_size: the kernel size for dilation
    :return:
    """
    if isinstance(img, str):
        img = load_file(img)

    if binarize:
        img = binarize_mask(img)

    # dilate the image
    if dilate:
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)

    # connected components
    im_label = measure.label(img > 0)
    reg_props = measure.regionprops(im_label, img)

    # get bboxes
    bboxes = []
    for rp in reg_props:
        if rp.area > 50:
            bboxes.append(rp.bbox)

    return bboxes


def seg_to_polygon(img, binarize=False, approx=False):
    """
    Transform segmentation mask to polygons
    :param img: the segmentation mask
    :param binarize: if True, the map will be binarized by a threshold
    :param approx: if True, the polygons will be approximated. Note, this is not working very well some times
    :return:
    """
    if isinstance(img, str):
        img = load_file(img)

    if binarize:
        img = binarize_mask(img)

    contours, hierarchy = cv2.findContours(img, 1, 2)

    polygons = []

    for contour in contours:
        if approx:
            epsilon = 0.1 * cv2.arcLength(contour, True)
            contour = cv2.approxPolyDP(contour, epsilon, True)
        contour = [a[0].tolist() for a in contour]
        polygons.append(contour)

    return polygons


if __name__ == '__main__':
    pass
