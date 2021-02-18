# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-08 11:50

@author: johannes

"""
import time
import pandas as pd


if __name__ == '__main__':
    # df = pd.DataFrame({k: [3, 4, 6] for k in range(100000)})
    # df = pd.DataFrame({k: range(100000) for k in [4]})
    # ll = df[4].unique()
    # ll = set(df[4])
    start_time = time.time()

    print("--%.9f sec" % (time.time() - start_time))

