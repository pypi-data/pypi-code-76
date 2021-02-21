from functools import reduce
import numpy as np

def conjunction(*conditions):
    return reduce(np.logical_and, conditions)

def filter_spec(df, f, k1, k2, t_name, code, p=0):
    """
    df is dataframe
    f is feature of dataframe
    s is small numbers
    b is bigs numbers
    """
    # if p == 0:
    #     df['p'] == 0
    l = []
    sb_list = zip(f, k1, k2)
    for feature, small, big in sb_list:
        l.append(df[feature].between(small, big, inclusive=False))
    # l.append(df['p'] >= p)
    df.loc[conjunction(*l), t_name] = 1
    df.loc[conjunction(*l), 'code'] = code
    # print(f"F: {f}")
    # print(f"K1: {k1}")
    # print(f"K2: {k2}")
    return df
