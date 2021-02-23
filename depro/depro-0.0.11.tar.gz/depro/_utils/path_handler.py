# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

path handler

@author: tadahaya
"""
from pathlib import Path
import os

def get_base():
    """ get base path """
    return os.path.dirname(__file__)


def get_filepath(p,extension="txt"):
    """ obtain paths and file names of files in the indicated directory """    
    p2 = Path(p)
    paths = list(map(lambda x: x.as_posix(),list(p2.glob("*.{}".format(extension)))))
    names = [v.split("/")[-1].replace(".{}".format(extension),"") for v in paths]
    return paths,names


