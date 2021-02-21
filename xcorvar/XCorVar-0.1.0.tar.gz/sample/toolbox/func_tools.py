'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

class Map:

    #public:

        def __init__ (self, *func):
            self.func = func
        
        def __call__ (self, *X):
            return [fun (x) for fun, x in zip (self.func, X)]

class Join:

    #public:

        def __init__ (self, *func):
            self.func = func
        
        def __call__ (self, *X):
            return [fun (*X) for fun in self.func]

class Comp:

    #public:

        def __init__ (self, *func):
            self.func = func

        def __call__ (self, *X):
            try: return CompCore (self.func [0], Comp (*self.func [1:])) (*X)
            except IndexError: return self.func [0] (*X) 

class CompCore:

    #public:

        def __init__ (self, func1, func2):
            self.func1 = func1
            self.func2 = func2
        
        def __call__ (self, *X):
            try: return self.func1 (*self.func2 (*X))
            except TypeError: return self.func1 (self.func2 (*X))