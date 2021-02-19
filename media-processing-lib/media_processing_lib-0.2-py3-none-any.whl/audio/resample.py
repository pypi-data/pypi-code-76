import numpy as np
from .mpl_audio import MPLAudio

def resample(audio:MPLAudio, sampleRate:int):
    # Lazily use NumPy for this task
    newLen = int(len(audio.data) / audio.sampleRate * sampleRate)
    xVal = np.arange(0, newLen)
    xp = np.arange(0, len(audio.data))
    newData = np.interp(xVal, xp, audio.data)
    return MPLAudio(newData, sampleRate)
