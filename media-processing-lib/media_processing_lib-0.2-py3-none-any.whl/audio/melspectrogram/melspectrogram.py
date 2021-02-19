import librosa
import numpy as np
from scipy import signal

class HParams:
	def __init__(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, v)

hp = HParams(
	n_fft=800,  # Extra window size is filled with 0 paddings to match this parameter
	hop_size=200,  # For 16000Hz, 200 = 12.5 ms (0.0125 * sample_rate)
	win_size=800,  # For 16000Hz, 800 = 50 ms (If None, win_size = n_fft) (0.05 * sample_rate)
	sample_rate=16000,  # 16000Hz (corresponding to librispeech) (sox --i <filename>)
	frame_shift_ms=None,  # Can replace hop_size parameter. (Recommended: 12.5)
	min_level_db=-100,
	num_mels=80,  # Number of mel-spectrogram channels and local conditioning dimensionality
	fmin=55, # 55 male, 95 female. Pitch info: male~[65, 260], female~[100, 525])
	fmax=7600,  # To be increased/reduced depending on data.
	ref_level_db=20,
	signal_normalization=True,
	allow_clipping_in_normalization=True,  # Only relevant if mel_normalization = True
	symmetric_mels=True,
	max_abs_value=4.,
	preemphasize=True,  # whether to apply filter
	preemphasis=0.97,  # filter coefficient.
)

def get_hop_size():
	hop_size = hp.hop_size
	if hop_size is None:
		assert hp.frame_shift_ms is not None
		hop_size = int(hp.frame_shift_ms / 1000 * hp.sample_rate)
	return hop_size

def _stft(y):
	# if hp.use_lws:
	# 	return _lws_processor(hp).stft(y).T
	# else:
    return librosa.stft(y=y, n_fft=hp.n_fft, hop_length=get_hop_size(), win_length=hp.win_size)

def preemphasis(wav, k, preemphasize=True):
	if preemphasize:
		return signal.lfilter([1, -k], [1], wav)
	return wav

def _amp_to_db(x):
	min_level = np.exp(hp.min_level_db / 20 * np.log(10))
	return 20 * np.log10(np.maximum(min_level, x))

# Conversions
_mel_basis = None

def _linear_to_mel(spectogram):
	global _mel_basis
	if _mel_basis is None:
		_mel_basis = _build_mel_basis()
	return np.dot(_mel_basis, spectogram)

def _build_mel_basis():
	assert hp.fmax <= hp.sample_rate // 2
	return librosa.filters.mel(hp.sample_rate, hp.n_fft, n_mels=hp.num_mels,
							   fmin=hp.fmin, fmax=hp.fmax)


def _normalize(S):
	if hp.allow_clipping_in_normalization:
		if hp.symmetric_mels:
			return np.clip((2 * hp.max_abs_value) * ((S - hp.min_level_db) / (-hp.min_level_db)) - hp.max_abs_value,
						   -hp.max_abs_value, hp.max_abs_value)
		else:
			return np.clip(hp.max_abs_value * ((S - hp.min_level_db) / (-hp.min_level_db)), 0, hp.max_abs_value)
	
	assert S.max() <= 0 and S.min() - hp.min_level_db >= 0
	if hp.symmetric_mels:
		return (2 * hp.max_abs_value) * ((S - hp.min_level_db) / (-hp.min_level_db)) - hp.max_abs_value
	else:
		return hp.max_abs_value * ((S - hp.min_level_db) / (-hp.min_level_db))

def melspectrogram(wav):
	D = _stft(preemphasis(wav, hp.preemphasis, hp.preemphasize))
	S = _amp_to_db(_linear_to_mel(np.abs(D))) - hp.ref_level_db
	
	if hp.signal_normalization:
		return _normalize(S)
	return S
