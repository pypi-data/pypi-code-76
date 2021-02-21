'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

from toolbox.func_tools import Join, Comp

class AntiVar:

    #public:

        def __init__ (self, join):
            self.X = Comp (mean, join)
            
        def __call__ (self, gen):
            return self.X (gen)

class SubAntiVar (AntiVar):

    #public:

        def __init__ (self, func, trans, X):
            super ().__init__ (Join (Comp (func, X), Comp (func, trans, X)))

#toolkit:

def mean (x, y):
    return 0.5 * (x + y)