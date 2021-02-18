#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from collections import OrderedDict as OD
from mendeleev import get_all_elements

elements = {x.symbol: x for x in get_all_elements()}


def get_element_dict(propname='mass_number'):
    """ Obtain dictionary of elements ordered by a property.
    """
    
    prop_dict = {k:getattr(elements[k], propname) for k in elements.keys()}

    elems = list(elements.keys())
    props = list(prop_dict.values())

    # Sort the element list by the masses
    srtseq = np.argsort(props)
    elems = np.array(elems)[srtseq]
    props = np.array(props)[srtseq]

    prop_odict = OD({k:v for k, v in zip(elems, props)})
    
    return prop_odict