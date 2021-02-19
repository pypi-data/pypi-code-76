import imageio
import os
import numpy as np
from tqdm import trange
from typing import Callable
from ...mpl_video import MPLVideo
from ....utils import drange

def writeVideo(video:MPLVideo, path:str, applyFn:Callable[[MPLVideo, int], np.ndarray], **kwargs):
	writer = imageio.get_writer(path, fps=video.fps)
	N = len(video)

	for i in drange(N, desc="[ImageIO::writeVideo]"):
		frame = applyFn(video, i)
		writer.append_data(frame)
	writer.close()
