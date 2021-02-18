# -*- coding: utf-8 -*-

"""
@date: 2021/1/12 下午2:25
@file: cls_functional.py
@author: zj
@description: 
"""

import torch
import math
import cv2
import imgaug as ia
from imgaug import augmenters as iaa

import numpy as np
from numpy import sin, cos, tan
import numbers
from collections.abc import Sequence, Iterable
import warnings


def _is_numpy(img):
    return isinstance(img, np.ndarray)


def _is_numpy_image(img):
    return img.ndim in {2, 3}


def to_tensor(pic):
    """Convert a  ``numpy.ndarray`` to tensor.

    See ``ToTensor`` for more details.

    Args:
        pic (numpy.ndarray): Image to be converted to tensor.

    Returns:
        Tensor: Converted image.
    """
    if not _is_numpy(pic):
        raise TypeError('pic should be ndarray. Got {}'.format(type(pic)))

    if _is_numpy(pic) and not _is_numpy_image(pic):
        raise ValueError('pic should be 2/3 dimensional. Got {} dimensions.'.format(pic.ndim))

    # handle numpy array
    if pic.ndim == 2:
        pic = pic[:, :, None]

    img = torch.from_numpy(pic.transpose((2, 0, 1)))
    # backward compatibility
    if isinstance(img, torch.ByteTensor):
        return img.float().div(255)
    else:
        return img


def to_numpy_image(pic):
    """Convert a tensor to ``numpy.ndarray``

    Args:
        pic (tesnor): Image to be converted to numpy.

    Returns:
        numpy.ndarray: Converted image.
    """
    if not isinstance(pic, torch.Tensor):
        raise TypeError('pic should be tensor. Got {}'.format(type(pic)))

    assert pic.dim() == 3
    npimg = pic
    if pic.is_floating_point():
        pic = pic.mul(255).byte()
    npimg = np.transpose(pic.cpu().numpy(), (1, 2, 0))
    return npimg


def normalize(tensor, mean, std, inplace=False):
    """Normalize a tensor image with mean and standard deviation.

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    See :class:`~torchvision.transforms.Normalize` for more details.

    Args:
        tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool,optional): Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """
    if not torch.is_tensor(tensor):
        raise TypeError('tensor should be a torch tensor. Got {}.'.format(type(tensor)))

    if tensor.ndimension() != 3:
        raise ValueError('Expected tensor to be a tensor image of size (C, H, W). Got tensor.size() = '
                         '{}.'.format(tensor.size()))

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    if (std == 0).any():
        raise ValueError('std evaluated to zero after conversion to {}, leading to division by zero.'.format(dtype))
    if mean.ndim == 1:
        mean = mean[:, None, None]
    if std.ndim == 1:
        std = std[:, None, None]
    tensor.sub_(mean).div_(std)
    return tensor


