'''_6590.py

StraightBevelDiffGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2216, _2220, _2221
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6459
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearLoadCase',)


class StraightBevelDiffGearLoadCase(_6459.BevelGearLoadCase):
    '''StraightBevelDiffGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2216.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.StraightBevelDiffGear.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
