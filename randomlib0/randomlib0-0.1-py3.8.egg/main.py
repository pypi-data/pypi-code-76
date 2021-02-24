from secrets import *
import hashlib
def _ty():
    d=token_bytes()
    n=hashlib.md5(d).hexdigest()
    return int(n,16)
def get(n=2):
    import sounddevice as sd
    from scipy.io.wavfile import write

    fs = 44100
    seconds = n

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('jdfgssjkdfghlsdkfjlgfgbdfkjgdjsldkfjghoutputjadsf.wav', fs, myrecording)
    y=open('jdfgssjkdfghlsdkfjlgfgbdfkjgdjsldkfjghoutputjadsf.wav','rb')
    ttt=y.read()
    y.close()
    return ttt
from random import Random
import time,os
def rand(_max=2**10,xxx=2):
    data=get(xxx)
    n=0
    r=Random()
    for t in data:
        _time=int(time.time())
        n+=(t*_ty()+_time)%_max
    return int(n)%_max
##for i in range(15):
##    print(rand())
##        
    
