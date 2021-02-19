import numpy as np
from typing import Optional
import ffmpeg

from .mpl_video import MPLVideo
from ..utils import dprint

def isRotated90(path, data, shape):
	ix = []
	f = ffmpeg.probe(path)
	for i, stream in enumerate(f["streams"]):
		if ("codec_type" in stream) and (stream["codec_type"] == "video"):
			ix.append(i)
	assert len(ix) == 1
	stream = f["streams"][ix[0]]

	# Other weird cases ? We'll see...
	if (not "tags" in stream) or (not "rotate" in stream["tags"]):
		return False

	if stream["tags"]["rotate"] != "90":
		return False

	# Some good shit happening here.
	strType = str(type(data)).split(".")[-1][0:-2]
	# Basically, ImageIOReader decided to transpose it by default for us.
	if strType == "ImageIOReader":
		return False
	# PyAVTimedReader decided to not transpose it at all.
	elif strType == "PyAVReaderTimed":
		return True
	# We'll see for other cases... we assume to it is not transposed.
	return True

def tryReadVideo(path:str, vidLib:str="imageio", count:int=5, nFrames:Optional[int]=None) -> MPLVideo:
	extension = path.lower().split(".")[-1]
	assert extension in ("gif", "mp4", "mov", "mkv")
	assert vidLib in ("imageio", "pims", "opencv")

	if vidLib == "pims":
		from .libs.pims import readRaw as readFn
	elif vidLib == "imageio":
		from .libs.imageio import readRaw as readFn
	elif vidLib == "opencv":
		from .libs.opencv import readRaw as readFn

	i = 0
	while True:
		try:
			data, fps, shape, nFrames = readFn(path, nFrames)
			isPortrait = isRotated90(path, data, shape)
			assert len(shape) == 4
			video = MPLVideo(data, fps, isPortrait, shape, nFrames)
			dprint("[mpl::tryReadVideo] Read video %s. Shape: %s. FPS: %2.3f. Portrait: %s" % \
				(path, str(video.shape), video.fps, isPortrait))
			return video
		except Exception as e:
			dprint("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception(e)
