import numpy as np
from typing import Union, List, Callable
from .mpl_audio import MPLAudio

def tryWriteAudio(audio:Union[MPLAudio, np.ndarray, List], path:str, \
	audioLib:str="soundfile", count:int=5, **kwargs):
	import soundfile

	assert audioLib in ("soundfile", )
	if audioLib == "soundfile":
		from .libs.soundfile import writeAudio

	if isinstance(audio, (np.ndarray, List)):
		assert "sampleRate" in kwargs
		audio = MPLAudio(audio, kwargs["sampleRate"])

	i = 0
	while True:
		try:
			writeAudio(audio, path, **kwargs)
			return
		except Exception as e:
			print("Path: %s. Exception: %s" % (path, e))
			i += 1

			if i == count:
				raise Exception
