#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"


"""Various useful methods for temporal simulation."""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter


# ========== SIGNAL PROCESSING ==========

def antialias(signal, dt, cutoff_freq=18000, order=5):
    """Decimate high frequencies using a digital Butterworth filter."""
    nyq = 0.5 / dt
    normal_cutoff = cutoff_freq / nyq
    if normal_cutoff > 1:
        # Can't antialias beyond the Nyquist frequency!
        return signal
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, signal)



def resample(signal, dt, samplerate=44100, cutoff_freq=18000):
    """Change sampling rate of signal, applying anti-aliasing if needed."""
    signal = antialias(signal, dt)
    Tmax = dt*len(signal)
    ts_before = np.linspace(0,Tmax,len(signal))
    ts_after = np.arange(0,Tmax,1.0/samplerate)
    return np.interp(ts_after, ts_before, signal)


def export_mono(filename, out, ts, verbose=True):
    """Export simulation data to an audio file.

    Resamples with antialiasing, and normalizes amplitude so that the highest
    peak is at 0 dB.

    Parameters
    ----------
    filename : str
    out : array(float)
        1D array of data to export.
    ts : array(float)
        1D array of times of the simulation. We assume constant increment.
    """
    dt = ts[1] - ts[0]
    assert np.allclose(ts[1:], ts[:-1] + dt)

    samplerate=44100
    out_interp = resample(out, dt, samplerate=samplerate)

    out_interp /= np.max(np.abs(out_interp)) # Normalize to [-1,1]
    wavfile.write(filename,samplerate,out_interp)

    if verbose:
        print("Wrote audio to", filename)

