import threading
import sys
import functools
from inspect import isfunction
from copy import deepcopy


class ClassHolder(object):
    _instance_lock = threading.Lock()
    __class_dict = dict()
    __func_to_class = dict()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(ClassHolder, "_instance"):
            with ClassHolder._instance_lock:
                if not hasattr(ClassHolder, "_instance"):
                    ClassHolder._instance = object.__new__(cls)
        return ClassHolder._instance

    def get_class_dict(self):
        return deepcopy(self.__class_dict)

    def put(self, obj, special_key='__default'):
        # class_module = obj.__class__.__module__
        # class_name = obj.__class__.__name__
        # obj_class = getattr(sys.modules[class_module], class_name)
        with ClassHolder._instance_lock:
            obj._fixed = True
            self.__class_dict[obj.__class__] = {"obj": obj, "name": special_key}

    def get(self, clazz, special_key='__default', is_singleton=True):
        current_result = []
        if isfunction(clazz):
            clazz = self.get_fix(clazz)
        for one_class, value in self.__class_dict.items():
            if (one_class == clazz or issubclass(one_class, clazz)) and value['name'] == special_key:
                if current_result:
                    raise Exception("class {} conflict with {}".format(current_result[0][0], one_class))
                current_result.append((one_class, value))
        if not current_result:
            raise Exception("none of {} can be found".format(clazz))

        exist = current_result[0][1]['obj']
        if is_singleton:
            return exist
        return deepcopy(exist)

    def fix(self, func, clazz):
        self.__func_to_class[func] = clazz

    def get_fix(self, func):
        return self.__func_to_class.get(func)


def class_getter(name=None):
    def wrapper(property_get):
        def get(obj):
            if getattr(obj, "_fixed",False):
                return ClassHolder().get(name)
            return name()
        return get
    return wrapper



def class_register(name="__default"):
    """
    正在尝试注入，beta
    :param name:
    :return:
    """
    def wrapper(func):
        # @functools.wraps(func)
        # def request(*args, **kwargs):
        #     filled_obj = func(*args, **kwargs)
        #     ClassHolder().put(filled_obj, special_key=name)
        #     # ClassHolder().put(args[0],special_key=name)
        #     return filled_obj
        #
        # ClassHolder().fix(request, func)
        # return request

        # 创建对象
        ClassHolder().put(func(), special_key=name)
        return func

    return wrapper


