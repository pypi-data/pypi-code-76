import functools
type_cache = {}

class jsiter_base:
    pass

def jsiter(self_obj):
    if type(self_obj) in type_cache:
        return type_cache[type(self_obj)](self_obj)
    iter(self_obj)
#     if type(self_obj) == str:
#         return self_obj
    class jsiter_class(jsiter_base):
        def __init__(self,self_obj):
            self.__jsiter_original_obj = self_obj
        def map(self,func):
            return jsiter(map(func,self.__jsiter_original_obj))
        def filter(self,func):
            return jsiter(filter(func,self.__jsiter_original_obj))
        def reduce(self,func):
            iter_obj = iter(self.__jsiter_original_obj)
            ret = functools.reduce(func,iter_obj, next(iter_obj))
            try:
                return jsiter(ret)
            except TypeError:
                return ret
        def list(self):
            return jsiter(list(self.__jsiter_original_obj))
        def sorted(self, *args, **kwargs):
            return jsiter(sorted(self.__jsiter_original_obj, *args, **kwargs))
        def join(self,Jstr):
            ret = Jstr.join(self)
            try:
                return jsiter(ret)
            except TypeError:
                return ret
    def decorator_jsiter(func):
        def _decorator_jsiter(*args, **kwargs):
            args = [a._jsiter_class__jsiter_original_obj if issubclass(type(a), jsiter_base) else a for a in args]
            ret = func(*args, **kwargs)
            if func.__name__ in ["__repr__","__str__"]:
                return ret
            elif type(ret) == type(args[0]):
                return jsiter_class(ret)
            else:
                return ret
        return _decorator_jsiter
    for d in dir(type(self_obj)):
        if d not in ["__class__","__init__","__new__","__setattr__","__getattribute__","__delattr__","__dir__"] :
            attrset = getattr(type(self_obj), d)
            if callable(attrset):
                setattr(jsiter_class,d, decorator_jsiter(attrset))
            else:
                setattr(jsiter_class,d, attrset)
    jsiter_class.__name__ = "jsiter_" + type(self_obj).__name__
    type_cache[type(self_obj)] = jsiter_class
    return jsiter_class(self_obj)