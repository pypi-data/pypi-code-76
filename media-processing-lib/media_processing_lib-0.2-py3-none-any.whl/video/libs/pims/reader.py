import pims
from typing import Tuple, List, Optional
from ....utils import dprint

def readRaw(path:str, nFrames:Optional[int]) -> Tuple[pims.Video, int, List[int], int]:
	dprint("[mpl::video::pims] Reading raw data.")

	video = pims.Video(path)
	fps = video.frame_rate
	data = video
	if nFrames == None:
		nFrames = len(video)
	shape = (nFrames, *video.frame_shape)
	return data, fps, shape, nFrames