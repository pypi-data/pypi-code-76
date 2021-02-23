import sys
try:
    from importlib._bootstrap_external import MAGIC_NUMBER
except ImportError:
    from importlib._bootstrap import MAGIC_NUMBER
import marshal
from types import CodeType,FunctionType
from collections import OrderedDict
from pyobject import desc
import dis, pickle

NoneType=None.__class__
class newNoneType():
    """一种新的None类型。
与Python自带的NoneType类型相比,这种类型什么都能做,可以相加,相减,相乘,相除,被调用,等等,
, 即支持许多"魔法"方法; 但每个方法什么也不做,直接pass。
示例:
>>> none=newNoneType()
>>> none
>>> print(none)
newNoneType
>>> none.write()
>>> none.write=1
>>> none.write
1
>>> none+'1'
'1'
>>> none-1
-1
>>> none>0
False
>>> none>=0
True
>>> none<0
False
>>> none<=0
True
>>> none==None
True"""
    def __add__(self,other):
        return other
    def __bool__(self):
        return False
    def __call__(self,*args,**kwargs):
        return self
    def __eq__(self,other):
        availbles=self,newNoneType, None,NoneType, 0,''
        for availble in availbles:
            if other is availble:return True
        return False
    def __ge__(self,value):
        return value<=0
    def __getattr__(self,name):
        return self
    def __gt__(self,value):
        return value<0
    def __le__(self,value):
        return value>=0
    def __lt__(self,value):
        return value>0
    def __str__(self):
        return self.__class__.__name__
    def __repr__(self):
        return ''
    def __sub__(self,value):
        return -value
    def __neg__(self):
        return self
    def __setattr__(self,name,value):
        self.__dict__[name]=value
        return self

inf=1e315
class Infinity():
    """无穷大。
示例:
>>> inf=Infinity()
>>> inf
Infinity()
>>> print(inf)
∞
>>> print(-inf)
-∞
>>> float(inf)
inf
>>> inf==float(inf)
True
>>> -inf
-Infinity()
>>> inf>1e308
True
>>> inf<1e308
False
>>> inf>=1e308
True
>>> inf<=1e308
False
>>> -inf==-float(inf)
True
>>> -inf>0
False
>>> -inf<0
True
>>> -inf>=0
False
>>> -inf<=0
True
    """
    def __init__(self,neg=False):
        self.neg=neg
    def __eq__(self,value):
        return value is self or value==float(self)
    def __float__(self):
        return -inf if self.neg else inf
    def __ge__(self,value):
        # self>=value
        return not self.neg
    def __gt__(self,value):
        # self>value
        return not self<=value
    def __le__(self,value):
        # self<=value
        return (not self==value) if self.neg else (self==value)
    def __lt__(self,value):
        # self<value
        return self.neg
    def __neg__(self):
        return Infinity(neg=(not self.neg))
    def __str__(self):
        return ('-' if self.neg else '')+'∞'
    def __repr__(self):
        return "%sInfinity()"%('-' if self.neg else '')

##class StrangeList(list,tuple):
##    """一种可变的,奇怪的序列类型,同时继承内置list和tuple类。"""

class ObjDict:
    "对象字典"
    def __init__(self,obj):
        self.obj=obj
    def __getitem__(self,key):
        return getattr(self.obj,key)
    def __setitem__(self,key,value):
        setattr(self.obj,key,value)
    def __delitem__(self,key):
        delattr(self.obj,key)
    def get(self,key,default):
        return getattr(self.obj,key,default)

    def __iter__(self):
        return dir(self.obj).__iter__()
    def keys(self):
        return dir(self.obj)
    def clear(self):
        for key in self.keys():
            try:
                delattr(self.obj,key)
            except Exception as err:
                print(type(err).__name__+":", err,
                      file=sys.stderr)
    def __str__(self):
        return str(dict(self))

    def __copy__(self):
        return ObjDict(self.obj)
    def __deepcopy__(self,*args):
        newobj=deepcopy(self.obj)
        return ObjDict(newobj)
    def __repr__(self):
        try:
            return "ObjDict(%r)"%self.obj
        except AttributeError: # ObjDict对象没有obj属性时
            return object.__repr__(self)
    def todict(self):
        return dict(self)
    @staticmethod
    def dict_to_obj(dict):
        """>>> d=ObjDict(ObjDict(1)).todict()
>>> ObjDict.dict_to_obj(d)
ObjDict(1)
"""
        obj=object.__new__(dict["__class__"])
        obj.__dict__.update(dict)
        return obj
    # for pickle
    def __getstate__(self):
        return self.obj
    def __setstate__(self,arg):
        self.obj=arg


