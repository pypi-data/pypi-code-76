import numpy as np
from imageio import get_reader
from typing import Tuple, List, Optional
from ....utils import dprint

def readRaw(path:str, nFrames:Optional[int]) -> Tuple[np.ndarray, int, List[int], int]:
	dprint("[mpl::video::imageio] Reading raw data.")

	reader = get_reader(path)
	metadata = reader.get_meta_data()

	nFrames = 1<<31 if nFrames is None else nFrames
	fps = metadata["fps"]
	
	# Make this smarter
	video = []
	for i, frame in enumerate(reader):
		if i == nFrames:
			break
		video.append(frame)
	video = np.array(video)
	nFrames = len(video)
	video = video[..., 0 : 3]

	return video, fps, video.shape, nFrames