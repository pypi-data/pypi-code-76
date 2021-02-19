import numpy as np
from typing import Callable

def imgResize_black_bars(data:np.ndarray, height:int, width:int, interpolation:str, \
	resizeFn:Callable, returnCoordinates:bool=False, **kwargs):
	desiredShape = (height, width) if len(data.shape) == 2 else (height, width, data.shape[-1])

	imgH, imgW = data.shape[0 : 2]
	desiredH, desiredW = desiredShape[0 : 2]
	# Early return
	if desiredH == imgH and desiredW == imgW:
		return data.copy()

	# Find the rapports between the imgH/desiredH and imgW/desiredW
	rH, rW = imgH / desiredH, imgW / desiredW

	# Find which one is the highest, that one will be used
	maxRapp = max(rH, rW)
	assert maxRapp != 0, "Cannot convert data of shape %s to (%d, %d)" % (data.shape, height, width)

	# Compute the new dimensions, based on the highest rapport
	scaledH, scaledW = int(imgH / maxRapp), int(imgW / maxRapp)
	assert scaledH != 0 and scaledW != 0, "Cannot convert data of shape %s to (%d, %d)" % (data.shape, height, width)

	resizedData = resizeFn(data, scaledH, scaledW, interpolation, **kwargs)
	# Also, find the half, so we can insert the other dimension from the half
	# Insert the resized image in the original image, halving the larger dimension and keeping half black bars in
	#  each side
	newData = np.zeros(desiredShape, dtype=data.dtype)
	halfH, halfW = int((desiredH - scaledH) / 2), int((desiredW - scaledW) / 2)
	newData[halfH : halfH + scaledH, halfW : halfW + scaledW] = resizedData

	if returnCoordinates:
		x0, y0, x1, y1 = halfW, halfH, halfW + scaledW, halfH + scaledH
		return newData, (x0, y0, x1, y1)
	else:
		return newData