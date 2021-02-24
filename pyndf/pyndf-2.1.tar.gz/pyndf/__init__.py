#!/usr/bin/python
# added support for ECG/HRV based scoring
# (c)-2020 Neurobit Technologies Pte Ltd - Amiya Patanaik amiya@neurobit.io
# Licensed under Neurobit EULA

import math
import json
import base64
import hashlib
import struct
import zlib
import msgpack
import warnings
import numpy as np
import msgpack_numpy as m
from io import BytesIO
from numba import jit
from msgpack import unpackb
from ecgdetectors import Detectors
from scipy.interpolate import interp1d
from skimage.measure import block_reduce
from pyndf.wt_compressor import compress, decompress, calculate_PRD
from scipy.signal import firwin, lfilter, resample_poly, stft, butter

# patch msgpack to handle numpy
m.patch()

# using Numba to optimize
# why vectorize when you have numba?
@jit(nopython=True, parallel=True)
def rolling_window(a, window, step_size):
    N = int((len(a)-window)/step_size) + 1
    X = np.zeros((N, window))
    for i in range(N):
        X[i,:] = a[i*step_size:i*step_size+window]

    return X


def dc_block(x, fs, fc = 0.1):
# DC block filter the time signal x(t), fs is the sampling rate and 
# fc is the highpass cutoff frequency 
    Fc = 2.0*fc/fs
    a = (np.sqrt(3) - 2.0*math.sin(math.pi*Fc))/(math.sin(math.pi*Fc)+np.sqrt(3)*math.cos(math.pi*Fc))
    return lfilter([1, -1], [1, -a], x)


# this can extract rr from the data
# but it appears to fail if data length is too long and 
# the data changes too much across time
# Uses ADARRI to detect spurious r-peaks, Rebergen et al. 2018
# R peak detection based on Vignesh Kalidas and Lakshman Tamil. 
# Real-time QRS detector using Stationary Wavelet Transform for Automated ECG Analysis.
def _extract_rr(ecg, fs=128):
    detectors = Detectors(fs)
    r_peaks = detectors.swt_detector(ecg)
    r_peaks = np.array(r_peaks, dtype=np.int)
    adRRI = abs(np.diff(r_peaks, n=2))*1000/fs
    invalid = np.where(adRRI>276)[0]
    rr_features = np.zeros((len(ecg)))
    rr_features[r_peaks] = 1
    rr_features[invalid] = -1
    return rr_features


#So rr is extracted in windows (4.5 minutes window)
def rr_from_ecg(ecg, fs=128):
    win_size = 9*30*fs
    # if data length is less than 4.5 minute 
    if len(ecg) <= win_size:
        return _extract_rr(ecg, fs)

    rr_features = np.zeros((len(ecg)))   
    res = np.apply_along_axis(_extract_rr, 1, rolling_window(ecg, win_size, win_size))
    res = res.flatten()
    last_bit = ecg[-win_size:]
    res_extra = _extract_rr(last_bit, fs)
    rr_features[0:len(res)] = res
    rr_features[-win_size:] = res_extra
    return rr_features


# nn interval - assumed to be artifact corrected rr(s)
def create_ndf_from_nn(nn_loc, sampling_rate, duration=None, compressionbit=True, age=None, gender=None, realtime=False):
    if duration is None:
        duration = math.ceil(nn_loc[-1]/sampling_rate) + 1
    elif int(nn_loc[-1]/sampling_rate) > duration:
        raise RuntimeError("duration and nn_loc do not agree")

    if realtime and duration != 9*30:
        raise RuntimeError("Exactly 4.5 minutes of rr data required to create realtime NDF from rr.")

    if not realtime and duration < 72*30:
        raise RuntimeError("Atleast 36 minutes of rr data required to create NDF from rr.")

    spec = {}
    spec['hrv'] = nn_loc
    spec['fs'] = sampling_rate

    if age is not None:
        spec['age'] = age

    if gender is not None:
        if gender is 'male':
            spec['gender'] = 'male'
        else:
            spec['gender'] = 'female'

    payload = msgpack.packb(spec, use_single_float=True, use_bin_type=True) 
    shaHash = hashlib.sha1()
    shaHash.update(payload)
    rawDigest = shaHash.digest()
    msgDigest = [c for c in rawDigest]

    urlSafeHash = base64.urlsafe_b64encode(("".join(map(chr, msgDigest))).encode('UTF-8')).decode('ascii')
    urlSafeHash = urlSafeHash[0:-1]

    header = '{"version":"HRV", "duration": '+ str(duration) + ', "url":"' + urlSafeHash + '", "spec":' + json.dumps(list(spec.keys())) + '}'
    header = '{:<256}'.format(header[:256])
    
    signature = bytearray(struct.pack('<3s?', b'NDF', compressionbit))  

    if not realtime and compressionbit:
        payload = zlib.compress(payload)

    return signature + header.encode() + payload