_py38=hasattr(compile('','','exec'), 'co_posonlyargcount')
class Code:
    """
>>> def f():print("Hello")

>>> c=Code.fromfunc(f)
>>> c.co_consts
(None, 'Hello')
>>> c.co_consts=(None, 'Hello World!')
>>> c.exec()
Hello World!
>>>
>>> 
>>> import os,pickle
>>> temp=os.getenv('temp')
>>> with open(os.path.join(temp,"temp.pkl"),'wb') as f:
...     pickle.dump(c,f)
... 
>>> 
>>> f=open(os.path.join(temp,"temp.pkl"),'rb')
>>> pickle.load(f).to_func()()
Hello World!
>>> 
>>> c.to_pycfile(os.path.join(temp,"temppyc.pyc"))
>>> sys.path.append(temp)
>>> import temppyc
Hello World!
"""
# 关于CodeType: 
# 参数
# code(argcount, kwonlyargcount, nlocals, stacksize, flags, codestring,
#    constants, names, varnames, filename, name, firstlineno,
#    lnotab[, freevars[, cellvars]])
# 属性:
#co_argcount
#co_cellvars
#co_code
#co_consts
#co_filename
#co_firstlineno
#co_flags
#co_freevars
#co_kwonlyargcount
#co_lnotab
#co_name
#co_names
#co_nlocals
#co_stacksize
#co_varnames
# 在Python 3.8中, 增加了属性co_posonlyargcount

    # 按顺序
    _default_args=OrderedDict(
         [('co_argcount',0),
          ('co_kwonlyargcount',0),
          ('co_nlocals',0),
          ('co_stacksize',1),
          ('co_flags',67),
          ('co_code',b'd\x00S\x00'),#1   LOAD_CONST    0 (None)
                                    #2   RETURN_VALUE
          ('co_consts',(None,)),
          ('co_names',()),
          ('co_varnames',()),
          ('co_filename',''),
          ('co_name',''),
          ('co_firstlineno',1),
          ('co_lnotab',b''),
          ('co_freevars',()),
          ('co_cellvars',())
          ])
    # 与Python3.8及以上版本兼容
    if _py38:
        _default_args['co_posonlyargcount']=0
        _default_args.move_to_end('co_posonlyargcount', last=False)
        _default_args.move_to_end('co_argcount', last=False)

    _arg_types={key:type(value) for key,value in _default_args.items()}
    def __init__(self,code=None):
        super().__setattr__('_args',self._default_args.copy())
        if code is not None:
            self._code=code
            for key in self._args.keys():
                self._args[key]=getattr(code,key)
        else:
            self._update_code()
    def __getattr__(self,name):
        _args=object.__getattribute__(self,'_args')
        if name in _args:
            return _args[name]
        else:
            # 调用super()耗时较大, 所以改用object
            return object.__getattribute__(self,name)
    def __setattr__(self,name,value):
        if name not in self._args:
            return object.__setattr__(self,name,value)
        if not isinstance(value,self._arg_types[name]):
            raise TypeError(name,value)
        self._args[name]=value
    def _update_code(self):
        self._code=CodeType(*self._args.values())
    def exec(self):
        self._update_code()
        exec(self._code)
    # for pickle
    def __getstate__(self):
        return self._args
    def __setstate__(self,state):
        super().__setattr__('_args',self._default_args.copy())
        self._args.update(state)
        if not _py38 and 'co_posonlyargcount' in state:
            del state['co_posonlyargcount']
        self._update_code()
    def __dir__(self):
        return object.__dir__(c) + list(c._args.keys())
    @classmethod
    def fromfunc(cls,function):
        c=function.__code__
        return cls(c)
    @classmethod
    def fromstring(cls,string,mode='exec',filename=''):
        return cls(compile(string,filename,mode))
    def to_code(self):
        return self._code
    def to_func(self,globals_=None,name=''):
        if globals_ is None:
            # 默认
            import builtins
            globals_=vars(builtins)
        return FunctionType(self._code,globals_,name)
    def to_pycfile(self,filename):
        with open(filename,'wb') as f:
            f.write(MAGIC_NUMBER)
            if sys.winver>='3.7':
                f.write(b'\x00'*12)
            else:
                f.write(b'\x00'*8)
            marshal.dump(self._code,f)
    def pickle(self,filename):
        with open(filename,'wb') as f:
            pickle.dump(self,f)
    def view(self):
        dis.show_code(self._code)
    def show(self,*args,**kw):
        desc(self._code,*args,**kw)
    def dis(self,*args,**kw):
        dis.dis(self._code,*args,**kw)

if __name__=="__main__":
    import doctest
    doctest.testmod()
