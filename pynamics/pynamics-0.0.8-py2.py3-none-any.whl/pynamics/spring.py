# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes
Email: danaukes<at>gmail.com
Please see LICENSE for full license.
"""

class Spring(object):
    def __init__(self,k,s,*forces):
        self.k = k
        self.s = s
        self.forces = forces
        