import librosa



def read_wav(path):
    speech, sr = librosa.load(path, sr=16000)
    return speech