def resize(img, size, interpolation=None):
    r"""Resize the input Numpy Image to the given size.

    Args:
        img (Numpy Image): Image to be resized.
        size (sequence or int): Desired output size. If size is a sequence like
            (h, w), the output size will be matched to this. If size is an int,
            the smaller edge of the image will be matched to this number maintaing
            the aspect ratio. i.e, if height > width, then image will be rescaled to
            :math:`\left(\text{size} \times \frac{\text{height}}{\text{width}}, \text{size}\right)`
        interpolation (int, optional): If ``None``, the interpolation will be chosen automatically. For size
        increases, ``area`` interpolation will be picked and for size
        decreases, ``linear`` interpolation will be picked.

    Returns:
        Numpy Image: Resized image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))
    if not isinstance(size, (int, Sequence)):
        raise TypeError("Size should be int or sequence. Got {}".format(type(size)))
    if isinstance(size, Sequence) and len(size) not in (1, 2):
        raise ValueError("If size is a sequence, it should have 1 or 2 values")
    if isinstance(size, Sequence) and len(size) == 1:
        size = size[0]

    h, w = img.shape[:2]
    if isinstance(size, int):
        if (w <= h and w == size) or (h <= w and h == size):
            return img
        if w < h:
            ow = size
            oh = int(size * h / w)
        else:
            oh = size
            ow = int(size * w / h)
    else:
        oh, ow = size
    if interpolation is None:
        interpolation = cv2.INTER_AREA if (w * h) < (ow * oh) else cv2.INTER_AREA
    return ia.imresize_single_image(img, (oh, ow), interpolation=interpolation)


def scale(*args, **kwargs):
    warnings.warn("The use of the transforms.Scale transform is deprecated, " +
                  "please use transforms.Resize instead.")
    return resize(*args, **kwargs)


def pad(img, padding, fill=0, padding_mode='constant'):
    r"""Pad the given Numpy Image on all sides with specified padding mode and fill value.

    Args:
        img (Numpy Image): Image to be padded.
        padding (int or tuple): Padding on each border. If a single int is provided this
            is used to pad all borders. If tuple of length 2 is provided this is the padding
            on left/right and top/bottom respectively. If a tuple of length 4 is provided
            this is the padding for the left, top, right and bottom borders
            respectively.
        fill: Pixel fill value for constant fill. Default is 0. If a tuple of
            length 3, it is used to fill R, G, B channels respectively.
            This value is only used when the padding_mode is constant
        padding_mode: Type of padding. Should be: constant, edge, reflect or symmetric. Default is constant.

            - constant: pads with a constant value, this value is specified with fill

            - edge: pads with the last value on the edge of the image

            - reflect: pads with reflection of image (without repeating the last value on the edge)

                       padding [1, 2, 3, 4] with 2 elements on both sides in reflect mode
                       will result in [3, 2, 1, 2, 3, 4, 3, 2]

            - symmetric: pads with reflection of image (repeating the last value on the edge)

                         padding [1, 2, 3, 4] with 2 elements on both sides in symmetric mode
                         will result in [2, 1, 1, 2, 3, 4, 4, 3]

    Returns:
        Numpy Image: Padded image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    if not isinstance(padding, (numbers.Number, tuple)):
        raise TypeError('Got inappropriate padding arg')
    if not isinstance(fill, (numbers.Number, str, tuple)):
        raise TypeError('Got inappropriate fill arg')
    if not isinstance(padding_mode, str):
        raise TypeError('Got inappropriate padding_mode arg')

    if isinstance(padding, Sequence) and len(padding) not in [2, 4]:
        raise ValueError("Padding must be an int or a 2, or 4 element tuple, not a " +
                         "{} element tuple".format(len(padding)))

    assert padding_mode in ['constant', 'edge', 'reflect', 'symmetric'], \
        'Padding mode should be either constant, edge, reflect or symmetric'

    # if padding_mode == 'constant':
    #     aug = iaa.Pad(px=padding, pad_mode=padding_mode, pad_cval=fill, keep_size=False)
    #     return aug.augment_image(img)
    # else:
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

    aug = iaa.CropAndPad(px=(pad_top, pad_right, pad_bottom, pad_left), pad_mode=padding_mode, pad_cval=fill,
                         keep_size=False)
    # aug = iaa.CropAndPad(px=(pad_top, pad_right, pad_bottom, pad_left), pad_mode=padding_mode, keep_size=False)
    return aug.augment_image(img)

    # # RGB image
    # if len(img.shape) == 3:
    #     aug = iaa.Pad(px=((pad_top, pad_bottom), (pad_left, pad_right)),
    #                   pad_mode=padding_mode, keep_size=False)
    #     return aug.augment_image(img)
    # # Grayscale image
    # if len(img.shape) == 2:
    #     aug = iaa.Pad(px=((pad_top, pad_bottom), (pad_left, pad_right)),
    #                   pad_mode=padding_mode, keep_size=False)
    #     return aug.augment_image(img)

    # return img


