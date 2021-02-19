'''_215.py

CompositeFatigueSafetyFactorItem
'''


from mastapy.materials import _218
from mastapy._internal.python_net import python_net_import

_COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM = python_net_import('SMT.MastaAPI.Materials', 'CompositeFatigueSafetyFactorItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CompositeFatigueSafetyFactorItem',)


class CompositeFatigueSafetyFactorItem(_218.FatigueSafetyFactorItem):
    '''CompositeFatigueSafetyFactorItem

    This is a mastapy class.
    '''

    TYPE = _COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompositeFatigueSafetyFactorItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
