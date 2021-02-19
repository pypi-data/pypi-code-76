'''_1553.py

OuterSupportTolerance
'''


from mastapy.bearings.tolerances import _1560
from mastapy._internal.python_net import python_net_import

_OUTER_SUPPORT_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'OuterSupportTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterSupportTolerance',)


class OuterSupportTolerance(_1560.SupportTolerance):
    '''OuterSupportTolerance

    This is a mastapy class.
    '''

    TYPE = _OUTER_SUPPORT_TOLERANCE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OuterSupportTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