def crop(img, top, left, height, width):
    """Crop the given Numpy Image.

    Args:
        img (Numpy Image): Image to be cropped. (0,0) denotes the top left corner of the image.
        top (int): Vertical component of the top left corner of the crop box.
        left (int): Horizontal component of the top left corner of the crop box.
        height (int): Height of the crop box.
        width (int): Width of the crop box.

    Returns:
        Numpy Image: Cropped image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    return img[top:top + height, left:left + width]


def center_crop(img, output_size):
    """Crop the given Numpy Image and resize it to desired size.

    Args:
        img (Numpy Image): Image to be cropped. (0,0) denotes the top left corner of the image.
        output_size (sequence or int): (height, width) of the crop box. If int,
            it is used for both directions
    Returns:
        Numpy Image: Cropped image.
    """
    if isinstance(output_size, numbers.Number):
        output_size = (int(output_size), int(output_size))
    image_height, image_width = img.shape[:2]
    crop_height, crop_width = output_size
    crop_top = int(round((image_height - crop_height) / 2.))
    crop_left = int(round((image_width - crop_width) / 2.))
    return crop(img, crop_top, crop_left, crop_height, crop_width)


def resized_crop(img, top, left, height, width, size, interpolation=cv2.INTER_LINEAR):
    """Crop the given Numpy Image and resize it to desired size.

    Notably used in :class:`~torchvision.transforms.RandomResizedCrop`.

    Args:
        img (Numpy Image): Image to be cropped. (0,0) denotes the top left corner of the image.
        top (int): Vertical component of the top left corner of the crop box.
        left (int): Horizontal component of the top left corner of the crop box.
        height (int): Height of the crop box.
        width (int): Width of the crop box.
        size (sequence or int): Desired output size. Same semantics as ``resize``.
        interpolation (int, optional): Desired interpolation. Default is
            ``cv2.INTER_LINEAR``.
    Returns:
        Numpy Image: Cropped image.
    """
    assert _is_numpy(img), 'img should be Numpy Image'
    img = crop(img, top, left, height, width)
    img = resize(img, size, interpolation)
    return img


def hflip(img):
    """Horizontally flip the given Numpy Image.

    Args:
        img (Numpy Image): Image to be flipped.

    Returns:
        Numpy Image:  Horizontall flipped image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    return np.fliplr(img)


def _get_perspective_coeffs(startpoints, endpoints):
    """
    已知开始坐标和变换坐标，计算透视矩阵
    Args:
        List containing [top-left, top-right, bottom-right, bottom-left] of the orignal image,
        List containing [top-left, top-right, bottom-right, bottom-left] of the transformed
                   image
    Returns:
        透视矩阵
    """
    M = cv2.getPerspectiveTransform(np.float32(startpoints), np.float32(endpoints))
    return M


def perspective(img, startpoints, endpoints, interpolation=cv2.INTER_LINEAR, fill=None):
    """Perform perspective transform of the given Numpy Image.

    Args:
        img (Numpy Image): Image to be transformed.
        startpoints: List containing [top-left, top-right, bottom-right, bottom-left] of the orignal image
        endpoints: List containing [top-left, top-right, bottom-right, bottom-left] of the transformed image
        interpolation: Default- cv2.INTER_LINEAR
        fill (n-tuple or int or float): Pixel fill value for area outside the rotated
            image. If int or float, the value is used for all bands respectively.

    Returns:
        Numpy Image:  Perspectively transformed Image.
    """

    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    height, width = img.shape[:2]
    M = _get_perspective_coeffs(startpoints, endpoints)
    return cv2.warpPerspective(img, M, (width, height), flags=interpolation, borderValue=fill)


