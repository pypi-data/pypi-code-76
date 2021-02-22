# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 16:50:49 2021

@author: Srirag
"""
import os

def locate(text,path):
    total_file,file_name=[],[]
    
    for root, dirs, files in os.walk(path, topdown=True):
        for name in files:
            total_file.append(os.path.join(root,name))
    
    for filename in total_file:
        try:
            with open(filename) as f:
                content=f.read().lower().split('\n')
                line_no=[]
                for no,line in enumerate(content):
                      if text.lower() in line:
                          line_no.append(no+1)
                if line_no !=[]:
                    file_name.append({"Filename":filename,"Lines":line_no})
        except: pass
    if file_name !=[]:   
        return file_name
    else:
        return "No match found"

