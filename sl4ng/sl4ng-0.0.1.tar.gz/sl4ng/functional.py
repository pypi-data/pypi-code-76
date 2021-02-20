from typing import Iterable, Any, Callable
import time

from .types import function, generator, regurge



def repeat(func:function, inpt:Any, times:int=2, **kwargs) -> type:
    """
    Get the output of recursive calls of a function some number of times
    Dependencies: None
    In: function,input,times[=1]
    Out: Function call
    
    repeat(lambda x: x+1,0)
        2
    repeat(lambda x: x+1,0,1)
        1
    """
    for i in range(times):
        inpt = func(inpt, **kwargs)
    return inpt
recursor = repeat


def eq(*args:Iterable[Any]) -> bool:
    """
    Check if arguments are equal
    Will always return True if the only argument given is not an iterable
    """
    if len(args) == 1:
        if hasattr(arg:=args[0], '__iter__'):
            return eq(*arg)
        return True
    
    args = iter(args)
    arg0 = next(args)
    
    for i in args:
        if i != arg0:
            return False
    return True


def clock(func:function, value:bool=False, name:bool=False) -> function:
    """
    A decorator for benchmarking functions
    
    :name:
        option to print the name of the function with the time taken to call it
    :value:
        return the value of the function instead of the period
    
    taken from
    Mari Wahl, mari.wahl9@gmail.com
    University of New York at Stony Brook
    """
    def wrapper(*args:Any, **kwargs:Any) -> Any:
        t = time.perf_counter()
        res = func(*args, **kwargs)
        delta = time.perf_counter()-t
        if name:
            print(f"{func.__name__}\n\t{delta}")
        else:
            print(f"d={delta}")
        return res if value else delta
    return wrapper
benchmark = clock


def imap(argument:Any, *functions:Callable) -> generator:
    """
    Converse of a map. Yield calls of the functions with the object as an argument
    Generator safe
    """
    iterates = hasattr(object, '__iter__')
    for func in functions:
        yield func((argument, regurge(argument))[iterates])


def rmap(argument:Any, *functions:Callable) -> Any:
    """
    Recursively call functions on an argument. Return the result of the last call
    Generator safe
    """
    functions = iter(functions)
    iterates = hasattr(object, '__iter__')
    result = next(functions)((argument, regurge(argument))[iterates])
    for func in functions:
        result = func((result, regurge(result))[iterates])
    return result
        


