import numpy as np
from functools import partial

# @brief Generic function to resize ONE 2D image of shape (H, W) or 3D of shape (H, W, D) into (height, width [, D])
# @param[in] data Image (or any 2D/3D array)
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
# @param[in] resizeLib The library used for resizing
# @param[in] onlyUint8 If true, only [0-255] images are allowed. Otherwise, let the resizeLib work the provided dtype.
# @return Resized image.
def imgResize(data, height, width, interpolation, resizeLib="opencv", onlyUint8=True):
	if onlyUint8 == True:
		assert data.dtype == np.uint8, "Data dtype: %s. Use onlyUint8=False." % data.dtype
	currentHeight, currentWidth = data.shape[0], data.shape[1]
	# If we provide width only, height is infered to keep image scale
	assert (height is None) + (width is None) < 2, "Both width and height cannot be infered. Provide at least one."
	if height is None:
		assert not width is None
		height = currentHeight / currentWidth * width

	if width is None:
		assert not height is None
		width = currentWidth / currentHeight * height

	# Early return.
	height, width = int(height), int(width)
	if currentHeight == height and currentWidth == width:
		return data.copy()

	func = {
		"skimage" : resize_skimage,
		"lycon" : resize_lycon,
		"opencv" : resize_opencv,
		"pillow" : resize_pillow,
		"PIL" : resize_pillow
	}[resizeLib]

	return func(data, height, width, interpolation)

def resize_pillow(data, height, width, interpolation):
	from PIL import Image
	assert data.dtype == np.uint8
	assert isinstance(height, int) and isinstance(width, int)
	imgData = Image.fromarray(data)

	# As per: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize
	resample = {
		"nearest" : Image.NEAREST,
		"bilinear" : Image.BILINEAR,
		"bicubic" : Image.BICUBIC,
		"lanczos" : Image.LANCZOS
	}[interpolation]

	imgResized = imgData.resize(size=(width, height), resample=resample)
	npImgResized = np.array(imgResized, dtype=data.dtype)
	return npImgResized

def resize_opencv(data, height, width, interpolation):
	import cv2
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
	interpolation = {
		"nearest" : cv2.INTER_NEAREST,
		"bilinear" : cv2.INTER_LINEAR,
		"area" : cv2.INTER_AREA,
		"bicubic" : cv2.INTER_CUBIC,
		"lanczos" : cv2.INTER_LANCZOS4
	}[interpolation]
	imgResized = cv2.resize(data, dsize=(width, height), interpolation=interpolation)
	return imgResized.astype(data.dtype)

def resize_skimage(data, height, width, interpolation):
	from skimage.transform import resize
	assert interpolation in ("nearest", "bilinear", "cubic", "quadratic", "quartic", "quintic")
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.warp
	order = {
		"nearest" : 0,
		"bilinear" : 1,
		"biquadratic" : 2,
		"bicubic" : 3,
		"biquartic" : 4,
		"biquintic" : 5
	}[interpolation]
	imgResized = resize(data, output_shape=(height, width), order=order, preserve_range=True)
	return imgResized.astype(data.dtype)

# @brief Lycon based image resizing function
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation method. Valid options: bilinear, nearest, cubic, lanczos, area
# @return Resized image.
def resize_lycon(data, height, width, interpolation):
	from lycon import resize as resizeFn, Interpolation
	assert interpolation in ("bilinear", "nearest", "cubic")
	assert isinstance(height, int) and isinstance(width, int)

	# As per: https://github.com/ethereon/lycon/blob/046e9fab906b3d3d29bbbd3676b232bd0bc82787/perf/benchmark.py#L57
	interpolationTypes = {
		"bilinear" : Interpolation.LINEAR,
		"nearest" : Interpolation.NEAREST,
		"bicubic" : Interpolation.CUBIC,
		"lanczos" : Interpolation.LANCZOS,
		"area" : Interpolation.AREA
	}

	interpolationType = interpolationTypes[interpolation]
	imgResized = resizeFn(data, height=height, width=width, interpolation=interpolationType)
	return imgResized.astype(data.dtype)

def imgResize_black_bars(data, height, width, interpolation, resizeLib="opencv", onlyUint8=True):
	# No need to do anything if shapes are identical.
	assert len(data.shape) in (2, 3)
	assert isinstance(height, int) and isinstance(width, int)
	if data.shape[0] == height and data.shape[1] == width:
		return np.copy(data)

	desiredShape = (height, width) if len(data.shape) == 2 else (height, width, data.shape[-1])

	imgH, imgW = data.shape[0 : 2]
	desiredH, desiredW = desiredShape[0 : 2]

	# Find the rapports between the imgH/desiredH and imgW/desiredW
	rH, rW = imgH / desiredH, imgW / desiredW

	# Find which one is the highest, that one will be used
	maxRapp = max(rH, rW)
	assert maxRapp != 0, "Cannot convert data of shape %s to (%d, %d)" % (data.shape, height, width)

	# Compute the new dimensions, based on the highest rapport
	scaledH, scaledW = int(imgH // maxRapp), int(imgW // maxRapp)
	assert scaledH != 0 and scaledW != 0, "Cannot convert data of shape %s to (%d, %d)" % (data.shape, height, width)
	resizedData = imgResize(data, height=scaledH, width=scaledW, interpolation=interpolation, \
		resizeLib=resizeLib, onlyUint8=onlyUint8)

	# Also, find the half, so we can insert the other dimension from the half
	# Insert the resized image in the original image, halving the larger dimension and keeping half black bars in
	#  each side
	newData = np.zeros(desiredShape, dtype=data.dtype)
	halfH, halfW = int((desiredH - scaledH) // 2), int((desiredW - scaledW) // 2)
	newData[halfH : halfH + scaledH, halfW : halfW + scaledW] = resizedData
	return newData

# @brief Resizes a batch of data of shape: BxHxW(xD) to a desired shape of BxdWxdH(xD)
# @param[in] height Desired resulting height
# @param[in] width Desired resulting width
# @param[in] interpolation Interpolation method. Valid options: bilinear, nearest, cubic
# @param[in] mode What type of resizing to do. Valid values: default (can break proportions) or black_bars.
def imgResize_batch(data, height, width, interpolation="bilinear", mode="default", resizeLib="opencv", onlyUint8=True):
	assert len(data[0].shape) in (2, 3), "Got: %s" % data.shape
	assert mode in ("default", "black_bars")
	N = len(data)
	assert N > 0

	resizeFunc = {
		"default" : imgResize,
		"black_bars" : imgResize_black_bars
	}[mode]

	# Let the imgResize/imgResize_black_bars infer the height/width if not provided (i.e. autosclaing for imgResize)
	firstResult = resizeFunc(data[0], height=height, width=width, interpolation=interpolation, \
		resizeLib=resizeLib, onlyUint8=onlyUint8)
	newData = np.zeros((N, *firstResult.shape), dtype=data[0].dtype)
	newData[0] = firstResult
	for i in range(1, N):
		result = resizeFunc(data[i], height=height, width=width, interpolation=interpolation, \
			resizeLib=resizeLib, onlyUint8=onlyUint8)
		newData[i] = result
	return newData