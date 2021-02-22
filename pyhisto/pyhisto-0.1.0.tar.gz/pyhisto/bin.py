#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Feb 10 16:09:24 CET 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file:  bin.py -*-

'''
 Module for 1-dimension bins

 A bin is used by Histograms.
 It is defined by low and up edges, a center and a count.
'''
from typing import Union, Optional

Number = Union[int, float]


class Bin:
    '''This object represent a one dimensionnal bin

    It can be represented as a string, or used as a number (equal to count).
    '''

    def __init__(self,
                 lowedge: Number = -0.5,
                 width: Number = 1,
                 count: Number = 0,
                 upedge: Optional[Union[Number, None]] = None,
                 fromstring: Optional[Union[str, None]] = None,
                 fromdict: Optional[Union[dict, None]] = None):
        ''' Create new bin

        Can be used to import from string or define a new bin:

        - To import from a string (f.ex. provided by Bin.str), use
        ``Bin(fromstring=z)```

        - Import from a dict (as after repr()): Bin(fromdict=d)

        - To define a new bin use the other key words.
        count: int, float -- The number of count (default 0)
        lowedge: float -- The lower limit of the bin (default -0.5)
        width: float -- the bin width (default 1)
        upedge: float -- the upper limit of the bin (default lowedge+width)

        The prefered way to create a bin is
        >>> Bin(count, lowedge, width)
        '''
        if fromstring:
            inputs = fromstring.split()
            if len(inputs) == 3:
                self.lowedge, width, self.count = map(float, inputs)
            elif len(inputs) == 2:
                self.lowedge = float(inputs[0]) - 0.5
                width = 1.0
                self.count = float(inputs[1])
        elif fromdict:
            self.lowedge = fromdict['from']
            self.upedge = fromdict['to']
            self.count = fromdict['count']
        else:
            self.count = count
            self.lowedge = lowedge
            self.upedge = upedge
        # end if string
        if upedge is None:
            self.upedge = self.lowedge + width
        if self.upedge < self.lowedge:
            self.lowedge, self.upedge = min(self.upedge, self.lowedge), max(self.upedge, self.lowedge)
    # end of init

    def __index__(self):
        ''' return a 'unique' indeitifer for the bin in the histogram '''
        return int("{0}{1}{2}".format(self.lowedge, self.count, self.upedge))

    def width(self):
        ''' Returns the width of the bin'''
        return self.upedge - self.lowedge

    def center(self):
        '''Returhs bin center (i.e. 0.5*(up+low))'''
        return 0.50 * (self.upedge + self.lowedge)

    def dict(self):
        ''' Returns the bin as a dictionnary '''
        return {'from': self.lowedge,
                'to': self.upedge,
                'count': self.count}

    def __repr__(self):
        return "{{'from':{0.lowedge}, 'to':{0.upedge}, 'count':{0.count}}}".format(self)

    def __str__(self):
        ''' Return as a string in a format that can be used to
        create a new bin with bin(string=)'''
        return "{0} {1} {2} ".format(self.lowedge,
                                     self.width(),
                                     self.count)

    # Type casting
    def __int__(self):
        ''' Returns count as an integer '''
        return int(self.count)

    def __float__(self):
        ''' Returns count as a float '''
        return float(self.count)

    # Addition
    def fill(self, w=1):
        ''' adds `w` to the bin count '''
        self.count += w

    def __add__(self, o):
        ''' Add (an number) to count '''
        return Bin(count=self.count + float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __radd__(self, o):
        ''' This is so that a sum(list-of-Bin) computes the sum of bin counts '''
        return self.count + float(o)

    def __iadd__(self, o):
        ''' Increment bin count '''
        self.count += float(o)
        return self

    # Substration
    def __sub__(self, o):
        ''' sub (an number) to count '''
        return Bin(count=self.count - float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __rsub__(self, o):
        '''  '''
        return Bin(count=self.count - float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __isub__(self, o):
        ''' Increment bin count '''
        self.count -= float(o)
        return self

    # Multiply
    def __mul__(self, o):
        ''' Multiply by a number '''
        return Bin(count=self.count * float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __rmul__(self, o):
        '''  '''
        return Bin(count=self.count * float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __imul__(self, o):
        ''' self multiplication '''
        self.count *= float(o)
        return self

    # Divide
    def __div__(self, o):
        ''' Multiply by a number '''
        return Bin(count=self.count / float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __rdiv__(self, o):
        '''  '''
        return Bin(count=self.count / float(o),
                   lowedge=self.lowedge,
                   upedge=self.upedge)

    def __idiv__(self, o):
        ''' self multiplication '''
        self.count /= float(o)

    # Comparison operator: we compare the counts and not the limits
    def __lt__(self, other):
        return self.count < float(other)

    def __le__(self, other):
        return self.count <= float(other)

    def __eq__(self, other):
        return self.count == float(other)

    def __ne__(self, other):
        return self.count != float(other)

    def __gt__(self, other):
        return self.count > float(other)

    def __ge__(self, other):
        return self.count >= float(other)

    def __and__(self, o):
        '''Merge the two bins (no proximity check)'''
        return Bin(count=self.count + o.count,
                   lowedge=min(self.lowedge, o.lowedge),
                   upedge=max(self.upedge, o.upedge))

    def __contains__(self, v):
        ''' Return true if v is inside Bin limits '''
        return v >= self.lowedge and v < self.upedge

    # other functions to 'sort' by bin bounadries
    def overlaps(self, other):
        ''' Determine if the bin 'other' overlaps with self's boundaries '''
        return not (other.lowedge > self.upedge
                    or other.upedge < self.lowedge)

    def higher(self, other):
        ''' determine if other bin is higher in x than self '''
        return other.lowedge >= self.upedge

    def lower(self, other):
        ''' determine if other bin is lower in x than self '''
        return other.upedge < self.lowedge

    def xy(self, x_pos='low'):
        ''' return a tuple of (x, count)

        x_pos: str -- Determine the position to return for x: low, up or center (default: low)
        '''
        y = self.count
        x = self.lowedge
        if x_pos == 'up':
            x = self.upedge
        elif x_pos == 'center':
            x = self.center()
        return (x, y)