def vflip(img):
    """Vertically flip the given Numpy Image.

    Args:
        img (Numpy Image): Image to be flipped.

    Returns:
        Numpy Image:  Vertically flipped image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    return np.flipud(img)


def five_crop(img, size):
    """Crop the given Numpy Image into four corners and the central crop.

    .. Note::
        This transform returns a tuple of images and there may be a
        mismatch in the number of inputs and targets your ``Dataset`` returns.

    Args:
       size (sequence or int): Desired output size of the crop. If size is an
           int instead of sequence like (h, w), a square crop (size, size) is
           made.

    Returns:
       tuple: tuple (tl, tr, bl, br, center)
                Corresponding top left, top right, bottom left, bottom right and center crop.
    """
    if isinstance(size, numbers.Number):
        size = (int(size), int(size))
    else:
        assert len(size) == 2, "Please provide only two dimensions (h, w) for size."

    image_height, image_width = img.shape[:2]
    crop_height, crop_width = size
    if crop_width > image_width or crop_height > image_height:
        msg = "Requested crop size {} is bigger than input size {}"
        raise ValueError(msg.format(size, (image_height, image_width)))

    tl = crop(img, 0, 0, crop_height, crop_width)
    tr = crop(img, 0, image_width - crop_width, crop_height, crop_width)
    bl = crop(img, image_height - crop_height, 0, crop_height, crop_width)
    br = crop(img, image_height - crop_height, image_width - crop_width, crop_height, crop_width)
    center = center_crop(img, (crop_height, crop_width))
    return (tl, tr, bl, br, center)


def ten_crop(img, size, vertical_flip=False):
    """Generate ten cropped images from the given Numpy Image.
    Crop the given Numpy Image into four corners and the central crop plus the
    flipped version of these (horizontal flipping is used by default).

    .. Note::
        This transform returns a tuple of images and there may be a
        mismatch in the number of inputs and targets your ``Dataset`` returns.

    Args:
        size (sequence or int): Desired output size of the crop. If size is an
            int instead of sequence like (h, w), a square crop (size, size) is
            made.
        vertical_flip (bool): Use vertical flipping instead of horizontal

    Returns:
        tuple: tuple (tl, tr, bl, br, center, tl_flip, tr_flip, bl_flip, br_flip, center_flip)
            Corresponding top left, top right, bottom left, bottom right and
            center crop and same for the flipped image.
    """
    if isinstance(size, numbers.Number):
        size = (int(size), int(size))
    else:
        assert len(size) == 2, "Please provide only two dimensions (h, w) for size."

    first_five = five_crop(img, size)

    if vertical_flip:
        img = vflip(img)
    else:
        img = hflip(img)

    second_five = five_crop(img, size)
    return first_five + second_five


def adjust_brightness(img, brightness_factor):
    """Adjust brightness of an Image.

    Args:
        img (Numpy Image): Numpy Image to be adjusted.
        brightness_factor (int):  How much to adjust the brightness. Can be
            any non negative number. 0 gives a black image, 1 gives the
            original image while 2 increases the brightness by a factor of 2.

    Returns:
        Numpy Image: Brightness adjusted image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    if brightness_factor < 1 or brightness_factor > 5:
        raise ValueError(
            f'brightness_factor({brightness_factor}) is outside of the expected value range (1 <= x <= 5)')

    aug = iaa.imgcorruptlike.Brightness(severity=brightness_factor)
    img = aug.augment_image(img)
    return img


def adjust_contrast(img, contrast_factor):
    """Adjust contrast of an Image.

    Args:
        img (Numpy Image): Numpy Image to be adjusted.
        contrast_factor (int): How much to adjust the contrast.
            the expected value range (1 <= x <= 5).
            1 gives the original image while 2 increases the contrast by a factor of 2.

    Returns:
        Numpy Image: Contrast adjusted image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    if contrast_factor < 1 or contrast_factor > 5:
        raise ValueError(
            f'contrast_factor({contrast_factor}) is outside of the expected value range (1 <= x <= 5)')

    aug = iaa.imgcorruptlike.Contrast(severity=contrast_factor)
    img = aug.augment_image(img)
    return img


def adjust_saturation(img, saturation_factor):
    """Adjust color saturation of an image.

    Args:
        img (Numpy Image): Numpy Image to be adjusted.
        saturation_factor (int):  How much to adjust the saturation.
            the expected value range (1 <= x <= 5).
            1 will give the original image while
            2 will enhance the saturation by a factor of 2.

    Returns:
        Numpy Image: Saturation adjusted image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    if saturation_factor < 1 or saturation_factor > 5:
        raise ValueError(
            f'saturation_factor({saturation_factor}) is outside of the expected value range (1 <= x <= 5)')

    aug = iaa.imgcorruptlike.Saturate(severity=saturation_factor)
    img = aug.augment_image(img)
    return img


