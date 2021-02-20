
import asyncio
import torch.nn as nn
import functools
import inspect

from ..Utils.Log import Logger

def parameter_collector(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            param_dict = dict()
            for idx, varname in enumerate(func.__code__.co_varnames):
                if varname == 'self' and idx == 0:
                    Logger.get_logger().warning('Encountering self arg, which may not be a necessary argument.')
                else:
                    param_dict[varname] = None
            print(param_dict)

            print(args, kwargs)
            # print(func.__code__.co_varnames)

            # print(inspect.signature(func).parameters)
            for param in inspect.signature(func).parameters.items():
                # print(param[0], param[1].default, param[1].annotation)
                if param[1].default != inspect._empty:
                    param_dict[param[0]] = param[1].default
            
            return func(self, *args, **kwargs)
        except BaseException as ex:
            raise Exception(ex.message)
    return wrapper

class TorchModel(object):

    def __init__(self, model):
        if model.__class__.__bases__[0] != nn.Module:
            raise TypeError("TorchModel can only be initialized by a torch.nn.Module instance.")
        self.model = model
        Logger.get_logger().info("Initialized torch Model.")
        self.watcher = None

    def get_model_parameters(self):
        return self.model.__str__()

    @staticmethod
    def parse_model_params_helper(lines):
        pass

    def parse_model_parameters(self):
        model_structure = [(line.__len__() - line.lstrip(' ').__len__(), line.lstrip(' ').rstrip(' '))for line in self.model.__str__().split('\n')]
        return model_structure

    def update_parameter(self):
        if self.watcher is None:
            # TODO: Add warning
            return False
        else:
            self.watcher.update_model(self)

@parameter_collector
def test_func(a, b, c=8):
    a = 5

if __name__ == '__main__':
    test_func(1, 2)
