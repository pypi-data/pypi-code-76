#!/usr/bin/env python
# coding: utf-8

# In[1]:


__version__ = 'v20201225'

import numpy as np
import matplotlib.pyplot as plt

class BradException(Exception): pass

OBJECT, DARK, LIGHT = 0, 125, 255

def light_side_of(M, start_index, start_from, stop_index_list, LIGHT, OBJECT):
    Ny, Nx = M.shape
    
    assert start_from in ['left', 'right', 'bottom', 'top']
    if start_from in ['left', 'right']:
        assert (0 <= start_index) and (start_index < Nx)
    else:
        assert (0 <= start_index) and (start_index < Ny)
    
    if start_from == "left":
        lsrc = np.full(Ny, True) # set light source
        for n in range(start_index, Nx): # propagate light from left to right
            if n in stop_index_list: break
            lsrc[M[:,n]==OBJECT] = False   # when meet objects, turn off light source
            if not lsrc.any(): break
            M[lsrc,n] = LIGHT
    elif start_from == "right":
        lsrc = np.full(Ny, True) # set light source
        for n in reversed(range(start_index + 1)): # propagate light from right to left
            if n in stop_index_list: break
            lsrc[M[:,n]==OBJECT] = False  # when meet objects, turn off light source
            if not lsrc.any(): break
            M[lsrc,n] = LIGHT
    elif start_from == "top":
        lsrc = np.full(Nx, True) # set light source
        for n in range(start_index, Ny): # propagate light from bottom to top
            if n in stop_index_list: break
            lsrc[M[n,:]==OBJECT] = False  # when meet objects, turn off light source
            if not lsrc.any(): break
            M[n,lsrc] = LIGHT
    elif start_from == "bottom":
        lsrc = np.full(Nx, True) # set light source
        for n in reversed(range(start_index + 1)): # propagate light from top to bottom
            if n in stop_index_list: break
            lsrc[M[n,:]==OBJECT] = False  # when meet objects, turn off light source
            if not lsrc.any(): break
            M[n,lsrc] = LIGHT
            
    return M

def convert_data_to_matrix(data, y_resolution=100):
    assert len(data.shape) == 1 # assert that data be rank 0
    assert y_resolution >= 2 # resolution has to be more than 1
    
    min_data, max_data = data.min(), data.max()
    
    Nx = len(data) # the number of data points
    Ny = y_resolution # the number of y-axis resolution
    nx = np.arange(0, Nx) # column indices for matrix M
    ny = ((max_data - data) / (max_data - min_data) * (Ny-1)).round(0).astype(int) # row indices for matrix M
    
    #---------------------------------------------------------------
    M = np.full((Ny, Nx), LIGHT, dtype=np.uint8) # initialize matrix
    M[ny,nx] = OBJECT # draw data points on the matrix
    
    #---------------------------------------------------------------
    MM = np.full((Ny, 2*Nx-1), DARK, dtype=np.uint8) # an expanded version of matrix
    MM[ny, np.arange(0,2*Nx-1,2)] = M[ny,nx] # draw original data points
    MM[ny[0:-1], np.arange(1,2*Nx-1,2)] = M[ny[0:-1],nx[0:-1]] # fill mid-points with left points
    MM[ny[1:], np.arange(1,2*Nx-1,2)] = M[ny[1:],nx[1:]] # fill mid-points with right points
    MM = light_side_of(MM, 0, "top", [], LIGHT, OBJECT) # light from the top 
    MM = light_side_of(MM, Ny-1, "bottom", [], LIGHT, OBJECT) # light from the bottom
    MM[MM==DARK] = OBJECT # fill mid-points by converting the dark area into the object
    
    #---------------------------------------------------------------
    y_pixel_size = (max_data - min_data) / (Ny - 1)
    
    return MM, y_pixel_size

def convert_matrix_to_image(M):
    img = np.zeros((*M.shape, 3), dtype=np.uint8) # initialize
    img[:] = M.reshape(*M.shape, 1)
    return img

