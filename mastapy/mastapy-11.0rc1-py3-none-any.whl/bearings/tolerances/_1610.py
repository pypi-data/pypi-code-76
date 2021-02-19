'''_1610.py

InnerSupportTolerance
'''


from mastapy.bearings.tolerances import _1624
from mastapy._internal.python_net import python_net_import

_INNER_SUPPORT_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'InnerSupportTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerSupportTolerance',)


class InnerSupportTolerance(_1624.SupportTolerance):
    '''InnerSupportTolerance

    This is a mastapy class.
    '''

    TYPE = _INNER_SUPPORT_TOLERANCE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InnerSupportTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
