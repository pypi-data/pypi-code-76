# -*- coding: utf-8 -*-

"""
@date: 2021/1/21 上午10:12
@file: functional_numpy.py
@author: zj
@description: 
"""

import cv2
import numbers
import numpy as np
import torch
from typing import List, Tuple, Any, Optional, Sequence

import albumentations as A


@torch.jit.unused
def _is_numpy(img: Any) -> bool:
    return isinstance(img, np.ndarray)


@torch.jit.unused
def _is_numpy_image(img: Any) -> bool:
    return img.ndim in {2, 3}


@torch.jit.unused
def _get_image_size(img: Any) -> List[int]:
    """
    Returns image size as [w, h]
    """
    if _is_numpy_image(img):
        return img.shape[1::-1]
    raise TypeError("Unexpected type {}".format(type(img)))


@torch.jit.unused
def resize(img, size, interpolation=cv2.INTER_LINEAR):
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))
    if not (isinstance(size, int) or (isinstance(size, Sequence) and len(size) in (1, 2))):
        raise TypeError('Got inappropriate size arg: {}'.format(size))

    if interpolation not in [cv2.INTER_LINEAR, cv2.INTER_AREA, cv2.INTER_CUBIC, cv2.INTER_LANCZOS4, cv2.INTER_NEAREST]:
        raise ValueError("This interpolation mode is unsupported with Numpy input")

    if isinstance(size, int) or len(size) == 1:
        if isinstance(size, Sequence):
            size = size[0]
        h, w = img.shape[:2]
        if (w <= h and w == size) or (h <= w and h == size):
            return img
        if w < h:
            ow = size
            oh = int(size * h / w)
        else:
            oh = size
            ow = int(size * w / h)
    else:
        oh, ow = size[:2]
    aug = A.Resize(oh, ow, interpolation=interpolation, always_apply=True)
    return aug.apply(img)


@torch.jit.unused
def crop(img: np.ndarray, top: int, left: int, height: int, width: int) -> np.ndarray:
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    aug = A.Crop(x_min=left, y_min=top, x_max=left + width, y_max=top + height, always_apply=True)
    return aug.apply(img)


@torch.jit.unused
def pad(img, padding, fill=0, padding_mode="constant"):
    if not _is_numpy_image(img):
        raise TypeError("img should be Numpy Image. Got {}".format(type(img)))

    if not isinstance(padding, (numbers.Number, tuple, list)):
        raise TypeError("Got inappropriate padding arg")
    if not isinstance(fill, (numbers.Number, str, tuple)):
        raise TypeError("Got inappropriate fill arg")
    if not isinstance(padding_mode, str):
        raise TypeError("Got inappropriate padding_mode arg")

    if isinstance(padding, list):
        padding = tuple(padding)

    if isinstance(padding, tuple) and len(padding) not in [1, 2, 4]:
        raise ValueError("Padding must be an int or a 1, 2, or 4 element tuple, not a " +
                         "{} element tuple".format(len(padding)))

    if isinstance(padding, tuple) and len(padding) == 1:
        # Compatibility with `functional_tensor.pad`
        padding = padding[0]

    if padding_mode not in ["constant", "edge", "reflect", "symmetric"]:
        raise ValueError("Padding mode should be either constant, edge, reflect or symmetric")

    if isinstance(padding, int):
        pad_left = pad_right = pad_top = pad_bottom = padding
    if isinstance(padding, Sequence) and len(padding) == 2:
        pad_top = pad_bottom = padding[0]
        pad_left = pad_right = padding[1]
    if isinstance(padding, Sequence) and len(padding) == 4:
        pad_top = padding[0]
        pad_left = padding[1]
        pad_bottom = padding[2]
        pad_right = padding[3]

    aug = A.IAACropAndPad(px=(pad_top, pad_right, pad_bottom, pad_left), pad_mode=padding_mode, pad_cval=fill,
                          keep_size=False).processor
    return aug.augment_image(img)


@torch.jit.unused
def hflip(img):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    aug = A.HorizontalFlip(always_apply=True)
    return aug.apply(img)


@torch.jit.unused
def vflip(img):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    aug = A.VerticalFlip(always_apply=True)
    return aug.apply(img)


@torch.jit.unused
def perspective(img, startpoints, endpoints, interpolation=cv2.INTER_CUBIC, fill=None):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    height, width = img.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32(startpoints), np.float32(endpoints))

    return cv2.warpPerspective(img, M, (width, height), flags=interpolation, borderValue=fill)


@torch.jit.unused
def adjust_brightness(img, brightness_factor):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    return A.adjust_brightness_torchvision(img, brightness_factor)


@torch.jit.unused
def adjust_contrast(img, contrast_factor):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    return A.adjust_contrast_torchvision(img, contrast_factor)


@torch.jit.unused
def adjust_saturation(img, saturation_factor):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    return A.adjust_saturation_torchvision(img, saturation_factor)


@torch.jit.unused
def adjust_hue(img, hue_factor):
    if not (-0.5 <= hue_factor <= 0.5):
        raise ValueError('hue_factor ({}) is not in [-0.5, 0.5].'.format(hue_factor))

    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    return A.adjust_hue_torchvision(img, hue_factor)


@torch.jit.unused
def rotate(img, angle, interpolation=0, expand=False, center=None, fill=None):
    if not _is_numpy_image(img):
        raise TypeError("img should be Numpy NDArray. Got {}".format(type(img)))

    return A.rotate(img, angle, interpolation=interpolation, value=fill)


@torch.jit.unused
def affine(img, angle, translate, scale, shear, interpolation, fill):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    aug = A.IAAAffine(
        scale=scale,
        translate_percent=None,
        translate_px=translate,
        rotate=angle,
        shear=shear,
        order=1,
        cval=fill,
        mode=interpolation,
        always_apply=True
    )
    return aug.apply(img)


@torch.jit.unused
def to_grayscale(img, num_output_channels):
    if not _is_numpy_image(img):
        raise TypeError('img should be Numpy NDArray. Got {}'.format(type(img)))

    if num_output_channels == 1:
        img = A.to_gray(img)
    elif num_output_channels == 3:
        img = A.to_gray(img)
        img = np.dstack([img, img, img])
    else:
        raise ValueError('num_output_channels should be either 1 or 3')

    return img
