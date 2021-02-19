from __future__ import annotations
import numpy as np
import os
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional
from tqdm import trange
from copy import copy
from ..utils import drange

class MPLVideo(ABC):
	def __init__(self, data:Any, fps:int, shape:Optional[Tuple[int]]=None, nFrames:Optional[int]=None):
		self.data = data
		self.nFrames = len(self.data) if nFrames is None else nFrames
		self.shape = self.data.shape if shape is None else shape
		self.fps = fps

	# @brief Creates a copy of this MPLVideo object
	# @return A copy of this video
	def copy(self) -> MPLVideo:
		return MPLVideo(copy(self.data), self.fps, self.shape, self.nFrames)

	def __getitem__(self, key):
		if isinstance(key, slice):
			assert key.step is None
			data = self.data[key]
			nFrames = key.stop - key.start
			return MPLVideo(data, self.fps, (nFrames, *self.shape[1: ]), nFrames)
		return self.data[key]

	def __setitem__(self, key, value):
		assert False, "Cannot set values to a video object. Use video.data or video[i] to get the frame."

	def __len__(self):
		return len(self.data)

	def __eq__(self, other:MPLVideo):
		return (self.nFrames == other.nFrames) and (self.shape == other.shape) \
			and (self.fps == other.fps) and (np.abs(self.data - other.data).sum() < 1e-5)

	# @brief Applies a function to each frame of the self video and creates a new video with the applied function.
	#  The callable prototype is (video, timestep) and must return a modified frame of video[timestep]
	# @return A new video where each frame is updates according to the provided callback
	def apply(self, applyFn:Callable[[MPLVideo, int], np.ndarray]) -> MPLVideo:
		N = len(self)
		firstFrame = applyFn(self, 0)
		newData = np.zeros((self.nFrames, *firstFrame.shape), dtype=np.uint8)
		newData[0] = firstFrame
		for i in drange(1, N, desc="[MPLVideo::aply]"):
			newFrame = applyFn(self, i)
			newData[i] = newFrame
		return MPLVideo(newData, self.fps, self.shape, self.nFrames)

	# @brief Saves the current video to the desired path. Calls tryWriteVideo with it's desired params, such as vidLib
	# @param[in] A path where to save this current file
	def save(self, path:str, **kwargs) -> None:
		from .video_writer import tryWriteVideo
		tryWriteVideo(self, path, **kwargs)

	def saveApply(self, path:str, applyFn:Callable[[MPLVideo, int], np.ndarray], **kwargs):
		from .video_writer import tryWriteVideoApply
		tryWriteVideoApply(self, path, applyFn, **kwargs)
