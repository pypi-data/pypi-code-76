import os
# os.environ["NUMPY_EXPERIMENTAL_ARRAY_FUNCTION"] = "1"

import numpy as np

HANDLED_FUNCTIONS = {}

class MyArray():
    def __init__(self, val, name=''):
        self.val = np.asarray(val).tolist()
        self.name = name

    def __repr__(self):
        return str(self.val)
    
    def __array__(self, *args, **kwargs):
        print('\t__array__ ({})'.format(self.name))
        return np.asarray(self.val)

    def __array_finalize__(self, obj):
        print('\t__array_finalize__ ({})'.format(self.name))
        print('\tobj: {}'.format(str(obj)))
        return

    def __array_prepare__(self, array, context=None):
        print('\t__array_prepare__ ({})'.format(self.name))
        print('\tarray: {}'.format(str(array)))
        return np.asarray(self.val)

    def __array_wrap__(self, array, context=None):
        print('\t__array_wrap__ ({})'.format(self.name))
        print('\tarray: {}'.format(str(array)))
        return self.__class__(array)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        print('\t__array_ufunc__ ({})'.format(self.name))
        print('\tufunc: {}'.format(str(ufunc)))
        print('\tmethod: {}'.format(str(method)))
        print('\tinputs: {}'.format(str(inputs)))

        if ufunc in HANDLED_FUNCTIONS:
            return HANDLED_FUNCTIONS[ufunc](*inputs, **kwargs)

        if method == '__call__':
            inputs = [np.asarray(input) if isinstance(input, self.__class__) else input for input in inputs]
            return self.__class__(ufunc(*inputs, **kwargs))
        else:
            print('\t>>> NotImplemented')
            if "NUMPY_EXPERIMENTAL_ARRAY_FUNCTION" in os.environ.keys():
                print('environment variable NUMPY_EXPERIMENTAL_ARRAY_FUNCTION = {}'.format(os.environ["NUMPY_EXPERIMENTAL_ARRAY_FUNCTION"]))
            else:
                print('environment variable NUMPY_EXPERIMENTAL_ARRAY_FUNCTION not defined')
            # return NotImplemented

            inputs = [np.asarray(input) if isinstance(input, self.__class__) else input for input in inputs]
            return self.__class__(getattr(ufunc, method)(*inputs, **kwargs))

    def __array_function__(self, func, types, args, kwargs):
        print('\t__array_function__ ({})'.format(self.name))
        print('\tfunc: {}'.format(str(func)))
        print('\ttypes: {}'.format(str(types)))
        print('\targs: {}'.format(str(args)))

        if func not in HANDLED_FUNCTIONS:
            print('\t>>> NotImplemented')
            # return NotImplemented

            new_args = []
            for i, arg in enumerate(args):
                if isinstance(arg, self.__class__):
                    new_args.append(np.asarray(arg))
                else:
                    new_args.append(arg)
            return self.__class__(func(*new_args, **kwargs))

        # Note: this allows subclasses that don't override
        # __array_function__ to handle MyArray objects
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented

        return self.__class__(HANDLED_FUNCTIONS[func](*args, **kwargs))

    def __add__(self, x):
        print('\t__add__ ({})'.format(self.name))
        print('\tparam: {}'.format(str(x)))
        return self.__class__(np.asarray(self.val) + np.asarray(x))

    def __mul__(self, x):
        print('\t__mul__ ({})'.format(self.name))
        print('\tparam: {}'.format(str(x)))
        return self.__class__(np.asarray(self.val) * np.asarray(x))       


def implements(np_function):
   "Register an __array_function__ implementation for DiagonalArray objects."
   def decorator(func):
       HANDLED_FUNCTIONS[np_function] = func
       return func
   return decorator

@implements(np.sum)
def my_sum(x):
    print('\t>>> my_sum')
    print('\tparam: {}'.format(str(x)))
    return MyArray(np.sum(np.asarray(x)))

@implements(np.multiply)
def my_mul(x, y):
    print('\t>>> my_mul')
    print('\tparams: {}, {}'.format(str(x), str(y)))
    return MyArray(np.multiply(np.asarray(x), np.asarray(y)))    


if __name__ == "__main__":
    v = [1, 2, 3]
    w = [-1, 0, 1]

    vnp = np.asarray(v)
    wnp = np.asarray(w)

    x = MyArray(v, name='x')
    print(x)
    y = MyArray(w, name='y')
    print(y)

    print('\nx + 2')
    z = x + 2
    print(z, type(z)) 

    print('\nnp.add(x, 2)')
    z = np.add(x, 2)
    print(z, type(z))

    print('\nx + y')
    z = x + y
    print(z, type(z)) 

    print('\nnp.add(x, y)')
    z = np.add(x, y)
    print(z, type(z))

    print('\nnp.sum(x)')
    z = np.sum(x)
    print(z, type(z))

    print('\nnp.dot(x, y)')
    z = np.dot(x, y)
    print(z, type(z))

    print('\nnp.dot(x, wnp)')
    z = np.dot(x, wnp)
    print(z, type(z))

    print('\nnp.dot(vnp, y)')
    z = np.dot(vnp, y)
    print(z, type(z))

    print('\nx * 2')
    z = x * 2
    print(z, type(z)) 

    print('\nnp.multiply(x, 2)')
    z = np.multiply(x, 2)
    print(z, type(z))

    print('\nx * y')
    z = x * y
    print(z, type(z)) 

    print('\nnp.multiply(x, y)')
    z = np.multiply(x, y)
    print(z, type(z))

    print('\nnp.add(x, a)')
    a = range(3)
    z = np.add(x, a)
    print(z, type(z))