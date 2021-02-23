def iterop(*instances):
    class it:
        def __getattribute__(self, name:str):
            attributes = []

            for instance in instances:
                attributes.append(getattr(instance, name))

            return iterop(*attributes)

        def __call__(self, *args, **kwargs):
            results = []

            for instance in instances:
                returned = None
                raised = None

                try:
                    returned = instance(*args, **kwargs)
                except Exception as e:
                    raised = e
                
                results.append((returned, raised))
            
            return results
    
    return it()

def chainop(instance):
    class ch:
        def __getattribute__(self, name:str):
            return chainop(getattr(instance, name))
        
        def __call__(self, *args, **kwargs):
            instance(*args, **kwargs) # Send the returned data somewhere?
            return self
    
    return ch()

def iterchain(*instances):
    return chainop(iterop(*instances))

from typing import Callable
from time import time_ns
def stopwatch(function:Callable, *args, **kwargs):
    returned:object = None
    raised:object = None
    duration:int # in nanoseconds

    begin = time_ns()

    try:
        returned = function(*args, **kwargs)
    except Exception as e:
        raised = e
    
    end = time_ns()

    duration = end - begin

    return duration, returned, raised

def lambdo(*functions:Callable):
    functions:list = list(functions)
    if len(functions) == 0:
        return

    execute = []

    def execute_functions():
        def e(function, args, kwargs):
            returned = None
            raised = None

            try:
                returned = function(*args, **kwargs)
            except Exception as e:
                raised = e
            
            return (returned, raised)

        if len(execute) == 1:
            return e(execute[0][0], execute[0][1], execute[0][2])

        data = list()

        for function, args, kwargs in execute:
            data.append(e(function, args, kwargs))
        
        return tuple(data)

    def collect_functions(*args, **kwargs):
        execute.append((functions.pop(0), args, kwargs))
        return collect_functions if len(functions) else execute_functions
    
    return collect_functions

def hint(*objects):
    return objects