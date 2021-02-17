import yaml
import importlib
from enum import Enum
from collections import OrderedDict


class Yac(OrderedDict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get # this returns None if key does not exist, while dict.__getitem__ raises KeyError
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


    @staticmethod
    def load(filepath, safe=True):

        with open(filepath, 'r') as stream:
            try:
                yac = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise

        return yachize(yac, safe=safe)

    def dump(self, filepath=None):

        d = unyachize(self)
        if filepath:
            with open(filepath, 'w') as f:
                yaml.dump(d, stream=f, default_flow_style=None, sort_keys=False)

        return yaml.dump(d, default_flow_style=None, sort_keys=False)


    def add(self, a_dict):
        return self.update(a_dict)

    def set_if_not_none(self, key, value):
        if value is not None:
            dict.__setitem__(self, key, value)


    # for pickle/unpickle
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        return self.__dict__.update(d)


    # print
    def __repr__(self):
        return self.dump()


def yachize(o, safe=True):
    """
    Transform all dictionaries into Yac objects.

    Args:
        o:
        safe: bool, whether to allow class instantiation.

    Returns:
        Yac: a yac object.

    """
    if isinstance(o, dict):

        # parse all elements in the dict, and yachize them.
        for k, o2 in o.items():
            o[k] = yachize(o2, safe=safe)
        o = Yac(o)

        # for parameters enum, instantiate them
        if o.enum:

            module_name, class_name = o.enum.rsplit('.', 1)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)

            if not issubclass(class_, Enum):
                raise ValueError('Class %s is not an Enum.' % class_)

            if not isinstance(o.name, (int, str)):
                raise ValueError('An enum parameter shall be an int or a string (found %s).' % type(o.name))

            for e in list(class_):
                if e.name == o.name:
                    return e

            raise ValueError('Enum %s has no member %s.' % (class_, o.name))

        # for parameters objects, instantiate them
        if 'class' in o:

            if safe:
                raise ValueError('Class instantiation is not allowed in safe mode.')

            module_name, class_name = o['class'].rsplit('.', 1)
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)

            if o.args and o.kwargs:
                return class_(*o.args, **o.wargs),
            elif o.args:
                return class_(*o.args)
            elif o.kwargs:
                return class_(**o.kwargs)
            else:
                return class_()

    return o


def unyachize(o, safe=True):

    if isinstance(o, Yac):

        # parse all elements in the dict, and un-yachize them.
        for k, o2 in o.items():
            o[k] = unyachize(o2, safe=safe)
        o = dict(o)

    return o



# for testing
class StuffEnum(Enum):

    A = 0
    B = 1


class StuffClassWithoutArgs:
    pass

class StuffClassWithArgs:

    def __init__(self, a, b):
        self.a = a
        self.b = b

class StuffClassWithKwargs:

    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b