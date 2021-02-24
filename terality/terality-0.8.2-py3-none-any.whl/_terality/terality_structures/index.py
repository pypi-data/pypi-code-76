import pandas as pd

from . import ClassMethod, Struct, StructIterator


class ClassMethodIndex(ClassMethod):
    _class_name: str = 'index'
    _pandas_class = pd.Index


class Index(Struct, metaclass=ClassMethodIndex):
    _class_name: str = 'index'
    _pandas_class_instance = pd.Index([])
    _additional_methods = Struct._additional_methods | {'get_range_auto'}

    def __iter__(self):
        return StructIterator(self)


class ClassMethodMultiIndex(ClassMethod):
    _class_name: str = 'index'
    _pandas_class = pd.MultiIndex


class MultiIndex(Struct, metaclass=ClassMethodMultiIndex):
    _class_name: str = 'multi_index'
