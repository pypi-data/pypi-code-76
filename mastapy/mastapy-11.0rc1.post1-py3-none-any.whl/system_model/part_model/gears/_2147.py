'''_2147.py

StraightBevelPlanetGear
'''


from mastapy.gears import _139
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2143
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGear',)


class StraightBevelPlanetGear(_2143.StraightBevelDiffGear):
    '''StraightBevelPlanetGear

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetary_details(self) -> '_139.PlanetaryDetail':
        '''PlanetaryDetail: 'PlanetaryDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_139.PlanetaryDetail)(self.wrapped.PlanetaryDetails) if self.wrapped.PlanetaryDetails else None
