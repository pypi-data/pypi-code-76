'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import random as rd

class RandomNumberGenerator:

    #public:

        def __init__ (self, seed=None):
            rd.seed (a=seed, version=2)

        def __call__ (self):
            return rd.random ()

