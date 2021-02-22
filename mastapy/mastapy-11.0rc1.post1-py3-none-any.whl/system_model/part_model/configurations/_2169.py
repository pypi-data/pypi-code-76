'''_2169.py

ActiveShaftDesignSelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2172, _2168
from mastapy.system_model.part_model.shaft_model import _2044
from mastapy.shafts import _40
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelectionGroup',)


class ActiveShaftDesignSelectionGroup(_2172.PartDetailConfiguration['_2168.ActiveShaftDesignSelection', '_2044.Shaft', '_40.SimpleShaftDefinition']):
    '''ActiveShaftDesignSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
