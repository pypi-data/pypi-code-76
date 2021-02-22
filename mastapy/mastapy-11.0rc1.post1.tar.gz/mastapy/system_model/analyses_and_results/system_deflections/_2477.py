'''_2477.py

StraightBevelDiffGearSystemDeflection
'''


from mastapy.system_model.part_model.gears import _2216, _2220, _2221
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6590, _6596, _6597
from mastapy.system_model.analyses_and_results.power_flows import _3801, _3806, _3807
from mastapy.gears.rating.straight_bevel_diff import _356
from mastapy.system_model.analyses_and_results.system_deflections import _2372
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'StraightBevelDiffGearSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSystemDeflection',)


class StraightBevelDiffGearSystemDeflection(_2372.BevelGearSystemDeflection):
    '''StraightBevelDiffGearSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSystemDeflection.TYPE'):
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

    @property
    def component_load_case(self) -> '_6590.StraightBevelDiffGearLoadCase':
        '''StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6590.StraightBevelDiffGearLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to StraightBevelDiffGearLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3801.StraightBevelDiffGearPowerFlow':
        '''StraightBevelDiffGearPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3801.StraightBevelDiffGearPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelDiffGearPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PowerFlowResults.__class__)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def component_detailed_analysis(self) -> '_356.StraightBevelDiffGearRating':
        '''StraightBevelDiffGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_356.StraightBevelDiffGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
