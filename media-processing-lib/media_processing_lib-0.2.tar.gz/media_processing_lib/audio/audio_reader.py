import os
import tempfile
import subprocess
import mimetypes
import warnings
import numpy as np
from typing import Optional

from ..utils import dprint
from .mpl_audio import MPLAudio

def getWavFromVideo(path:str) -> str:
	fd, tmpPath = tempfile.mkstemp(suffix=".wav")
	command = "ffmpeg -loglevel panic -y -i %s -strict -2 %s" % (path, tmpPath)
	subprocess.call(command, shell=True)
	return fd, tmpPath

# FUN FACT: Reading mp4 (videos in general?) will yield different results every time, so we can convert data to wav
#  first if mp4
def tryReadAudio(path:str, audioLib:str="librosa", count:int=5, **kwargs):
	assert audioLib in ("librosa", )
	if audioLib == "librosa":
		from .libs.librosa import readAudio

	if int(os.environ["MPL_QUIET"]) == 1:
		warnings.filterwarnings("ignore")

	isVideo = mimetypes.guess_type(path)[0].startswith("video")
	forceWav = False if ("forceWav" in kwargs) and (kwargs["forceWav"] == False) else True
	if forceWav and isVideo:
		fd, tmpPath = getWavFromVideo(path)
		dprint("[mpl::audio] Converting %s video to wav. Got path: %s" % (path, tmpPath))
		path = tmpPath

	i = 0
	while True:
		try:
			audioData, sampleRate = readAudio(path, **kwargs)
			audio = MPLAudio(audioData, sampleRate)
			dprint("[mpl::audio] Read audio %s. Shape: %s. Sample rate: %2.3f" % \
				(path, str(audio.shape), audio.sampleRate))
			if forceWav and isVideo:
				os.remove(path)
				os.close(fd)
			return audio
		except Exception as e:
			dprint("[mpl::audio] Path: %s. Exception: %s" % (path, str(e)))
			i += 1

			if i == count:
				raise Exception(e)