def create_ndf_from_rr(rr_loc, sampling_rate, duration=None, compressionbit=True, age=None, gender=None, realtime=False):
    if duration is None:
        duration = math.ceil(rr_loc[-1]/sampling_rate) + 1
    elif int(rr_loc[-1]/sampling_rate) > duration:
        raise RuntimeError("duration and rr_loc do not agree")

    if realtime and duration != 9*30:
        raise RuntimeError("Exactly 4.5 minutes of rr data required to create realtime NDF from rr.")

    if not realtime and duration < 72*30:
        raise RuntimeError("Atleast 36 minutes of rr data required to create NDF from rr.")

    # Uses ADARRI to detect spurious r-peaks, Rebergen et al. 2018
    adRRI = abs(np.diff(rr_loc, n=2))*1000/sampling_rate
    invalid = np.where(adRRI>276)[0]
    rr_features = np.zeros((int(duration*sampling_rate)))
    rr_features[rr_loc] = 1
    rr_features[invalid] = -1

    rr_loc = np.where(rr_features==1)[0]

    spec = {}
    spec['hrv'] = rr_loc
    spec['fs'] = sampling_rate

    if age is not None:
        spec['age'] = age

    if gender is not None:
        if gender is 'male':
            spec['gender'] = 'male'
        else:
            spec['gender'] = 'female'

    payload = msgpack.packb(spec, use_single_float=True, use_bin_type=True) 
    shaHash = hashlib.sha1()
    shaHash.update(payload)
    rawDigest = shaHash.digest()
    msgDigest = [c for c in rawDigest]

    urlSafeHash = base64.urlsafe_b64encode(("".join(map(chr, msgDigest))).encode('UTF-8')).decode('ascii')
    urlSafeHash = urlSafeHash[0:-1]

    header = '{"version":"HRV", "duration": '+ str(math.ceil(duration)) + ', "url":"' + urlSafeHash + '", "spec":' + json.dumps(list(spec.keys())) + '}'
    header = '{:<256}'.format(header[:256])
    
    signature = bytearray(struct.pack('<3s?', b'NDF', compressionbit))  

    if compressionbit:
        payload = zlib.compress(payload)

    return  signature + header.encode() + payload
  

def create_ndf_from_ecg(data, sampling_rate, compressionbit=True, age=None, gender=None, realtime=False):
    duration = len(data)/sampling_rate

    if realtime and duration != 9*30:
        raise RuntimeError("Exactly 4.5 minutes of rr data required to create realtime NDF from rr.")

    if not realtime and duration < 72*30:
        raise RuntimeError("Atleast 36 minutes of rr data required to create NDF from rr.")

    rr = rr_from_ecg(data, sampling_rate)
    rr_loc = np.where(rr==1)[0]
    spec = {}
    spec['hrv'] = rr_loc
    spec['fs'] = sampling_rate

    if age is not None:
        spec['age'] = age

    if gender is not None:
        if gender is 'male':
            spec['gender'] = 'male'
        else:
            spec['gender'] = 'female'

    payload = msgpack.packb(spec, use_single_float=True, use_bin_type=True) 
    shaHash = hashlib.sha1()
    shaHash.update(payload)
    rawDigest = shaHash.digest()
    msgDigest = [c for c in rawDigest]

    urlSafeHash = base64.urlsafe_b64encode(("".join(map(chr, msgDigest))).encode('UTF-8')).decode('ascii')
    urlSafeHash = urlSafeHash[0:-1]

    header = '{"version":"HRV", "duration": '+ str(math.ceil(duration)) + ', "url":"' + urlSafeHash + '", "spec":' + json.dumps(list(spec.keys())) + '}'
    header = '{:<256}'.format(header[:256])
    
    signature = bytearray(struct.pack('<3s?', b'NDF', compressionbit))  

    if compressionbit:
        payload = zlib.compress(payload)

    return signature + header.encode() + payload



# new API is more explicit in terms of where the data is coming from
def create_ndf_from_psg(data, sampling_rates, compressionbit=True, check_quality = True):
    return create_ndf(data, sampling_rates, compressionbit, check_quality)


