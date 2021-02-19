import numpy as np

def computeIntrinsics(fieldOfView:int, height:int, width:int, skew:float=0):
	cy = height / 2
	cx = width / 2
	fy = cy / (np.tan(fieldOfView * np.pi / 360))
	fx = cx / (np.tan(fieldOfView * np.pi / 360))

	K = np.array([
		[fx, skew, cx],
		[0, fy, cy],
		[0, 0, 1]
	], dtype=np.float32)
	return K
