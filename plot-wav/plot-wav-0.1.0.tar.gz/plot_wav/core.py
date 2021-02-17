import wave
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wio
import librosa
import librosa.display
import argparse


def get_rate(file):
    wf = wave.open(file, 'r')
    return wf.getframerate()


def plot_wave(file):
    # open wave file
    wf = wave.open(file, 'r')
    channels = wf.getnchannels()
    rate = get_rate(file)

    # load wave data
    time = wf.getnframes() / rate
    chunk_size = int(wf.getframerate() * time)
    amp = (2**8) ** wf.getsampwidth() / 2
    data = wf.readframes(chunk_size)
    data = np.frombuffer(data, 'int16')

    # make time axis
    size = float(chunk_size)
    x = np.arange(0, size/rate, 1.0/rate)

    # multi channels
    for i in range(channels):
        plt.plot(x, data[i::channels])

    plt.xlabel("time[s]")
    plt.ylabel("standerdized amplitude")
    plt.ylim([-amp, amp])

    plt.title(file)


def plot_spec(file):
    rate, data = wio.read(file)
    with np.errstate(divide='ignore'):
        pxx, freq, bins, t = plt.specgram(data, Fs=rate)

    plt.title(file)


def plot_mfcc(file):
    rate = get_rate(file)

    y, sr = librosa.load(file, sr=rate)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)

    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title(file)
    plt.tight_layout()


def main():
    # opts conf
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wave', help='plot original wave',
                        action='store_true')
    parser.add_argument('-s', '--spec', help='plot spectrogram',
                        action='store_true')
    parser.add_argument('-m', '--mfcc', help='plot MFCC',
                        action='store_true')
    parser.add_argument('-i', '--input', help='file to input',
                        type=str)
    parser.add_argument('-o', '--output', help='file to output',
                        type=str)
    args = parser.parse_args()

    fig = plt.figure()
    filename = args.input

    if filename is None:
        print("ERROR: You need to specify the file name with -i opt.")
        exit(1)

    if args.wave:
        plot_wave(filename)
    elif args.spec:
        plot_spec(filename)
    elif args.mfcc:
        plot_mfcc(filename)

    dump_filename = args.output
    if dump_filename is None:
        plt.show()
    else:
        fig.savefig(dump_filename)
