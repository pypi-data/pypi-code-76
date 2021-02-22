'''_1328.py

RollingBearingOrder
'''


from mastapy.utility.modal_analysis.gears import _1325
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_ORDER = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'RollingBearingOrder')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingOrder',)


class RollingBearingOrder(_1325.OrderForTE):
    '''RollingBearingOrder

    This is a mastapy class.
    '''

    TYPE = _ROLLING_BEARING_ORDER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingBearingOrder.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
