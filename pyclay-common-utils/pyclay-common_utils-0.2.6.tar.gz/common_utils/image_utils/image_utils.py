from typing import List
import cv2
import numpy as np
from ..common_types import Size
from logger import logger
from ..check_utils import check_type_from_list, \
    check_filepath_list_exists

def get_scaled_dims(width: int, height: int, scale_factor) -> (int, int):
    return int(width * scale_factor), int(height * scale_factor)

def scale_img(frame: np.ndarray, scale_factor) -> np.ndarray:
    height, width = frame.shape[:2]
    downsized_width, downsized_height = get_scaled_dims(width, height, scale_factor)

    if scale_factor == 1.0:    
        return frame
    elif scale_factor > 0.0 and scale_factor < 1.0:
        return cv2.resize(
            frame,
            (downsized_width, downsized_height),
            interpolation=cv2.INTER_AREA)
    elif scale_factor > 1.0:
        return cv2.resize(
            frame,
            (downsized_width, downsized_height),
            interpolation=cv2.INTER_LINEAR)
    else:
        raise Exception(f"Invalid scale_factor={scale_factor}. Expected scale_factor > 0.")

def get_grayscale(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def get_size(img: np.ndarray) -> Size:
    height, width = img.shape[:2]
    return Size(width=width, height=height)

def resize_img0(img: np.ndarray, size: Size) -> np.ndarray:
    img_size = get_size(img)
    if size.area >= img_size.area:
        return cv2.resize(
            src=img, dsize=(size.width, size.height), interpolation=cv2.INTER_LINEAR
        )
    else:
        return cv2.resize(
            src=img, dsize=(size.width, size.height), interpolation=cv2.INTER_AREA
        )

def resize_img(img: np.ndarray, size: Size, interpolation_method: str='area') -> np.ndarray:
    possible_methods = ['area', 'linear']
    if interpolation_method.lower() == 'area':
        interpolation = cv2.INTER_AREA
    elif interpolation_method.lower() == 'linear':
        interpolation = cv2.INTER_LINEAR
    else:
        logger.error(f"Invalid interpolation_method: {interpolation_method}")
        logger.error(f"Possible choices for interpolation_method:")
        for possible_method in possible_methods:
            logger.error(f"\t{possible_method}")
        raise Exception
    return cv2.resize(
        src=img, dsize=(size.width, size.height), interpolation=interpolation
    )

def show_cv2_image(img: np.ndarray, title: str='Test', window_size: Size=None):
    if img.dtype is np.dtype('int64'):
        image = img.astype('uint8')
    else:
        image = img.copy()
    cv2.namedWindow(winname=title, flags=cv2.WINDOW_NORMAL)
    if window_size is not None:
        cv2.resizeWindow(winname=title, width=window_size.width, height=window_size.height)
    cv2.imshow(title, image)
    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()

def cv2_img2matplotlib_img(img: np.ndarray):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def matplotlib_img2cv2_img(img: np.ndarray):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def concat_images(imga, imgb, orientation: int=0):
    """
    Combines two color image ndarrays side-by-side.

    orientation
    0: horizontal
    1: vertical
    """
    ha, wa = imga.shape[:2]
    hb, wb = imgb.shape[:2]
    max_h, max_w = np.max([ha, hb]), np.max([wa, wb])
    sum_h, sum_w = np.sum([ha, hb]), np.sum([wa, wb])

    if orientation == 0: # horizontal
        new_img = np.zeros(shape=(max_h, sum_w, 3))
        new_img[:ha, :wa] = imga
        new_img[:hb, wa:wa+wb] = imgb
    elif orientation == 1: # vertical
        new_img = np.zeros(shape=(sum_h, max_w, 3))
        new_img[:ha, :wa] = imga
        new_img[ha:ha+hb, :wb] = imgb
    else:
        raise Exception

    return new_img.astype('uint8')

def concat_n_images(img_list: list, orientation: int=0):
    """
    Combines N color images from a list ndarray images

    orientation
    0: horizontal
    1: vertical
    """
    output = None
    for i, img in enumerate(img_list):
        if i==0:
            output = img
        else:
            output = concat_images(output, img, orientation=orientation)
    return output

def concat_n_images_from_pathlist(img_pathlist: list, orientation: int=0):
    """
    Combines N color images from a list of image paths.

    orientation
    0: horizontal
    1: vertical
    """
    check_filepath_list_exists(img_pathlist)

    output = None
    for i, img_path in enumerate(img_pathlist):
        img = cv2.imread(img_path)
        if i==0:
            output = img
        else:
            output = concat_images(output, img, orientation=orientation)
    return output

def scale_to_max(img: np.ndarray, target_shape: List[int]) -> np.ndarray:
    """
    Scales an image to a given target_shape, where the image is fitted
    to either the vertical borders or horizontal borders of the frame,
    depending on the current shape of the image.
    """
    result = img.copy()
    target_h, target_w = target_shape[:2]
    img_h, img_w = img.shape[:2]
    h_ratio, w_ratio = target_h / img_h, target_w / img_w
    if abs(h_ratio - 1) <= abs(w_ratio - 1): # Fit height to max
        fit_h, fit_w = int(target_h), int(img_w * h_ratio)
    else: # Fit width to max
        fit_h, fit_w = int(img_h * w_ratio), int(target_w)
    result = cv2.resize(src=result, dsize=(fit_w, fit_h))
    return result

def pad_to_max(img: np.ndarray, target_shape: List[int]) -> np.ndarray:
    """
    Pads an image to a given target_shape.
    The padded region is filled with [0, 0, 0] (Black)
    """
    target_h, target_w = target_shape[:2]
    img_h, img_w = img.shape[:2]
    if img_h > target_h or img_w > target_w:
        logger.error(f"img.shape[:2]={img.shape[:2]} doesn't fit inside of target_shape[:2]={target_shape[:2]}")
        raise Exception
    dy, dx = int((target_h - img_h)/2), int((target_w - img_w)/2)
    result = np.zeros([target_h, target_w, 3]).astype('uint8')
    result[dy:dy+img_h, dx:dx+img_w, :] = img
    return result

def collage_from_img_buffer(img_buffer: List[np.ndarray], collage_shape: (int, int)) -> np.ndarray:
    target_buffer_len = collage_shape[0] * collage_shape[1]
    assert len(img_buffer) <= target_buffer_len, f"len(img_buffer)={len(img_buffer)} doesn't match collage_shape={collage_shape}"
    if len(img_buffer) < target_buffer_len:
        blank_img = np.zeros_like(img_buffer[0])
        img_buffer0 = img_buffer + [blank_img]*(target_buffer_len-len(img_buffer))
    else:
        img_buffer0 = img_buffer.copy()
    result_img_idx_matrix = np.array([idx for idx in range(len(img_buffer0))]).reshape(*collage_shape).tolist()
    row_img_list = [cv2.hconcat([img_buffer0[idx] for idx in img_idx_list]) for img_idx_list in result_img_idx_matrix]
    collage_img = cv2.vconcat(row_img_list) if len(row_img_list) > 1 else row_img_list[0]
    return collage_img