def create_ndf(data, sampling_rates, compressionbit=True, check_quality = True):
# Order of data(12 channels cell array of 1Xsamples PSG data): 
# C3, C4, EOG-l, EOG-R, EMG-chin, EMG-left, 
# EMG-right, ECG, Airflow, Thor, Abdo, SpO2 and Corresponding sampling rates as a numpy array
# a new dc-block filter is added now to EEG and ECG channels, other channels are not touched

    window_128 = np.hamming(128)
    window_256 = np.hamming(256)
    window_512 = np.hamming(512)

    data_exists = np.zeros(12)
    for idx, value in enumerate(data):
        if np.any(value):
            data_exists[idx] = 1  

    sampling_rates[data_exists == 0] = 200
    idx = np.where(data_exists == 1)[0]

    if data_exists[0] == 0:
        sampling_rates[0] = sampling_rates[1]

    if data_exists[1] == 0:
        sampling_rates[1] = sampling_rates[0]

    if sampling_rates[1] != sampling_rates[0]:
        raise RuntimeError("Both EEG channels must be sampled at the same rate.")

    # check sampling rates
    if np.any(sampling_rates[0:2] < 100):
        raise RuntimeError("Sampling rate must be >= 100Hz for EEG channels.")

    if np.any(sampling_rates[2:4] < 100):
        raise RuntimeError("Sampling rate must be >= 100Hz for EOG channels.")

    if np.any(sampling_rates[4:7] < 200):
        raise RuntimeError("Sampling rate must be >= 200Hz for EMG channels.")

    if sampling_rates[7] < 100:
        raise RuntimeError("Sampling rate must be >= 100Hz for ECG channels.")

    if np.any(sampling_rates[8:11] < 25):
        raise RuntimeError("Sampling rate must be >= 25Hz for respiratory channels")

    if np.any(sampling_rates[11] < 1):
        raise RuntimeError("Sampling rate must be >= 1Hz for SpO2 channel")

    
    # this will hold the pre-processed version of the data
    processed_data = [None]*12
    eeg = None
    
    # apply a sharp DC block at 0.1 Hz
    for i in idx:
        # check if EEG/EOG/ECG channel
        if i < 8:
            data[i] = dc_block(data[i], sampling_rates[i])

    # apply filters to first 5 channels as per spec
    # Order 50 FIR filter
    # Basic Settings C3, C4, EOG-l, EOG-R, EMG-chin
    filter_lp = [35, 35, 35, 35, 80]
    filter_hp = [0.3, 0.3, 0.3, 0.3, 0.3]
    one = np.array(1)
    for i in idx:
        if i < 5:
            filter_b = firwin(51, [filter_hp[i]*2 / sampling_rates[i], filter_lp[i]*2 / sampling_rates[i]], pass_zero=False, window='hamming', scale=True)
            processed_data[i] = lfilter(filter_b, one, data[i])
        elif i==5 or i==6:
            filter_b, filter_a = butter(N=2, Wn=[10*2 / sampling_rates[i], 80*2 /sampling_rates[i] ], btype='band')
            processed_data[i] = lfilter(filter_b, filter_a, data[i])

      
    threshold = 10

    # Process EEG
    eeg_exist = 0
    if data_exists[0] and data_exists[1]:
        eeg = (processed_data[0] + processed_data[1])/2
        eeg_exist = 1
    elif data_exists[0]:
        eeg = processed_data[0]
        eeg_exist = 1
    elif data_exists[1]:
        eeg = processed_data[1]
        eeg_exist = 1

    if eeg_exist:
        if sampling_rates[0] != 100:
            P = 100
            Q = sampling_rates[0]
            eeg = resample_poly(eeg, P, Q)
            processed_data[0] = eeg
            processed_data[1] = eeg

    # Process EOG
    for i in range(2,4):
        if data_exists[i] and sampling_rates[i] != 100:
            P = 100
            Q = sampling_rates[i]
            processed_data[i] = resample_poly(processed_data[i], P, Q)

    # Process EMG 
    for i in range(4,7):
        if data_exists[i] and sampling_rates[i] != 200:
            P = 200
            Q = sampling_rates[i]
            processed_data[i] = resample_poly(processed_data[i], P, Q)

    # Process ECG
    if data_exists[7] and sampling_rates[7] != 100:
        P = 100
        Q = sampling_rates[7]
        data[7] = resample_poly(data[7], P, Q)
        processed_data[7] = compress(data[7])
        
    # Process Respiration
    for i in range(8,12):
        if data_exists[i] and sampling_rates[i] != 25:
            P = 25
            Q = sampling_rates[i]
            processed_data[i] = resample_poly(data[i], P, Q)

    # Process EEG and chin EMG for respiration
    # only if respiratory channels are present
    if np.sum(data_exists[8:11]) != 0:
        if eeg_exist:
            eeg_bands = np.zeros((int(len(eeg)/4), 4))
            [_, _, Sxx] = stft(eeg, fs=100, window=window_256, nperseg=256, noverlap=252, return_onesided=True)
            # alpha 
            eeg_bands[:, 0] = np.sum(abs(Sxx[21:32, 1:])* np.sum(window_256), axis=0) 
            # theta 
            eeg_bands[:, 1] = np.sum(abs(Sxx[16:21, 1:]) * np.sum(window_256), axis=0) 
            # spindle 
            eeg_bands[:, 2] = np.sum(abs(Sxx[29:42, 1:]) * np.sum(window_256), axis=0) 
            # other 
            eeg_bands[:, 3] = np.sum(abs(Sxx[42:66, 1:]) * np.sum(window_256), axis=0) 
        # check if chin emg is present
        if data_exists[4]:
            emg_power = np.zeros((int(len(processed_data[4])/4)))
            [_, _, Sxx] = stft(processed_data[4], fs=200, window=window_512, nperseg=512, noverlap=504, return_onesided=True)
            # total power
            emg_power = np.sum(abs(Sxx[26:155, 1:]) * np.sum(window_512), axis=0) 



    # process Leg EMG
    # EMG-L
    if data_exists[5]:
        processed_data[5] = np.abs(processed_data[5])
        # Low Pass Filter
        b, a = butter(N=2, Wn=5.0*2.0/200.0, btype='lowpass')
        processed_data[5] = lfilter(b, a, processed_data[5])
        # resample to 25Hz
        processed_data[5] = resample_poly(processed_data[5], 25, 200)

    # EMG-R
    if data_exists[6]:
        processed_data[6] = np.abs(processed_data[6])
        # Low Pass Filter
        b, a = butter(N=2, Wn=5.0*2.0/200.0, btype='lowpass')
        processed_data[6] = lfilter(b, a, processed_data[6])
        # resample to 25Hz
        processed_data[6] = resample_poly(processed_data[6], 25, 200)

    # release memory
    data = []

    rates = [100, 100, 100, 100, 200, 200, 200, 200, 25, 25, 25]
    totalEpochs = math.floor(processed_data[idx[0]].size/30/rates[idx[0]])

    data = np.zeros((32,32,4,totalEpochs), dtype=np.float32)

    for i in range(totalEpochs):
        if eeg_exist:
            frame = stft(eeg[i * 3000:(i + 1) * 3000], window=window_128, noverlap=36, boundary=None, nperseg=128,
                      return_onesided=True, padded=False)
            data[:, :, 0, i] = abs(frame[2][1:33, 0:32]) * np.sum(window_128)

        # EOG-L
        if data_exists[2]:
            frame = stft(processed_data[2][i * 3000:(i + 1) * 3000], window=window_128, noverlap=36, boundary=None, nperseg=128,
                      return_onesided=True, padded=False)
            data[:, :, 1, i] = abs(frame[2][1:33, 0:32]) * np.sum(window_128)

        # EOG-R
        if data_exists[3]:
            frame = stft(processed_data[3][i * 3000:(i + 1) * 3000], window=window_128, noverlap=36, boundary=None, nperseg=128,
                      return_onesided=True, padded=False)
            data[:, :, 2, i] = abs(frame[2][1:33, 0:32]) * np.sum(window_128)

        # EMG chin
        if data_exists[4]:
            frame = stft(processed_data[4][i * 6000:(i + 1) * 6000], window=window_256, noverlap=71, boundary=None, nperseg=256,
                      return_onesided=True, padded=False) 
            data[:, :, 3, i] = block_reduce(abs(frame[2][1:129, :]) * np.sum(window_256), (4, 1), np.mean) 

    
    quality = np.sum(np.mean(data, axis=(0,1)) > 500, axis = 1)*100.0/totalEpochs

    if np.any(quality > threshold) and check_quality:
        print("\u001b[31;1mWARNING:\u001b[0m Electrode Falloff detected, problematic channels will be ignored.")

    if np.sum(data_exists[0:5]) == 0:
        print("\u001b[31;1mWARNING:\u001b[0m No EEG channel found, sleep staging cannot be done.")
    
    if np.sum(data_exists[5:7]) == 0:
        print("\u001b[31;1mWARNING:\u001b[0m Leg EMG not found, PLM detection disabled.")

    if np.sum(data_exists[8:11]) == 0:
        print("\u001b[31;1mWARNING:\u001b[0m No respiratory channel found, respiratory events detection disabled.")

    spec = {}
    
    if eeg_exist:
        spec['eeg'] = data[:, :, 0, :]
        if np.sum(data_exists[8:11]) != 0:
            spec['eeg_bands'] = eeg_bands

    # EOG-L
    if data_exists[2]:    
        spec['eog_l'] = data[:, :, 1, :]

    # EOG-R
    if data_exists[3]:    
        spec['eog_r'] = data[:, :, 2, :]

    # EMG-Chin
    if data_exists[4]:    
        spec['emg'] = data[:, :, 3, :]
        if np.sum(data_exists[8:11]) != 0:
            spec['emg_power'] = emg_power      

    # EMGL-Left
    if data_exists[5]:    
        spec['emg_l'] = processed_data[5]

    # EMGL-Right
    if data_exists[6]:    
        spec['emg_r'] = processed_data[6]

    # ECG
    if data_exists[7]:    
        spec['ecg'] = processed_data[7]

    # Airflow
    if data_exists[8]:    
        spec['airflow'] = processed_data[8]

    # thor
    if data_exists[9]:    
        spec['thor'] = processed_data[9]

    # abdo
    if data_exists[10]:    
        spec['abdo'] = processed_data[10]

    # spo2
    if data_exists[11]:    
        spec['spo2'] = processed_data[11]

    
    payload = msgpack.packb(spec, use_single_float=True, use_bin_type=True) 
    shaHash = hashlib.sha1()
    shaHash.update(payload)
    rawDigest = shaHash.digest()
    msgDigest = [c for c in rawDigest]

    urlSafeHash = base64.urlsafe_b64encode(("".join(map(chr, msgDigest))).encode('UTF-8')).decode('ascii')
    urlSafeHash = urlSafeHash[0:-1]

    header = '{"version":"PSG", "duration": '+ str(int(totalEpochs*30)) + ', "url":"' + urlSafeHash + '", "spec":' + json.dumps(list(spec.keys())) + '}'
    header = '{:<256}'.format(header[:256])
    
    signature = bytearray(struct.pack('<3s?', b'NDF', compressionbit))  

    if compressionbit:
        payload = zlib.compress(payload)

    stream = signature + header.encode() + payload

    # return the stream and processed eeg, eog-l and eog-r data
    return stream, eeg, processed_data[5], processed_data[6]


