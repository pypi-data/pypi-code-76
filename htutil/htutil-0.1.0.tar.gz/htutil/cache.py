'''
Author: HaoTian Qi
Date: 2021-02-18 13:40:42
Description: function result cache
LastEditTime: 2021-02-18 13:58:34
LastEditors: HaoTian Qi
FilePath: \htutil\htutil\cache.py
'''
import time
import pickle as pkl
from pathlib import Path
import inspect


def file_cache(function):
    def fun(*args, **kwargs):
        dir_tmp = Path('.') / 'tmp'
        file_name = Path(inspect.getframeinfo(
            inspect.currentframe().f_back).filename).name

        if not dir_tmp.exists():
            dir_tmp.mkdir()

        cache_path = dir_tmp / f"{file_name}-{function.__name__}.pkl"
        if not cache_path.exists():
            result = function(*args, **kwargs)
            with open(cache_path, 'wb') as f:
                pkl.dump(result, f)
            return result
        else:
            with open(cache_path, 'rb') as f:
                result = pkl.load(f)
            return result
    return fun

@file_cache
def get_1():
    time.sleep(3)
    return 1


def main():
    print(get_1())


if __name__ == '__main__':
    main()
