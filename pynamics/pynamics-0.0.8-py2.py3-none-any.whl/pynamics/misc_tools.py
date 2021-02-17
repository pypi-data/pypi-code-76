#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:01:38 2020

@author: danaukes
"""

def delete_all_local(name = '__main__'):
    import sys
    import pynamics.blank_module
    
    m = sys.modules['pynamics.blank_module']
    default_variables = dir(m)
    
    main = sys.modules[name]
    all_variables = dir(main)
    
    variables_to_delete = list(set(all_variables) - set(default_variables))
    for item in variables_to_delete:
        delattr(main,item)