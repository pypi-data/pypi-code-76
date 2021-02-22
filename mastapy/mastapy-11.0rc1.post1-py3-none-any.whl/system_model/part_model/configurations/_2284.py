'''_2284.py

ActiveShaftDesignSelection
'''


from mastapy.system_model.part_model.configurations import _2289
from mastapy.system_model.part_model.shaft_model import _2154
from mastapy.shafts import _40
from mastapy._internal.python_net import python_net_import

_ACTIVE_SHAFT_DESIGN_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveShaftDesignSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveShaftDesignSelection',)


class ActiveShaftDesignSelection(_2289.PartDetailSelection['_2154.Shaft', '_40.SimpleShaftDefinition']):
    '''ActiveShaftDesignSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_SHAFT_DESIGN_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveShaftDesignSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
