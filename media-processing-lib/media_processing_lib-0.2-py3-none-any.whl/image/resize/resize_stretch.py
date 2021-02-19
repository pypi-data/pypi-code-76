import numpy as np
from typing import Callable

def imgResize_stretch(data:np.ndarray, height:int, width:int, interpolation:str, resizeFn:Callable, **kwargs):
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

	return resizeFn(data, height, width, interpolation, **kwargs)