def find_valley_in_matrix(data, ilows, MM, iMMlows, y_pixel_size, threshold, pour_water_from='top'):
    M = MM[:,0::2]
    
    if pour_water_from == 'top':
        water_depth = data.max() - data - (M==DARK).argmax(axis=0) * y_pixel_size # ref level - depth - local level
    elif pour_water_from == 'bottom':
        water_depth = data - data.min() - (M==DARK)[::-1,:].argmax(axis=0) * y_pixel_size # ref level - depth - local level
    else:
        BradException("Brad Error: only 'top' or 'bottom' is allowed...")
    water_depth[(M!=DARK).all(axis=0)] = float('-inf') # no water region
    water_depth[water_depth < threshold] = float('-inf') # ignore if the water depth is below threshold
    
    ilow = np.full(len(data), False) # initialize
    if np.isfinite(water_depth).any(): 
        ilow[np.nanargmax(water_depth)] = True

    ilows[ilow] = True # update by adding ilow to ilows
    
    #---------------------------------------------------------------
    iMMlow = np.full(iMMlows.shape, False)
    iMMlow[0::2] = ilow
    
    if iMMlow.any(): # remove water if the lowest is found in that region
        stop_index_list = np.flatnonzero(iMMlows)
        MM = light_side_of(MM, iMMlow.argmax(), 'left', stop_index_list, LIGHT, OBJECT) # spill over-flow to the left
        MM = light_side_of(MM, iMMlow.argmax(), 'right', stop_index_list, LIGHT, OBJECT) # spill over-flow to the right
        
    iMMlows[iMMlow] = True # update by adding iMMlow to iMMlows
    
    return ilow, ilows, MM, iMMlows

def find_valleys_in_data(data, threshold, pour_water_from='top', y_resolution=100, verbose=True):
    MM, y_pixel_size = convert_data_to_matrix(data, y_resolution=y_resolution)
    if verbose: plt.figure(figsize=(20,5)); plt.imshow(convert_matrix_to_image(MM)); plt.show()
    
    iMMlows = np.full(MM.shape[1], False) # initialize
    ilows = np.full(len(data), False) # initialize
    
    # initialize water level
    if pour_water_from == 'top':
        MM = light_side_of(MM, 0, pour_water_from, [], DARK, OBJECT)  # fill with water
    if pour_water_from == 'bottom':
        MM = light_side_of(MM, MM.shape[0]-1, pour_water_from, [], DARK, OBJECT)  # fill with water
    else:
        BradException("Brad Error: only 'top' or 'bottom' is allowed...")
    MM = light_side_of(MM, 0, 'left', [], LIGHT, OBJECT) # spill over-flow to the left
    MM = light_side_of(MM, MM.shape[1]-1, 'right', [], LIGHT, OBJECT) # spill over-flow to the right
    if verbose: plt.figure(figsize=(20,5)); plt.imshow(convert_matrix_to_image(MM)); plt.show()

    for i in range(len(data)):
        if verbose: print(f'> iteration = {i+1}')
        ilow, ilows, MM, iMMlows = find_valley_in_matrix(data, ilows, MM, iMMlows, y_pixel_size, threshold, pour_water_from=pour_water_from)
        if verbose: plt.figure(figsize=(20,5)); plt.imshow(convert_matrix_to_image(MM)); plt.show()
        if not ilow.any(): break
            
    return ilows


# In[2]:


