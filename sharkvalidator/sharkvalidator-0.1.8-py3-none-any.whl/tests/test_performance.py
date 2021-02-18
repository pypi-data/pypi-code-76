# Copyright (c) 2021 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-01-08 11:50

@author: johannes

"""
import time
import pandas as pd

# df = pd.DataFrame({k: [3, 4, 6] for k in range(100000)})
df = pd.DataFrame({k: range(100000) for k in [4]})
# ll = df[4].unique()
ll = set(df[4])
start_time = time.time()
6747 in ll
print("--%.9f sec" % (time.time() - start_time))

# f = pd.ExcelFile('C:/Temp/DV/validator_test/Hallands kustkontroll kvartal 2_2020.xlsx')
# df = f.parse(
#     'Kolumner',
#     header=2,
#     dtype=str,
#     keep_default_na=False,
# ).fillna('')
