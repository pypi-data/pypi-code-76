from abc import ABC, abstractmethod, ABCMeta

from py4j.java_gateway import JavaObject

from ..conversion.java_method_call import auto_convert_java_type
from ..conversion.type_converters import j_value_to_py_value

__all__ = ['JavaObjectWrapper', 'JavaObjectWrapperWithFunc', 'JavaObjectWrapperWithAutoTypeConversion']


class JavaObjectWrapper(ABC):

    @abstractmethod
    def get_j_obj(self):
        raise Exception("Not implemented.")

    def __str__(self):
        return self.get_j_obj().toString()


class JavaObjectWrapperWithFunc(JavaObjectWrapper):

    def __init__(self, j_obj):
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def __dir__(self):
        keys = self.get_j_obj().__dir__()
        return keys

    def __getattr__(self, attr_name):
        def wrapped_func(f):
            def inner(*args, **kwargs):
                args = [
                    arg.get_j_obj() if isinstance(arg, JavaObjectWrapper) else arg
                    for arg in args
                ]
                retval = f(*args, **kwargs)
                return j_value_to_py_value(retval)

            return inner

        # assume all access are functions
        attr = self.get_j_obj().__getattr__(attr_name)
        if isinstance(attr, JavaObject):
            return j_value_to_py_value(attr)
        else:
            return wrapped_func(attr)


class AutoTypeConversionMetaClass(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if not attr_name.startswith("__") and attr_name != "get_j_obj" and callable(attr_value):
                attrs[attr_name] = auto_convert_java_type(attr_value)
        return super(AutoTypeConversionMetaClass, mcs).__new__(mcs, name, bases, attrs)


class JavaObjectWrapperWithAutoTypeConversion(JavaObjectWrapper, ABC, metaclass=AutoTypeConversionMetaClass):
    """
    This class provides automatically type conversion of arguments and return values for all instances methods.
    Note that static methods and class methods are not included.
    Use the decorator `auto_convert_value_type` instead.
    """
