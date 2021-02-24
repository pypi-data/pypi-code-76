from . import ClassMethod, Struct


class ClassMethodGroupBy(ClassMethod):
    _class_name: str = 'groupby'


class GroupBy(Struct, metaclass=ClassMethodGroupBy):
    _class_name: str = 'groupby'
