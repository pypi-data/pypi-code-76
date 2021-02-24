# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:36:32 2021

@author: ADMIN
"""
import pandas as pd
import numpy as np


def clip_save(name):
    """ Save clipboard data into .csv with given filename
        Please be cautious to put '' or str object input 
    
    :param str name: Assigned file name by user
    
    :returns: (pd.DataFrame) event detected raw data
    
    ::
        
        bring data in clipboard
        >>> data = clipboard_to_csv('name')
        >>> type(data)
        pandas.core.frame.DataFrame
        
    """
    
    
    assert isinstance(name, str), TypeError('Invalid file name datatype')
    df = pd.read_clipboard(sep = '\t', index_col = 0) 
    if name.lower().endswith('.csv'):
        df.to_csv(name) 
    else:
        name += '.csv'
        
    data = pd.read_clipboard(sep = '\t', index_col = 0)
    data.to_csv('mini_'+ name) 
    
    return data



#그런데 이건 굳이 넣어야하나 싶긴 함)
def clip_unsave():
    """Bring clipboard data into dataframe without file saving
    
    :returns: (pd.Dataframe) dataframe from clipboard
    
    ::
        
        bring data in clipboard
        >>> clip_unsave()
        

    """
    
    
    return pd.read_clipboard(sep = '\t', index_col = 0)
    
    
    
    
def mini_processing(mini_data, base = 'max'):
    """ processing to get 5 parameters in mini_anlaysis data
        Recommend to get input data from clip_save() or clip_unsave()
    
    :param pd.DataFrame mini_data: mini analyzed event detection list, should be given by using 'pd.read_cipboard()' (because column name & format is sensitive to use this function)
    
    :returns: 
    ux (np.ndarray) detected time stamp of event (unit : sec)
    ux (np.ndarray) amplitude * peak direction
    t1 (np.ndarray) detected rise tau (unit : sec)
    t2 (np.ndarray) detected decay(fall) tau (unit : sec)
    b (float) baseline
    
    ::
        
        (copy and bring in saved state in clipboard)
        >>>ux, uy, t1, t2 = mini_processing(sample_data)
        >>> type(ux)
        numppy.ndarray
        >>>y = init_based_psc_multiple(ux, uy, t1, t2)
        >>>x = np.arange(-1000,1000,10)
        >>>plt.plot(x, y)
    
    """
    assert isinstance(mini_data, pd.DataFrame), TypeError('Invalid file data type : use pd.DataFrame')
    #assert ('Time (ms)' in mini_data.columns.to_list()), TypeError('Input Dataframe does not have Time column')
        
    tmp = mini_data['Time (ms)'].apply(lambda x: float(x.replace(',', '')))
    ux = (tmp.to_numpy())/1000
    uy = ((mini_data['Amplitude']* mini_data['Peak Dir']).to_numpy())
    t1 = (mini_data['Rise (ms)'].to_numpy())/1000
    t2 = (mini_data['Decay (ms)'].to_numpy())/1000
    b = mini_data['Baseline'].mean()
   
    return ux, uy, t1, t2, b


def clampfit_processing(cf_data):
    
    assert isinstance(cf_data, pd.DataFrame), TypeError('Invalid file data type : use pd.DataFrame')
    cf2_data = cf_data.iloc[:, [6,7,9,17,18]].replace('Not found', np.NaN)
    data = cf2_data.dropna(axis = 0)
    
    ux = (data.iloc[:, 2].to_numpy())/1000
    uy = ((data.iloc[:, 1]).to_numpy())
    t1 = (data.iloc[:, 3].astype(float).to_numpy())/1000
    t2 = (data.iloc[:, 4].astype(float).to_numpy())/1000
    b = data.iloc[:, 0].mean()
    
    
    return ux, uy, t1, t2, b



#--------------------------------------------------------------------
# Error function
#--------------------------------------------------------------------

def get_iou(x, y1, y2):
    """Get IoU(Intersecion over Union) specific to 2 graph: (x,a), (x,b)
    
    :param np.ndarray x: x value of (x,y) ordered pair to calculate delta x for area
    :param np.ndarray a: y valuesof one func/object
    :param np.ndarray b: y values of the other func/object
    
    :returns: 
    iou (int | float)
    each area's unit is (sec * pA)000
    
    
    """
   
    
    assert isinstance(x, np.ndarray), TypeError('Invalid Datatype of x : Recommend to use x.to_numpy()')
    assert isinstance(y1, np.ndarray), TypeError('Invalid Datatype of a ')
    assert isinstance(y2, np.ndarray), TypeError('Invalid Datatype of b')
    
    length = np.zeros(min(len(y1), len(y2)))
    intersection = 0
    union = 0

    for i in range(min(len(y1), len(y2))):
        length[i] = min(abs(y1[i]), abs(y2[i]))
        delta = x[2] - x[1]
        delta_inter = length[i] * delta
        intersection += delta_inter
        
    for p in range(min(len(y1), len(y2))):
        delta_union = max(abs(y1[p]), abs(y2[p])) * delta
        union += delta_union
        
    iou = intersection/union
    return iou


    
    
    
    
    