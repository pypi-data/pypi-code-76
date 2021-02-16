import numpy as np

''' Библиотека для импорта во внешние модули (np по дэфолту) '''
core = np


def set_core_type(lib_type: str):
    ''' Устанавливает тип библиотеки numpy | cupy '''
    
    global core

    if lib_type == 'cpu':
        core = np
    elif lib_type == 'gpu':
        try:
            import cupy as cp
        except ModuleNotFoundError:
            raise Exception('CuPy lib not found, try to install it')
        
        core = cp
    else:
        raise Exception('Unexpected `lib_type`')
