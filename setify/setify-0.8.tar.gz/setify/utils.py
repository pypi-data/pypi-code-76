# url link to JSON file
# file_name to cash the dataset if not exists
import datetime
import json
import math
import os
import sys
import urllib.request
from pathlib import Path
from time import sleep
from colorama import Fore
import pandas as pd
from tqdm import tqdm

import setify


def load_data(origin, fname):
    return get_file(origin, fname)


def get_file(origin, fname, cache_dir=None, cache_subdir='datasets'):
    """
    - if cache dir is not provided
    - if no access to ~ directory use tmp
    - add sub directory
    - if directory not exists make one
    - if file doesn't exists download it
    - save as pickle file
    """
    if cache_dir is None:
        cache_dir = os.path.join(str(Path.home()), '.setify')

    datadir_base = os.path.expanduser(cache_dir)

    if not os.access(str(Path.home()), os.W_OK):
        datadir_base = os.path.join('/tmp', '.setify')
    datadir = os.path.join(datadir_base, cache_subdir)

    if not os.path.exists(datadir):
        os.makedirs(datadir)
    fpath = os.path.join(datadir, fname)
    print(fpath)

    download = False
    if os.path.exists(fpath):
        # File found; verify integrity if a hash was provided.
        pass
    else:
        download = True

    if download:
        print('Downloading data from', origin)
        meta = {'date-time': datetime.datetime.now(),
                'version': setify.__version__}

        with urllib.request.urlopen(origin) as response, pd.HDFStore(fpath, 'w') as f:
            content_type = response.info().get('Content-Length')
            total_size = -1
            if content_type is not None:
                total_size = int(content_type.strip())

            chunk_size = int(total_size / 10)
            data = ''
            print(Fore.WHITE + 'file size: ', convert_size(total_size))
            print(Fore.WHITE + 'file location: ', fpath)
            with tqdm(total=total_size,
                      unit='B', unit_scale=True, unit_divisor=chunk_size,
                      bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.WHITE, Fore.WHITE)) as progress:
                while True:
                    chunk = response.read(chunk_size)
                    data = data + chunk.decode()

                    if not chunk:
                        break

                    progress.set_postfix(file=fpath, refresh=True)
                    progress.update(len(chunk))
                    sleep(.01)

            json_data = json.loads(data)

            df = pd.DataFrame(json_data)
            f.append(key='/dataset1', value=df)
            f.get_storer('/dataset1').attrs.metadata = meta
            f.close()

    return fpath


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def frame_information(df):
    x = df[:5]
    y = pd.DataFrame([['...'] * df.shape[1]],
                     columns=df.columns, index=['...'])
    z = df[-5:]
    frame = [x, y, z]
    result = pd.concat(frame)
    print(Fore.GREEN +  str(result))
    print('[' + str(df.shape[0]) + ' rows x ' + str(df.shape[1]) + ' columns]')
  
