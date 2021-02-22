# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:50:49 2021

@author: Srirag
"""
import os

def locator(text,path):
    total_file,file_name=[]
    
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            total_file.append(os.path.join(root,name))
    
    for filename in total_file:
        try:
            with open(filename) as f:
                      if text in f.read():
                          file_name.append(filename)
        except: pass
    
    return file_name