from __future__ import annotations
import numpy as np
import os
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional
from tqdm import trange
from copy import copy
from ...utils import drange

class MPLVideo(ABC):
	def __init__(self, data:Any, fps:int, isPortrait:Optional[bool]=False, \
		shape:Optional[Tuple[int]]=None, nFrames:Optional[int]=None):
		self.data = data
		self.nFrames = len(self.data) if nFrames is None else nFrames
		self.baseShape = self.data.shape if shape is None else shape
		self.fps = fps
		# for the awesome technology that films in 'portrait' mode, but phones store the data as 'landscape',
		# however for all intents and purposes, we must read it as 'portrait'.
		self.isPortrait = isPortrait

	# @brief Creates a copy of this MPLVideo object
	# @return A copy of this video
	def copy(self) -> MPLVideo:
		dataCopy = copy(self.data)
		if isinstance (dataCopy, np.ndarray):
			isPortrait = False
		else:
			isPortrait = self.isPortrait
		return MPLVideo(dataCopy, self.fps, isPortrait, self.baseShape, self.nFrames)

	def __getitem__(self, key):
		if isinstance(key, slice):
			# Slicing is troubling. If the underlying reader converts it to numpy (thus accessing element by element)
			#  then it's no longer a portrait mode (but a regular one). However, if it's slicing (i.e. not accessing)
			#  then we need to make sure the data remains in portrait mode!
			assert key.step is None
			sliceData = self.data[key]
			sliceNFrames = key.stop - key.start
			sliceShape = (sliceNFrames, *self.baseShape[1 :])
			if isinstance(sliceData, np.ndarray):
				sliceIsPortrait = False
			else:
				sliceIsPortrait = self.isPortrait
			return MPLVideo(sliceData, self.fps, sliceIsPortrait, sliceShape, sliceNFrames)
		
		item = self.data[key]
		if self.isPortrait:
			# Landscape to portrait and via trapose & mirror
			item = item.transpose(1, 0, 2)
			item = np.flip(item, axis=1)
		return item

	def __setitem__(self, key, value):
		assert False, "Cannot set values to a video object. Use video.data or video[i] to get the frame."

	def __getattr__(self, key):
		if key == "shape":
			if self.isPortrait:
				N, H, W, D = self.baseShape
				return (N, W, H, D)
			else:
				return self.baseShape
		return getattr(self, key)

	def __len__(self):
		return len(self.data)

	def __eq__(self, other:MPLVideo):
		check = (self.nFrames == other.nFrames) and (self.shape == other.shape) and (self.fps == other.fps) \
			and (self.isPortrait == other.isPortrait)
		if not check:
			return False
		for i in range(len(self)):
			if not np.abs(self[i] - other[i]).sum() < 1e-5:
				return False
		return True

	# @brief Applies a function to each frame of the self video and creates a new video with the applied function.
	#  The callable prototype is (video, timestep) and must return a modified frame of video[timestep]
	# @return A new video where each frame is updates according to the provided callback
	def apply(self, applyFn:Callable[[MPLVideo, int], np.ndarray]) -> MPLVideo:
		N = len(self)
		firstFrame = applyFn(self, 0)
		newData = np.zeros((self.nFrames, *firstFrame.shape), dtype=np.uint8)
		newData[0] = firstFrame
		for i in drange(1, N, desc="[MPLVideo::apply]"):
			newFrame = applyFn(self, i)
			newData[i] = newFrame
		# Here we call MPLVideo as we basically rotate the video (in case of rotate 90) when accessing it.
		newShape = (N, *firstFrame.shape)
		return MPLVideo(newData, self.fps, isPortrait=False, shape=newShape, nFrames=self.nFrames)

	# @brief Saves the current video to the desired path. Calls tryWriteVideo with it's desired params, such as vidLib
	# @param[in] A path where to save this current file
	def save(self, path:str, **kwargs) -> None:
		from ..video_writer import tryWriteVideo
		tryWriteVideo(self, path, **kwargs)

	def saveApply(self, path:str, applyFn:Callable[[MPLVideo, int], np.ndarray], **kwargs):
		from ..video_writer import tryWriteVideoApply
		tryWriteVideoApply(self, path, applyFn, **kwargs)
