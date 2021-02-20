from typing import Any, Iterable
import sys, winsound, os, time, inspect

import pyperclip

from .types import SineWave, generator, regurge, function


separator = " ".join(70*'-')
spaceprint = lambda x: print(x, "\n{}".format(separator))

main = '__name__ == "__main__"'
    

def tipo(inpt:Any=type(lambda:0), keep_module:bool=False) -> str:
    """
    Return the name of an object's type
    Dependencies: None
    In: object
    Out: str
    """
    if keep_module:
        return str(type(inpt)).split("'")[1]
    return str(type(inpt)).split("'")[1].split('.')[-1]


def beeper(inpt:int) -> SineWave:
    """Produces a series of beeps of increasing frequency
    Dependencies: Beep(a function from the winsound module)
    In: (number of beeps desired)
    Out: Series of beeps of increasing frequency"""
    for i in range(inpt):
        frequency = 65*2**(i)
        duration = 500
        winsound.Beep(frequency, duration)


def syspath():
    """Displays the path
    Dependencies: sys, sys.path
    In: (N/A)
    Out: string with formatted list"""
    return f"current:\n{sys.path}"


def padd(inpt):
    """Adds a string to the path
    Dependencies: sys, sys.path
    In: (desired address)
    Out: N/A"""
    sys.path.append(inpt)
    return("done :)\n{0}".format(sys.path))


def test(func:type(lambda:1), unsortedlist:tuple) -> float:
    """Test measures the amount of time needed to run a function on a given Input
    dependencies: time.clock() (perf_counter due to deprecation )
    In: function, input
    Out: Difference in time between the call and return of the function
    lifted from davejm's sorting module on github"""
    #Set copy equal to a new copy (different mem. location) of unsortedList to preserve current list
    #using the [:] split command which returns a copy of the whole list but as a new object
    from time import perf_counter as clock
    copy = unsortedlist[:]
    start = clock() #Set start time. TODO - May convert to using timit module.
    func(copy) #Run bubble or shuttle sort with copy of unsorted list as argument
    duration  = clock() - start #Work out how long the execution of algorithm took and set to duration
    return duration


def modir(module:type(os), copy:bool=True) -> str:
    """
    Returns the full path of the directory inwhich a given module is located
    Dependencies: os, pyperclip
    In: module object, boolean (t-copy,f-not copy)
    Out: String or Boolean
    
    Example:
        import matplotlib.pyplot as plt
        print(modir(plt),modir(plt,False),sep='\n')
    
        Prints
            None
            E:\Languages\Python37-64\Lib\site-packages\matplotlib
    """
    pth = os.sep.join(module.__file__.split(os.sep)[:-1])
    return pth if not copy else pyperclip.copy(pth)


def printer(iterable:Iterable, indent:int=0) -> None:
    """
    Prints each element of an iterable on a new line, features an optional indent argument
    """
    assert isinstance(indent, int), "Indentation level must be a positive integer"
    for i in iterable:
        print(indent*"\t"+f"{i}")


def tryimport(name:str, pack:str=None, substitute:bool=False, subpack:str=None, silent:bool=False) -> Any:
    """
    Import a package, or something from within it, failing its installation import an optional substitute.
    Example:
    trasher = tryimport('send2trash',pack='send2trash',substitute='remove',subpack='os')
        would try to 'import send2trash from send2trash' and be ready to 'import remove from os' if send2trash is not installed, and assign the result to the 'trasher' variable
    Dependencies: None
    Arguments: name,pack=None,substitute=False,subpack=None; all strings
    Outputs: module/object
    """
    try:
        message = f'from {pack} import {name}' if pack else f'import {name}'
        exec(message)
        return eval(name)
    except ModuleNotFoundError:
        if substitute:
            if subpack:
                return tryimport(substitute, subpack)
            else:
                return tryimport(substitute)
        elif subpack:
            return tryimport(subpack)
        else: 
            if not silent: 
                raise ModuleNotFoundError


def aspectRatio(x:int, y:int, w:int=None, h:int=None) -> float:
    """
    Compute aspect ratio and scale to desired size
    aspectRatio(a, b) ~> a/b
    aspectRatio(a, b, w=c) ~> (c,round(c*(b/a)))
    aspectRatio(a, b, h=c) ~> (round(c*(a/b)), c)
    aspectRatio(a, b, w=c, h=d) ~> a/b==c/d
    Dependencies: None
    In: x, y, w, h: numbers
    Outs: int or tuple
    """
    return w/h==x/y if w and h else (w, (w*(y/x))) if w else ((h*(x/y)), h) if h else x/y


def show(iterable:Iterable[Any], indentation:int=0, enum:bool=False, first:int=1, indentor:str='\t', tail=True, head=False, file=sys.stdout, sep:str='') -> None: 
    """
    Print each element of an array.
    >>> show(zip('abc','123'))
    ('a', '1')
    ('b', '2')
    ('c', '3')


    >>>
    """
    # consumable = regurge(iterable)
    consumable = iter(regurge(iterable))
    if (wasstr:=isinstance(file, str)):
        file = open(file)
    print('\n', file=file) if head else None
    for i, j in enumerate(consumable, first):
        print(
            (
                f"{indentation*indentor}{j}",
                f"{indentation*indentor}{i}\t{j}"
            )[enum],
            sep=sep,
            file=file
        )
        # if sep:
            # print(sep)
    print('\n', file=file) if tail else None
    if wasstr:
        file.close()


def pop(arg:Any=None, file:bool=True, silent:bool=False) -> str:
    """
    Open the folder containing a given module, or object's module, or the content at the path of the given string
    Opens current working directory if no object is given
    Open the module's file if it is given
    If a path is given, it will be opened.
    Return the path which is opened
    
    This will raise an attribute error whenever there is no file to which the object/module is imputed
    """
    module = type(os)
    if arg:
        if isinstance(arg, str):
            path = arg
        elif isinstance(arg, module):
            path = arg.__file__
        else:
            mstr = arg.__module__
            if (top:=mstr.split('.')[0]) in globals().keys():
                m = eval(mstr)
            else:
                t = exec(f'import {top}')
                m = eval(mstr)
            path = m.__file__
        if not file:
            path = os.path.dirname(path)
    else:
        path = os.getcwd()
    if not silent:
        os.startfile(path)
    return path


def hasDocs(module:type(os), copy:bool=True) -> bool:
    """
    Returns directory of a given module's documentation... if it can be found by lesser mortals such as I
    Dependencies: os, pyperclip
    In: module object, boolean (t-copy,f-not copy)
    Out: String or Boolean
    """
    base = modir(module, False)
    directory = os.path.join(base, 'docs') if os.path.exists(os.path.join(base, 'docs')) else os.path.join(base, 'doc')
    d = False if not os.path.exists(directory) else directory
    return d if not copy else pyperclip.copy(d)


def getsource(obj:Any, *args, copy:bool=False, **kwargs) -> str:
    """
    Wrapper on inspect.getsource which uses .show to present the text more readably and pyperclip.copy to copy said text to the clipboard.
    """
    text = inspect.getsource(obj).splitlines()
    if copy:
        pyperclip.copy('\n'.join(text))
        return
    show(text, *args, **kwargs)



if __name__=='__main__':
    pass