def find_nears(data, ilows, threshold, threshold_margin, pour_water_from='top', y_resolution=100, verbose=True):
    MM, y_pixel_size = convert_data_to_matrix(data, y_resolution=100)
    if verbose: plt.figure(figsize=(20,5)); plt.imshow(convert_matrix_to_image(MM)); plt.show()

    if pour_water_from == 'bottom':
        MM = MM[::-1,:]
        
    iMMlows = np.full(MM.shape[1], False)
    iMMlows[0::2] = ilows

    Nx = len(iMMlows)
    for idx in np.flatnonzero(iMMlows): # lows index
        # initialize light source
        iobj = (MM[:,idx] == OBJECT)
        nerr = max(0, np.flatnonzero(iobj)[0] - int(np.round(threshold_margin/y_pixel_size,0)))

        lsrc = ~iobj
        lsrc[:max(0, np.flatnonzero(iobj)[0] - int(np.round(threshold/y_pixel_size,0)))] = False
        lsrc[np.flatnonzero(iobj)[-1]:] = False

        # right sweep
        lsrc_r = lsrc.copy()
        for n in range(idx, Nx): # propagate light from left to right
            iobj = (MM[:,n] == OBJECT)
            lsrc_r[iobj] = False   # when meet objects, turn off light source
            if not lsrc_r.any(): break
            MM[nerr:iobj.argmax(),n] = DARK

        # left sweep
        lsrc_l = lsrc.copy()
        for n in reversed(range(idx)): # propagate light from left to right
            iobj = (MM[:,n] == OBJECT)
            lsrc_l[iobj] = False   # when meet objects, turn off light source
            if not lsrc_l.any(): break
            MM[nerr:iobj.argmax(),n] = DARK

    if verbose: plt.figure(figsize=(20,5)); plt.imshow(convert_matrix_to_image(MM)); plt.show()

    iMMnearlows = (MM==DARK).any(axis=0)
    inearlows = iMMnearlows[0::2]
    return inearlows

def find_highs_and_lows(data, percent_threshold=5, percent_threshold_margin=0.5, y_resolution=100, verbose=False):   # percent_threshold [%]    
    log_data = np.log(data)
    threshold = np.log(1 + percent_threshold/100)
    threshold_margin = np.log(1 + percent_threshold_margin/100)
    
    if verbose: print('>> Finding lows...')
    ilows  = find_valleys_in_data(log_data, threshold, pour_water_from='top', y_resolution=y_resolution, verbose=verbose)
    if verbose: print('>> Finding highs...')
    ihighs = find_valleys_in_data(log_data, threshold, pour_water_from='bottom', y_resolution=y_resolution, verbose=verbose)
    if verbose: print('>> Finding nearlows...')
    inearlows = find_nears(log_data, ilows, threshold, threshold_margin, pour_water_from='top', y_resolution=y_resolution, verbose=verbose)
    if verbose: print('>> Finding nearhighs...')
    inearhighs = find_nears(log_data, ihighs, threshold, threshold_margin, pour_water_from='bottom', y_resolution=y_resolution, verbose=verbose)
    
    return ihighs, ilows, inearhighs, inearlows


# # Test Code

# In[4]:


if __name__=='__main__':
    import pandas as pd
    import time
    import csv

    #--- example data 1 --------------------------------------------
#     x = np.linspace(-0.5, 0.5, 1000)
#     data = 1.0 + (0.05/2 + 0.01*x)*np.sin(42*x) # example: sine wave
    
    #--- example data 2 --------------------------------------------
    data0 = []
    with open('sample_data/KRW.csv','r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i ==0:
                header = row
            else:
                data0.append({k:v for k,v in zip(header, row)})
    data1 = sorted(data0, key=lambda x: x['Date'])
    data = np.array([float(r['Price']) for r in data1])
    
    #--- find lows, highs, and nears -----------------------------
    percent_threshold=5.0 # [%]
    percent_threshold_margin=1.0 # [%]
    y_resolution=100
#     verbose=True
    verbose=False
    
    tic = time.time()
    ihighs, ilows, inearhighs, inearlows = find_highs_and_lows(data, percent_threshold=percent_threshold, percent_threshold_margin=percent_threshold_margin, y_resolution=y_resolution, verbose=verbose)
    toc = time.time()
    print(str(toc-tic) + " sec")
    
    #--- plot results --------------------------------------------
    ss = pd.Series(data)
    ss.plot(color='black', figsize=(20,5))
    ss.loc[ihighs].plot(color='blue', marker='o', linewidth=0, markersize=12, markerfacecolor='none')
    ss.loc[ilows].plot(color='red', marker='o', linewidth=0, markersize=12, markerfacecolor='none')
    ss.loc[inearhighs].plot(color='blue', marker='o', linewidth=0, markersize=4)
    ss.loc[inearlows].plot(color='red', marker='o', linewidth=0, markersize=4)
    plt.show()


# In[ ]:




