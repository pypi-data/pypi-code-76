'''_2259.py

ActiveShaftDesignSelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2262, _2258
from mastapy.system_model.part_model.shaft_model import _2129
from mastapy.shafts import _40
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelectionGroup',)


class ActiveShaftDesignSelectionGroup(_2262.PartDetailConfiguration['_2258.ActiveShaftDesignSelection', '_2129.Shaft', '_40.SimpleShaftDefinition']):
    '''ActiveShaftDesignSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
