import os
import sys
import random
import zipfile
import numpy as np
import pandas as pd
from tqdm import tqdm


def seed_everything(seed=914):
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


def progressbar(iteration, prefix="", size=50, file=sys.stdout):
    
    def show(t):
        x = int(size*t/count)
        file.write("{}| {}{} | {}%\r".format(prefix, "█"*x, "."*(size-x), int(100*t/count)))
        file.flush()
    
    count = len(iteration)
    show(0)
    for i, item in enumerate(iteration):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()


def extract_zip_file(src_path, trg_path):
    with zipfile.ZipFile(r"{}".format(src_path), 'r') as extractor:
        # Print all the contents of the zip file
        extractor.printdir()
        # Extract all the files
        print('Extracting all the files now...')
        extractor.extractall(path=r"{}".format(trg_path))
        print('Done!')


def threshold_search(y_true, y_proba):
    best_threshold = 0
    best_score = 0
    for threshold in tqdm([i * 0.01 for i in range(100)], disable=True):
        score = metrics.f1_score(y_true=y_true, y_pred=y_proba > threshold)
        if score > best_score:
            best_threshold = threshold
            best_score = score
    search_result = {'threshold': best_threshold, 'f1': best_score}
    return search_result


def pretty_print_matrix(M, rows=None, cols=None, dtype=float, float_fmt="{0:.04f}"):
    df = pd.DataFrame(M, index=rows, columns=cols, dtype=dtype)
    old_fmt_fn = pd.get_option('float_format')
    pd.set_option('float_format', lambda f: float_fmt.format(f))
    display(df)
    pd.set_option('float_format', old_fmt_fn)


def type_of_columns(data, label_col=None, show=True):
    df = data.copy()
    if label_col is not None:
        df = df.drop(label_col, axis=1)
    int_features = []
    float_features = []
    object_features = []
    for dtype, feature in zip(df.dtypes, df.columns):
        if dtype == 'float64':
            float_features.append(feature)
        elif dtype == 'int64':
            int_features.append(feature)
        else:
            object_features.append(feature)
    if show:
        print(f'{len(int_features)} Integer Features : {int_features}\n')
        print(f'{len(float_features)} Float Features : {float_features}\n')
        print(f'{len(object_features)} Object Features : {object_features}')
    return int_features, float_features, object_features


class DictObj(object):
    def __init__(self, dictionary):
        import pprint
        self.map = dictionary
        pprint.pprint(dictionary)

    def __setattr__(self, name, value):
        if name == 'map':
            # print("init set attr", name ,"value:", value)
            object.__setattr__(self, name, value)
            return
        # print('set attr called ', name, value)
        self.map[name] = value

    def __getattr__(self, name):
        # print('get attr called ', name)
        return  self.map[name]
