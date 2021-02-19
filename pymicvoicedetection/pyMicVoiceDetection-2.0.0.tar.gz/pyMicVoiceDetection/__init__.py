#!/usr/bin/env python
# coding: utf-8
import wave
import pyaudio
from pyaudio import PyAudio,paInt16
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
sampwidth=2
def listDevices():
    '''
    list avalible input mic devices in system
    '''
    p = PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))

def save_wave_file(filename,data):
    '''
    save the data to the wavfile
    =================================
    filename:path to save the sound recorded from Mic
    data:list of samples in type of bytes
    =================================
    '''
    wf=wave.open(filename,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sampwidth)
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()
    
def Record(filename,buf=None,dur=3,deviceIndex=None):
    '''
    record limit duration to filename
    =================================
    buf:list of recorded samples in type of bytes 
    dur:recording duration (sec)
    =================================
    '''
    pa=PyAudio()
    stream=pa.open(format = FORMAT,channels=CHANNELS,
    rate=RATE,input=True,
    input_device_index = deviceIndex,
    frames_per_buffer=CHUNK)
    count=0
    if buf == None: buf = []
    try:
        while count<dur*RATE/CHUNK :#控制錄音時間 #
            string_audio_data = stream.read(CHUNK,exception_on_overflow = False)#一次性錄音取樣位元組大小
            buf.append(string_audio_data)
            count+=1
            print('.',end='')
    finally:stream.close()
    save_wave_file(filename,buf)

def play_wav(wav_filename):
    '''
    play the wav_filename
    =================================
    '''
    try:
        print('Trying to play file ' + wav_filename)
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
        str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
        str(eofe) + '. Skipping.\n')
        return
    # Instantiate PyAudio.
    p = pyaudio.PyAudio()
    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

def _rms(x):
    return np.sqrt(x.dot(x)/x.size)

def recordAsyn(filename,dur=25,TH=0.01,Samples=None,deviceIndex=None):
    '''
    record asynchronously to the same file==>filename
    =================================
    dur:total duration of voice activitive detection
    TH:threshold of endpoint detection rms Energy
    Samples:normalized recorded samples (list)
    =================================
    '''
    #WAVE_OUTPUT_FILENAME = "output.wav"
    _MAX_VALUE=np.iinfo(np.int16).max    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = deviceIndex,
                    frames_per_buffer = CHUNK)
    print("* recording...")
    energy = [];    buf=[]
    S='silence'
    serial = 0;    silenceNum=0;    waitNum=0
    iterationPerSec = int(RATE/CHUNK)
    HALF_CHUNK = int(CHUNK/2)
    for i in range(0, dur*iterationPerSec):
        #若每個frame 512個samples，一個frame:512/16000=32ms
        data = stream.read(CHUNK, exception_on_overflow = False)
        sample=np.frombuffer(data,np.int16)/_MAX_VALUE
        e1=_rms(sample[0:HALF_CHUNK])
        e2=_rms(sample[HALF_CHUNK:CHUNK])
        energy.append(e1)
        energy.append(e2)
        if S=='silence':
            if e1>TH and e2>TH:
                buf.append(data)
                S='voice'
        elif S=='voice':
            buf.append(data)
            if e1<TH and e2<TH:
                silenceNum+=1
                if silenceNum>5:
                    serial+=1
                    save_wave_file(filename,buf)
                    print(filename + ".......saved")
                    break
            else: silenceNum=0
            
        if Samples != None: Samples.extend(list(sample))
        
    stream.close()
    p.terminate()
    