def save_ndf(file_name, ndf_bytearray):

    with open(file_name, 'wb') as f:
        f.write(ndf_bytearray)




def read_stream_header(stream):
    # Read header:
    # 3 bytes signature, 1 byte compressionbit
    bytes = stream.read(4)
    header = stream.read(256) 
    signature = struct.unpack('<3s?', bytes)

    if (signature[0].decode("ascii") != 'NDF'):
        raise RuntimeError("File is not a valid NDF file.")

    compressionbit = signature[1]
    header = json.loads(header.decode("ascii"))
    header['compressionbit'] = compressionbit
   
    stream.seek(0)
   
    return header 


def read_header(ndf_file):
    # Read header:
    with open(ndf_file, "rb") as stream:
        return read_stream_header(stream)
    

# check_quality is not used as of now
def read_stream(stream, check_quality = True):
    # Read header:
    bytes = stream.read(4)
    header = stream.read(256) 
    signature = struct.unpack('<3s?', bytes)

    if (signature[0].decode("ascii") != 'NDF'):
        raise RuntimeError("File is not a valid NDF file.")

    compressionbit = signature[1]
    header = json.loads(header.decode("ascii"))
    header['compressionbit'] = compressionbit
    
    # read rest of the data
    bytes = stream.read()

    if (compressionbit):
        bytes = zlib.decompress(bytes)

    try:
        payload = msgpack.unpackb(bytes, raw=False)
    except:
        raise RuntimeError("File is corrupt.")

    if not 'url' in header:
        shaHash = hashlib.sha1()
        shaHash.update(bytes)
        rawDigest = shaHash.digest()
        msgDigest = [c for c in rawDigest]
    
        urlSafeHash = base64.urlsafe_b64encode(("".join(map(chr, msgDigest))).encode('UTF-8')).decode('ascii')
        urlSafeHash = urlSafeHash[0:-1]
    
        header['url'] = urlSafeHash

    stream.seek(0)

    return header, payload



def read_ndf(ndf_file, check_quality = True):
    with open(ndf_file, "rb") as stream:
        return read_stream(stream, check_quality)

