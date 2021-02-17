import os
from pathlib import Path
import numpy as np
import pandas as pd
from torch.utils.data import random_split
from . import parser
from ..config.availables import EXTENSIONS, MODELS, OPTIMIZERS, METRICS


################################################################################################################################
# SUB-FUNCTIONS
################################################################################################################################
def _get_package_dir():
    """Returns directory containing MLflow python package."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(current_dir, os.pardir))


################################################################
# sort_labels
################################################################
def sort_labels(labels):
    '''
    클래스 순서를 정렬
    sort_labels([NG_1, OK, NG_2, OK, NG_1, ...]) -> ['OK', 'NG_1', 'NG_2', 'NG_3']
    '''
    PATTERN_OK = 'ok'
    INCLASS_REVERSE = False
    
    classes = set(labels)
    ok_labels = sorted({l for l in labels if isinstance(l, (int, bool, np.int, np.bool_)) or PATTERN_OK in l.lower()}, reverse=INCLASS_REVERSE)
    other_labels = sorted({l for l in labels if l not in ok_labels}, reverse=INCLASS_REVERSE)
        
    return ok_labels + other_labels


################################################################
# encode labels
################################################################
def encode_labels(labels, force_binary=False, class_nothing='ok'):
    '''
    encode labels
    
    Parameters
    ----------
    labels : np.ndarray or list or pd.Series or pd.DataFrame
    binary : boolean
      n-level labels to n binary labels
    class_nothing : string
      class of nothing (when binary is True)
      
    Examples
    --------
    >>> encode_labels([OK, NG, OK, NG])
    (np.array([0, 1, 0, 1]), 'label', {0: 'OK', 1: 'NG'})
    >>> encode_labels([OK, NG, OK, NG], forced_binary=True)
    (np.array([[1, 0], [0, 1], [1, 0], [0, 1]]), ['OK', 'NG'], {0: 'OK', 1: 'NG'})
      
    Returns
    -------
    encoded_label : np.ndarray
    classes : list
    decoder : dict
    '''
    
    # other types to np.ndarray
    if isinstance(labels, pd.Series):
        classes = [labels.name]
        labels = labels.to_numpy()
    elif isinstance(labels, pd.DataFrame):
        classes = labels.columns.to_list()
        labels = labels.to_numpy() if len(classes) > 1 else labels.iloc[:, 0].to_numpy()
    elif isinstance(labels, list):
        classes = ['label']
        labels = np.array(labels)

    # type check
    if not isinstance(labels, np.ndarray):
        raise TypeError(f"Input labels is not in ['list', 'np.array', 'pd.Series', 'pd.DataFrame']!")

    # generate encoder, decoder
    names = sort_labels(labels.flatten())    
    n_classes = len(names)
    
    # expand labels if force_binary
    if labels.ndim == 1 or labels.shape[1] == 1:
        if force_binary:
            classes, expanded_labels = [], []
            for name in [name for name in names if class_nothing not in name.lower()]:
                classes.append(name)
                expanded_labels.append(np.array(labels==name, dtype=int))
            encoded_labels = np.array(expanded_labels).T
            decoder = {0: False, 1: True}
            is_binary = True
        else:
            encoder = {name: code for code, name in enumerate(names)}
            classes = list(encoder.keys())
            encoded_labels = np.array([encoder[x] for x in labels])
            decoder = {code: name for code, name in enumerate(names)}
            is_binary = False
    else:
        encoder = {name: code for code, name in enumerate(names)}
        encoded_labels = []
        for nth_labels in labels.T:
            nth_encoded_labels = np.array([encoder[x] for x in nth_labels])
            encoded_labels.append(nth_encoded_labels)
        encoded_labels = np.array(encoded_labels).T
        decoder = {code: name for code, name in enumerate(names)}
        is_binary = True
        
    return encoded_labels, is_binary, classes, decoder


################################################################
# make labels inferred from subdirs
################################################################
def make_dataset_df(root, hrchy='label', extensions='all'):
    '''
    root 내 파일들의 filename, filepath 및 하위 디렉토리 이름을 데이터프레임으로 반환
    
    Args:
      root                           root directory
      hrchy <string> or <list>       'label', 'split/label', ['split', 'label']
      extensions <string> or <list>  'all', 'image', 'audio', ['jpg', 'png'], ...
    
    Return:
      <pd.DataFrame>
      
    Examples:
      아래 구조의 hrchy는 'channel/label'임
        ./dataset
            ├ CH1
            │   ├ NG
            │   └ OK
            └ CH2
                ├ NG
                └ OK
      >>> df = make_dataset_df('./dataset', 'channel/label', extension='audio')
    '''
    
    if not isinstance(hrchy, list):
        hrchy = hrchy.split('/')
    
    if type(extensions) is not list:
        exts = EXTENSIONS[extensions] if extensions in EXTENSIONS.keys() else [extensions]
    else:
        exts = [ext.strip('.') for ext in extensions]
        
    files = [f for fs in [Path(root).glob(f"**/*.{ext}") for ext in exts] for f in fs]
    
    if len(files) == 0:
        raise FileNotFoundError(f"File {', '.join([f'*.{ext}' for ext in exts])} not found!")
        
    df = pd.DataFrame({
        'filepath': [str(f) for f in files],
        'hrchy': [str(f).replace(root, '').strip('/') for f in files]
    })

    fields = df['hrchy'].str.split('/', expand=True).iloc[:, :len(hrchy)]
    fields.columns = hrchy
    
    # merge labels with fields
    df = pd.concat([df, fields], axis=1).drop(columns='hrchy')
    
    return df


################################################################
# split_dataset
################################################################
def split_dataset(dataset, ratio=0.2):
    '''
    split dataset to trainset and testset, or split trainset to trainset and validation-set
    if ratio is single value, the ratio becomes second ratio - ratio=0.2 -> ratio=[0.8, 0.2]
    
    Args:
      dataset
      ratio
      
    Returns:
      dataset_a, dataset_b, ...
    '''
    
    # scalar to list
    if not isinstance(ratio, (list, tuple)):
        ratio = [1-ratio, ratio]
    
    # raise error if sum of ratios is not 1
    if sum(ratio) != 1:
        raise ValueError(f"Sum of {', '.join([str(r) for r in ratio])} is not 1.0!")
    
    # get n_each
    n = len(dataset)
    indices = np.arange(0, n, 1)
    n_split = [int(n*r) for r in ratio]
    n_split[-1] = n - sum(n_split[:-1])
    
    return random_split(dataset, n_split)


################################################################
# list_availables
################################################################
def list_availables(dict_: dict, search: str=None, sort: str=None, return_: bool=False):
    '''
    직접 사용하지 않음. 다른 함수들이 호출하여 사용.
    
    Arguments
    ---------
    dict_
      MODELS, CRITERIONS, OPTIMIZERS, or METRICS (avaialables 모듈에 정의되어 있는)
    search
      keyword for pattern match
    sort
      column names for sort values
    return_
      for REST API - if true it returns dictionary
    '''
    if search is not None:
        dict_ = {k: v for k, v in dict_.items() if parser.prep_args(search) in k}
    
    tbl = pd.DataFrame.from_records(data=list(dict_.values()), index=list(dict_.keys()))
    tbl = tbl[[c for c in tbl.columns if c not in ['classifier', 'class']]]
    tbl = tbl.fillna('')
    
    if sort is not None:
        if sort == 'top_1_acc':
            tbl = tbl.sort_values(sort, ascending=False)
        else:
            tbl = tbl.sort_values(sort, ascending=True)

    if return_:
        return tbl.to_dict(orient='index')
    
    print(tbl.to_markdown(tablefmt='simple'))
    
def list_models(search=None, sort=None, return_=False):
    output = list_availables(MODELS, search=search, sort=sort, return_=return_)
    if output is not None:
        return output
    
def list_criterions(search=None, sort=None, return_=False):
    output = list_availables(CRITERIONS, search=search, sort=sort, return_=return_)
    if output is not None:
        return output
    
def list_optimizers(search=None, sort=None, return_=False):
    output = list_availables(OPTIMIZERS, search=search, sort=sort, return_=return_)
    if output is not None:
        return output
    
def list_metrics(search=None, sort=None, return_=False):
    output = list_availables(METRICS, search=search, sort=sort, return_=return_)
    if output is not None:
        return output