def adjust_hue(img, hue_factor):
    """Adjust hue of an image.

    The image hue is adjusted by converting the image to HSV and
    cyclically shifting the intensities in the hue channel (H).
    The image is then converted back to original image mode.

    `hue_factor` is the amount of shift in H channel

    See `Hue`_ for more details.

    .. _Hue: https://en.wikipedia.org/wiki/Hue

    Args:
        img (Numpy Image): Numpy Image to be adjusted.
        hue_factor (int):  How much to shift the hue channel.
            This is expected to be in the range -255 to +255
            5 and -5 give complete reversal of hue channel in
            HSV space in positive and negative direction respectively.
            0 means no shift. Therefore, both -5 and 5 will give an image
            with complementary colors while 0 gives the original image.

    Returns:
        Numpy Image: Hue adjusted image.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    if hue_factor < -255 or hue_factor > 255:
        raise ValueError(
            f'hue_factor({hue_factor}) is outside of the expected value range (-255 <= x <= 255)')

    aug = iaa.color.AddToHue(value=hue_factor, from_colorspace='RGB')
    img = aug.augment_image(img)
    return img


def rotate(img, angle):
    """Rotate the image by angle.


    Args:
        img (Numpy Image): Numpy Image to be rotated.
        angle (float or int): In degrees degrees counter clockwise order.

    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    aug = iaa.Affine(rotate=angle)
    return aug.augment_image(img)


def affine(img, angle, translate, scale, shear):
    """Apply affine transformation on the image keeping image center invariant

    Args:
        img (Numpy Image): Numpy Image to be rotated.
        angle (float or int): rotation angle in degrees between -180 and 180, clockwise direction.
        translate (list or tuple of integers): horizontal and vertical translations (post-rotation translation)
        scale (float): overall scale
        shear (float or tuple or list): shear angle value in degrees between -180 to 180, clockwise direction.
        If a tuple of list is specified, the first value corresponds to a shear parallel to the x axis, while
        the second value corresponds to a shear parallel to the y axis.
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))

    assert isinstance(translate, (tuple, list)) and len(translate) == 2, \
        "Argument translate should be a list or tuple of length 2"

    assert scale > 0.0, "Argument scale should be positive"

    aug = iaa.Affine(scale=scale, rotate=angle, translate_px=translate, shear=shear)
    return aug.augment_image(img)


def to_grayscale(img, num_output_channels=1):
    """Convert image to grayscale version of image.

    Args:
        img (Numpy Image): Image to be converted to grayscale.

    Returns:
        Numpy Image: Grayscale version of the image.
            if num_output_channels = 1 : returned image is single channel

            if num_output_channels = 3 : returned image is 3 channel with r = g = b
    """
    if not _is_numpy(img):
        raise TypeError('img should be Numpy Image. Got {}'.format(type(img)))
    if num_output_channels not in (1, 3):
        raise ValueError('num_output_channels should be either 1 or 3')

    aug = iaa.Grayscale(alpha=1.0)
    img = aug.augment_image(img)
    if num_output_channels == 1:
        return img[:, :, 0]
    if num_output_channels == 3:
        return img


def erase(img, i, j, h, w, v, inplace=False):
    """ Erase the input Tensor Image with given value.

    Args:
        img (Tensor Image): Tensor image of size (C, H, W) to be erased
        i (int): i in (i,j) i.e coordinates of the upper left corner.
        j (int): j in (i,j) i.e coordinates of the upper left corner.
        h (int): Height of the erased region.
        w (int): Width of the erased region.
        v: Erasing value.
        inplace(bool, optional): For in-place operations. By default is set False.

    Returns:
        Tensor Image: Erased image.
    """
    if not isinstance(img, torch.Tensor):
        raise TypeError('img should be Tensor Image. Got {}'.format(type(img)))

    if not inplace:
        img = img.clone()

    img[:, i:i + h, j:j + w] = v
    return img
