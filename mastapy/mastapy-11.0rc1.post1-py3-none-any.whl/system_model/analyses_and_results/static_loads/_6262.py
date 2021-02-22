'''_6262.py

StraightBevelSunGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2148
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6255
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelSunGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearLoadCase',)


class StraightBevelSunGearLoadCase(_6255.StraightBevelDiffGearLoadCase):
    '''StraightBevelSunGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2148.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2148.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