def recordAsynSerial(dur=25,TH=0.01,label="",Samples=None,deviceIndex=None):
    '''
    =================================
    record asynchronously one bye one in serial
    dur:total duration of voice activitive detection
    TH:threshold of endpoint detection rms Energy
    label:label in front of serial(filename format)
    Samples:normalized recorded samples (list)
    =================================
    '''
    #WAVE_OUTPUT_FILENAME = "output.wav"
    _MAX_VALUE=np.iinfo(np.int16).max    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index = deviceIndex,
                    frames_per_buffer = CHUNK)
    print("* recording...")
    energy = [];    buf=[]
    S='silence'
    startTime = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    serial = 0;    silenceNum=0;    waitNum=0
    iterationPerSec = int(RATE/CHUNK)
    HALF_CHUNK = int(CHUNK/2)
    for i in range(0, dur*iterationPerSec):
        #若每個frame 512個samples，一個frame:512/16000=32ms
        data = stream.read(CHUNK, exception_on_overflow = False)
        sample=np.frombuffer(data,np.int16)/_MAX_VALUE
        e1=_rms(sample[0:HALF_CHUNK])
        e2=_rms(sample[HALF_CHUNK:CHUNK])
        energy.append(e1)
        energy.append(e2)
        if S=='silence':
            if e1>TH and e2>TH:
                buf.append(data)
                S='voice'
        elif S=='voice':
            buf.append(data)
            if e1<TH and e2<TH:
                silenceNum+=1
                if silenceNum>5:
                    serial+=1
                    filename = label + '_' +startTime +"_"+str(serial)+".wav"
                    save_wave_file(filename,buf)
                    #y, sr = librosa.load(filename,sr=None)
                    print(filename + ".......saved")
                    buf=[]
                    S='wait'
                    silenceNum=0
            else: silenceNum=0        
        elif S=='wait':  
            waitNum+=1
            if waitNum>iterationPerSec*1:
                S='silence'
        if Samples !=None : Samples.extend(list(sample))

    stream.close()
    p.terminate()


def recordAsynSerialAndPlot(dur=25,TH=0.01,label="",Samples=None,endPoints=None,deviceIndex=None):
    '''
    =================================
    record asynchronously one bye one in serial and plot the result in the end
    dur:total duration of voice activitive detection
    TH:threshold of endpoint detection rms Energy
    label:label in front of serial(filename format)
    Samples:normalized recorded samples (list)
    endPoints:pairs of every segment start and end point
    =================================
    '''
    #WAVE_OUTPUT_FILENAME = "output.wav"
    _MAX_VALUE=np.iinfo(np.int16).max    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input_device_index = deviceIndex,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("* recording...")
    energy = [];    buf=[]
    S='silence'
    startTime = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
    serial = 0;    silenceNum=0;    waitNum=0
    iterationPerSec = int(RATE/CHUNK)
    HALF_CHUNK = int(CHUNK/2)
    start,end = 0,0
    if endPoints==None : endPoints=[]
    if Samples == None: Samples = []
    for i in range(0, dur*iterationPerSec):
        #若每個frame 512個samples，一個frame:512/16000=32ms
        data = stream.read(CHUNK, exception_on_overflow = False)
        sample=np.frombuffer(data,np.int16)/_MAX_VALUE
        e1=_rms(sample[0:HALF_CHUNK])
        e2=_rms(sample[HALF_CHUNK:CHUNK])
        energy.append(e1)
        energy.append(e2)
        if S=='silence':
            if e1>TH and e2>TH:
                buf.append(data)
                S='voice'
                start = i*len(sample)-int(len(sample)*0.5)
        elif S=='voice':
            buf.append(data)
            if e1<TH and e2<TH:
                silenceNum+=1
                if silenceNum>5:
                    serial+=1
                    filename = label + '_' +startTime +"_"+str(serial)+".wav"
                    save_wave_file(filename,buf)
                    #y, sr = librosa.load(filename,sr=None)
                    print(filename + ".......saved")
                    buf=[]
                    S='wait'
                    silenceNum=0
                    end = i*len(sample)-int(len(sample)*0.5)
                    endPoints.append((start,end))
            else: silenceNum=0        
        elif S=='wait':  
            waitNum+=1
            if waitNum>iterationPerSec*1:
                S='silence'
        Samples.extend(list(sample))
    stream.close()
    p.terminate()
    
    A=[0]*len(Samples)
    B=[0]*len(Samples)
    try:
        for start,end in endPoints:
            A[start-1]=-1; A[start]=1
            B[end-1]=-1; B[end]=1
    except:pass
    plt.plot(Samples)
    plt.plot(A)
    plt.plot(B)
    plt.show()
