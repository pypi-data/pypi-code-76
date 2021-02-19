import numpy as np
from typing import Union, List, Callable
from .mpl_video import MPLVideo

# TODO: Add ffmpeg params here perhaps to call each specific writer with it's caveats.

def tryWriteVideo(video:Union[MPLVideo, np.ndarray, List], path:str, vidLib:str="imageio", count:int=5, **kwargs):
	tryWriteVideoApply(video, path, lambda video, t : video[t], vidLib, count, **kwargs)

def tryWriteVideoApply(video:Union[MPLVideo, np.ndarray, List], path:str, \
	applyFn:Callable[[MPLVideo, int], np.ndarray], vidLib:str="imageio", count:int=5, **kwargs):

	assert vidLib in ("imageio", "opencv")
	if vidLib == "imageio":
		from .libs.imageio import writeVideo
	elif vidLib == "opencv":
		from .libs.opencv import writeVideo

	if isinstance(video, (np.ndarray, List)):
		assert "fps" in kwargs
		video:MPLVideo = MPLVideo(video, kwargs["fps"])

	i = 0
	while True:
		try:
			writeVideo(video, path, applyFn, **kwargs)
			return
		except Exception as e:
			print("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception
