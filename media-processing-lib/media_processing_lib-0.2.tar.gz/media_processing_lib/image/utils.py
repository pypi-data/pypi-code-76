import numpy as np

# @brief Generic NumPy to plottable image uint8 [0 : 255] image. Basically, turns the image in [0:1] and float32,
#  applies minMax, does some stuff about potential shapes being wrong, converts image to [0:255] and to uint8.
# @param[in] x A NumPy array that ist o be converted to [0 : 255] image
# @param[in] A NumPy array that represents the [0 : 255] image version of the original array.
def toImage(x:np.ndarray):
	x = np.array(x)
	x = x.astype(np.float32)
	Min, Max = x.min(), x.max()
	x = (x - Min) / (Max - Min + np.spacing(1))
	if len(x.shape) == 2:
		x = np.expand_dims(x, axis=-1)
	if x.shape[0] in (1, 3):
		x = x.transpose(1, 2, 0)
	if x.shape[-1] == 1:
		x = np.concatenate([x, x, x], axis=-1)
	if x.shape[-1] == 4:
		x = x[..., 0 : 3]
	x = np.clip(x, 0, 1) * 255
	x = x.astype(np.uint8)
	return x
