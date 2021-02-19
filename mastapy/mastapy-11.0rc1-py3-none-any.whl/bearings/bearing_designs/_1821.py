'''_1821.py

DetailedBearing
'''


from mastapy.bearings.bearing_designs import _1824
from mastapy._internal.python_net import python_net_import

_DETAILED_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns', 'DetailedBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DetailedBearing',)


class DetailedBearing(_1824.NonLinearBearing):
    '''DetailedBearing

    This is a mastapy class.
    '''

    TYPE = _DETAILED_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DetailedBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
