#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:28:02 2020

@author: ageiges
"""


import xarray as xr
import numpy as np
import pandas as pd
#%%

        #%%
   
    median = xData.loc['ITA',:,:].median(dim='pathway').plot()
    
    xData.loc['ITA',:,:].min(dim='pathway').plot()
    xData.loc['ITA',:,:].max(dim='pathway').plot()
    
    xData.loc['ITA',:,:].quantile(.9, dim='pathway').plot()
    xData.loc['ITA',:,:].quantile(.1, dim='pathway').plot()
    xData.loc['ITA',:,:].plot.line(x='year', color = 'gray')
    xData.plot()