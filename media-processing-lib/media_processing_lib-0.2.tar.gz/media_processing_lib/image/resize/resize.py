import numpy as np
from functools import partial

# @brief Generic function to resize ONE 2D image of shape (H, W) or 3D of shape (H, W, D) into (height, width [, D])
# @param[in] data Image (or any 2D/3D array)
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
# @param[in] mode Whether to stretch the image or apply black bars around it to preserve scaling.
# @param[in] resizeLib The library used for resizing
# @param[in] onlyUint8 If true, only [0-255] images are allowed. Otherwise, let the resizeLib work the provided dtype.
# @return Resized image.
def imgResize(data:np.ndarray, height:int, width:int, interpolation:str="bilinear", mode:str="stretch", \
	resizeLib:str="opencv", onlyUint8:bool=True, **kwargs):
	assert len(data.shape) in (2, 3)
	if onlyUint8 == True:
		assert data.dtype == np.uint8, "Data dtype: %s. Use onlyUint8=False." % data.dtype

	if mode == "stretch":
		from .resize_stretch import imgResize_stretch
		resizeFn = imgResize_stretch
	elif mode == "black_bars":
		from .resize_black_bars import imgResize_black_bars
		resizeFn = imgResize_black_bars
	else:
		assert False, mode

	if resizeLib == "skimage":
		from ..libs.skimage import resizeImage
	elif resizeLib == "lycon":
		from ..libs.lycon import resizeImage
	elif resizeLib in ("pillow", "PIL"):
		from ..libs.pil import resizeImage
	elif resizeLib == "opencv":
		from ..libs.opencv import resizeImage
	else:
		assert False, resizeLib

	resizedData = resizeFn(data, height, width, interpolation, resizeImage, **kwargs)
	return resizedData

# @brief Generic function to resize a batch of images of shape BxHxW(xD) to a desired shape of BxdWxdH(xD)
# @param[in] data batch of images (or any 2D/3D array)
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
# @param[in] mode Whether to stretch the image or apply black bars around it to preserve scaling.
# @param[in] resizeLib The library used for resizing
# @param[in] onlyUint8 If true, only [0-255] images are allowed. Otherwise, let the resizeLib work the provided dtype.
# @return Resized batch of images.
def imgResize_batch(data:np.ndarray, height:int, width:int, interpolation:str="bilinear", mode:str="stretch", \
	resizeLib:str="opencv", onlyUint8:bool=True, **kwargs):
	N = len(data)
	assert N > 0

	# Let the imgResize/imgResize_black_bars infer the height/width if not provided (i.e. autosclaing for imgResize)
	firstResult = imgResize(data[0], height=height, width=width, interpolation=interpolation, \
		mode=mode, resizeLib=resizeLib, onlyUint8=onlyUint8, **kwargs)
	newData = np.zeros((N, *firstResult.shape), dtype=data[0].dtype)
	newData[0] = firstResult
	for i in range(1, N):
		result = imgResize(data[i], height=height, width=width, interpolation=interpolation, \
			mode=mode, resizeLib=resizeLib, onlyUint8=onlyUint8, **kwargs)
		newData[i] = result
	return newData