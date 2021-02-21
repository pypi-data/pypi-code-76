import pyaudio
import wave
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from python_speech_features import *

def plot_mfcc(mic_data_in, plot_y, mfcc_n):

	mic_data = np.frombuffer(mic_data_in, dtype=np.short)
	wav_data_plot = mic_data[0:-1:300]
	plot_x = np.linspace(0, 5, 735)
	a = len(wav_data_plot)
	plot_y = np.append(plot_y, wav_data_plot)
	plot_y = plot_y[a:]
	plt.ylim(-40000, 40000)
	plt.yticks([-40000, -20000, 0, 20000, 40000])
	plt.plot(plot_x, plot_y, color='green')
	plt.grid()
	fig_name = '../pic/wavepic.jpg'
	plt.savefig(fig_name, bbox_inches='tight')
	plt.close()

	mfccdata = mfcc(mic_data, nfilt=int(mfcc_n / 2), winlen=(len(mic_data) / 44100), samplerate=44100,
					numcep=int(mfcc_n / 2), nfft=len(mic_data))
	mfccdata_ = mfccdata[0][1:]
	mfccdata__ = np.append(mfccdata_, 0)
	mfcc_ = mfccdata__ - mfccdata[0]
	mfcc_data = np.append(mfccdata, mfcc_)
	# fftdata = fft(mic_data, n=(fft_n * 4))#频率取1/4，这里乘4
	# fft_data = abs(fftdata)
	# fft_data = fft_data[:fft_n]
	#print(fft_data)

	return mfcc_data, fig_name, plot_y

# def record_wav(record_pertime):
# 	CHUNK = int(44100 * record_pertime)
# 	FORMAT = pyaudio.paInt16
# 	CHANNELS = 1
# 	RATE = 44100
# 	p = pyaudio.PyAudio()
# 	stream = p.open(format=FORMAT,
# 					channels=CHANNELS,
# 					rate=RATE,
# 					input=True,
# 					frames_per_buffer=CHUNK)
# 	file_name = './recorddata'
# 	word_name = os.path.exists(file_name)
# 	if not word_name:
# 		os.makedirs(file_name)
# 	while True:
# 		frames = []
# 		for i in range(0, int(RATE / CHUNK * record_pertime)):
# 			data = stream.read(CHUNK)
# 			print(data)
# 			frames.append(data)
# 		stream.stop_stream()
# 		stream.close()
# 		p.terminate()
# 		now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')
# 		wav_name = now_time + ".wav"
# 		WAVE_OUTPUT_FILENAME = './recorddata' + '/' + wav_name
# 		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# 		wf.setnchannels(CHANNELS)
# 		wf.setsampwidth(p.get_sample_size(FORMAT))
# 		print(p.get_sample_size(FORMAT))
# 		wf.setframerate(RATE)
# 		wf.writeframes(b''.join(frames))
# 		wf.close()
# 		return WAVE_OUTPUT_FILENAME

def wav_mfcc(path, mfcc_n):
	f = wave.open(path, "rb")
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_date = f.readframes(nframes)
	f.close()
	wave_date = np.frombuffer(str_date, dtype=np.short)
	mfccdata = mfcc(wave_date, nfilt=int(mfcc_n/2), winlen=(len(wave_date)/44100), samplerate=44100, numcep=int(mfcc_n / 2), nfft=len(wave_date))
	mfccdata_ = mfccdata[0][1:]
	mfccdata__ = np.append(mfccdata_, 0)
	mfcc_ = mfccdata__ - mfccdata[0]
	mfcc_data = np.append(mfccdata, mfcc_)
	return mfcc_data



