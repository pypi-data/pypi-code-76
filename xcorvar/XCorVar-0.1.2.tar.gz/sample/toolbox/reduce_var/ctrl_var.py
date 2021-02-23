'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

from toolbox.compose import CompCore
from toolbox.map import Map

class CtrlVar:

    #public:

        def __init__ (self, join, mean):
            self.mean = mean
            self.X = CompCore (minus, join)
            
        def __call__ (self, *args):
            return self.mean + self.X (*args)

class SubCtrlVar (CtrlVar):

    #public:

        def __init__ (self, join, mean, *func):
            super ().__init__ (CompCore (Map (*func), join), mean)

#toolkit:

def minus (x, y):
    return x - y