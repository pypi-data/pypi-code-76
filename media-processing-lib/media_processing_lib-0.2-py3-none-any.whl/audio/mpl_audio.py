from __future__ import annotations
import numpy as np
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional
from tqdm import trange
from copy import copy
from ..utils import drange

class MPLAudio(ABC):
	def __init__(self, data:Any, sampleRate:int):
		self.data = data
		self.sampleRate = sampleRate
		self.shape = self.data.shape

	# @brief Creates a copy of this MPLAudio object
	# @return A copy of this video
	def copy(self) -> MPLAudio:
		return MPLAudio(copy(self.data), self.sampleRate)

	# @brief Resamples this audio object to a new sample rate
	# @return A copy of this audio with the new sample rate
	def resample(self, sampleRate:int):
		from .resample import resample
		return resample(self, sampleRate)

	# @brief Saves the current audio to the desired path. Calls tryWriteAudio with it's desired params, such as
	#  audioLib
	# @param[in] A path where to save this current file
	def save(self, path:str, **kwargs) -> None:
		from .audio_writer import tryWriteAudio
		tryWriteAudio(self, path, **kwargs)

	def __len__(self):
		return len(self.data)

	def __setitem__(self, key, value):
		assert False, "Cannot set values to an audio object. Use audio.data or audio[i] to get the value."

	def __getitem__(self, key):
		if isinstance(key, slice):
			assert key.step is None
			data = self.data[key]
			return MPLAudio(data, self.sampleRate)
		return self.data[key]

	def __str__(self):
		Str = "Audio. Shape: %s. Sample rate: %s" % (self.shape, self.sampleRate)
		return Str

	def __eq__(self, other:MPLAudio):
		# Close enough equality
		return (self.sampleRate == other.sampleRate) and (self.shape == other.shape) \
			and np.median(np.abs(self.data - other.data)) < 1e-4

	# # @brief Applies a function to each frame of the self video and creates a new video with the applied function.
	# #  The callable prototype is (video, timestep) and must return a modified frame of video[timestep]
	# # @return A new video where each frame is updates according to the provided callback
	# def apply(self, applyFn:Callable[[MPLVideo, int], np.ndarray]) -> MPLVideo:
	# 	N = len(self)
	# 	firstFrame = applyFn(self, 0)
	# 	newData = np.zeros((self.nFrames, *firstFrame.shape), dtype=np.uint8)
	# 	newData[0] = firstFrame
	# 	for i in drange(1, N, desc="[MPLVideo::aply]"):
	# 		newFrame = applyFn(self, i)
	# 		newData[i] = newFrame
	# 	return MPLVideo(newData, self.fps, self.shape, self.nFrames)
	# def saveApply(self, path:str, applyFn:Callable[[MPLVideo, int], np.ndarray], **kwargs):
	# 	from .video_writer import tryWriteVideoApply
	# 	tryWriteVideoApply(self, path, applyFn, **kwargs)

# def save_wav(wav, path, sr):
# 	wav *= 32767 / max(0.01, np.max(np.abs(wav)))
# 	#proposed by @dsmiller
# 	wavfile.write(path, sr, wav.astype(np.int16))
