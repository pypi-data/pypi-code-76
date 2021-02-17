import os, textwrap
from pathlib import Path
import dask
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import torch, librosa, cv2
from nptdms import TdmsFile


################################################################
# make labels inferred from subdirs
################################################################
def make_labels(filepath, exts=["wav", "tdms"], use_dask=False):
    subdirs = [Path(d) for d in os.scandir(filepath) if os.path.isdir(d)]

    if use_dask:
        @dask.delayed
        def search(path, ext):
            return list(path.glob(f"*.{ext.lstrip('.')}"))      
        @dask.delayed
        def merge(lst):
            files = []
            for e in lst:
                files.extend(e)
            return files
        files = []
        for subdir in subdirs:
            for ext in exts:
                files.append(search(subdir, ext))
        files = merge(files).compute()
        
    else:
        files = []
        for subdir in subdirs:
            for ext in exts:
                files.extend(subdir.glob(f"**/*.{ext.lstrip('.')}"))
        
    labels = pd.DataFrame({
        'filename': [f.name for f in files],
        'filepath': [str(f) for f in files],
        'label': [f.parent.name for f in files]
    })
    
    return labels


################################################################
# encode labels
################################################################
def encode_labels(labels, reverse=False, verbose=True):
    names = sorted(labels['label'].unique(), reverse=reverse)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    labels['label'] = [encoder[x] for x in labels['label']]
    
    if verbose:
        print(f'<LABELS> {len(names)} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels, encoder, decoder


################################################################
# encode labels
################################################################

# 아래 def와 무관하게, 왜 global df labels의 값이 바뀌는지 확인...
def one_hot_encode_labels(labels, class_nothing='nothing', reverse=False, verbose=True):
    names = sorted(set('|'.join(labels['label'].tolist()).split('|')), reverse=reverse)
    if class_nothing in names:
        names.remove(class_nothing)
    n_classes = len(names)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    
    #### one hot encoding
    for i in labels.index:
        label_vector = n_classes * [0]
        classes = labels.at[i, 'label'].split('|')
        if class_nothing in classes:
            classes.remove(class_nothing)
        for c in classes:
            label_vector[encoder[c]] = 1
        labels.at[i, 'label'] = '|'.join([str(e) for e in label_vector])
    
    if verbose:
        print(f'<LABELS> {n_classes} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels, encoder, decoder


################################################################
# load_tmds
################################################################
def load_tdms(filepath, sr_new=None, channel='CPsignal1'):
    try:
        ch = TdmsFile(filepath).groups()[0][channel]
        y = ch[:]
        sr = 1//ch.properties['dt']
    except Exception as ex:
        print('ERROR!!! {ex}')
        return None, None
    return y, sr


################################################################
# make_confusion_matrix
################################################################
def make_confusion_matrix(truth, predict):
    cm = pd.crosstab(truth, predict)
    for l in cm.index:
        if l not in cm.columns:
            cm[l] = 0
    return cm[cm.index]

        
################################################################
#### AudioDataset (DEFAULT)
################################################################
class AudioDataset(Dataset):
    
    def __init__(self, labels, prep, label_dtype=None):
        
        # pd.series to list
        self.filename = labels.filename.tolist()
        self.filepath = labels.filepath.tolist()
        
        # assume binery_cross_entropy if label's codes are object (string), bce requires float32 label
        if labels.label.dtype == object:
            self.label = labels.label.str.split('|', expand=True).astype(int).to_numpy()
            self.dtype = torch.float32
        # assume cross_entropy if label's codes are integer, cross_entropy requires int64 label
        else:
            self.label = labels.label.tolist()
            self.dtype = torch.int64
        
        # prep = load + transforms
        self.prep = prep

        # manual dtype
        if label_dtype:
            self.dtype = label_dtype
    
    def __len__(self):
        return len(self.label)
    
    def __getitem__(self, idx):
        
        # parse index
        idx = idx.tolist() if torch.is_tensor(idx) else idx
        
        # get filename, filepath, y
        filename = self.filename[idx]
        filepath = self.filepath[idx]
        y = torch.tensor(self.label[idx], dtype=self.dtype)
        
        # prep: filepath -> load -> transform -> model input x
        x = self.prep(filepath)        
        
        return x, y, filename
