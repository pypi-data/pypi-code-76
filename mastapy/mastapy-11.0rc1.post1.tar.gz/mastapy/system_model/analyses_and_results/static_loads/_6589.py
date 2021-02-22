'''_6589.py

StaticLoadCase
'''


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears import _301
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6905
from mastapy.system_model.analyses_and_results import _2352
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5673
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6703
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.load_case_groups import _5313, _5314, _5315
from mastapy.system_model.analyses_and_results.static_loads import _6437
from mastapy._internal.python_net import python_net_import

_STATIC_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StaticLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticLoadCase',)


class StaticLoadCase(_6437.LoadCase):
    '''StaticLoadCase

    This is a mastapy class.
    '''

    TYPE = _STATIC_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StaticLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_state(self) -> 'str':
        '''str: 'DesignState' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DesignState

    @property
    def number_of_stop_start_cycles(self) -> 'int':
        '''int: 'NumberOfStopStartCycles' is the original name of this property.'''

        return self.wrapped.NumberOfStopStartCycles

    @number_of_stop_start_cycles.setter
    def number_of_stop_start_cycles(self, value: 'int'):
        self.wrapped.NumberOfStopStartCycles = int(value) if value else 0

    @property
    def is_stop_start_load_case(self) -> 'bool':
        '''bool: 'IsStopStartLoadCase' is the original name of this property.'''

        return self.wrapped.IsStopStartLoadCase

    @is_stop_start_load_case.setter
    def is_stop_start_load_case(self, value: 'bool'):
        self.wrapped.IsStopStartLoadCase = bool(value) if value else False

    @property
    def power_convergence_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PowerConvergenceTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PowerConvergenceTolerance) if self.wrapped.PowerConvergenceTolerance else None

    @power_convergence_tolerance.setter
    def power_convergence_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.PowerConvergenceTolerance = value

    @property
    def input_shaft_cycles(self) -> 'float':
        '''float: 'InputShaftCycles' is the original name of this property.'''

        return self.wrapped.InputShaftCycles

    @input_shaft_cycles.setter
    def input_shaft_cycles(self, value: 'float'):
        self.wrapped.InputShaftCycles = float(value) if value else 0.0

    @property
    def percentage_of_shaft_torque_alternating(self) -> 'float':
        '''float: 'PercentageOfShaftTorqueAlternating' is the original name of this property.'''

        return self.wrapped.PercentageOfShaftTorqueAlternating

    @percentage_of_shaft_torque_alternating.setter
    def percentage_of_shaft_torque_alternating(self, value: 'float'):
        self.wrapped.PercentageOfShaftTorqueAlternating = float(value) if value else 0.0

    @property
    def planetary_rating_load_sharing_method(self) -> '_301.PlanetaryRatingLoadSharingOption':
        '''PlanetaryRatingLoadSharingOption: 'PlanetaryRatingLoadSharingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryRatingLoadSharingMethod)
        return constructor.new(_301.PlanetaryRatingLoadSharingOption)(value) if value else None

    @planetary_rating_load_sharing_method.setter
    def planetary_rating_load_sharing_method(self, value: '_301.PlanetaryRatingLoadSharingOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryRatingLoadSharingMethod = value

    @property
    def current_time(self) -> 'float':
        '''float: 'CurrentTime' is the original name of this property.'''

        return self.wrapped.CurrentTime

    @current_time.setter
    def current_time(self, value: 'float'):
        self.wrapped.CurrentTime = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.'''

        return self.wrapped.Duration

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def advanced_system_deflection_options(self) -> '_6905.AdvancedSystemDeflectionOptions':
        '''AdvancedSystemDeflectionOptions: 'AdvancedSystemDeflectionOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6905.AdvancedSystemDeflectionOptions)(self.wrapped.AdvancedSystemDeflectionOptions) if self.wrapped.AdvancedSystemDeflectionOptions else None

    @property
    def te_set_up_for_dynamic_analyses_options(self) -> '_2352.TESetUpForDynamicAnalysisOptions':
        '''TESetUpForDynamicAnalysisOptions: 'TESetUpForDynamicAnalysesOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2352.TESetUpForDynamicAnalysisOptions)(self.wrapped.TESetUpForDynamicAnalysesOptions) if self.wrapped.TESetUpForDynamicAnalysesOptions else None

    @property
    def harmonic_analysis_options(self) -> '_5673.HarmonicAnalysisOptions':
        '''HarmonicAnalysisOptions: 'HarmonicAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5673.HarmonicAnalysisOptions.TYPE not in self.wrapped.HarmonicAnalysisOptions.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis_options to HarmonicAnalysisOptions. Expected: {}.'.format(self.wrapped.HarmonicAnalysisOptions.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicAnalysisOptions.__class__)(self.wrapped.HarmonicAnalysisOptions) if self.wrapped.HarmonicAnalysisOptions else None

    @property
    def harmonic_analysis_options_for_atsam(self) -> '_5673.HarmonicAnalysisOptions':
        '''HarmonicAnalysisOptions: 'HarmonicAnalysisOptionsForATSAM' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5673.HarmonicAnalysisOptions.TYPE not in self.wrapped.HarmonicAnalysisOptionsForATSAM.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis_options_for_atsam to HarmonicAnalysisOptions. Expected: {}.'.format(self.wrapped.HarmonicAnalysisOptionsForATSAM.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicAnalysisOptionsForATSAM.__class__)(self.wrapped.HarmonicAnalysisOptionsForATSAM) if self.wrapped.HarmonicAnalysisOptionsForATSAM else None

    @property
    def clutch_engagements(self) -> 'List[_5313.ClutchEngagementStatus]':
        '''List[ClutchEngagementStatus]: 'ClutchEngagements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClutchEngagements, constructor.new(_5313.ClutchEngagementStatus))
        return value

    @property
    def concept_clutch_engagements(self) -> 'List[_5314.ConceptSynchroGearEngagementStatus]':
        '''List[ConceptSynchroGearEngagementStatus]: 'ConceptClutchEngagements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptClutchEngagements, constructor.new(_5314.ConceptSynchroGearEngagementStatus))
        return value

    def run_power_flow(self):
        ''' 'RunPowerFlow' is the original name of this method.'''

        self.wrapped.RunPowerFlow()

    def set_face_widths_for_specified_safety_factors_from_power_flow(self):
        ''' 'SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow' is the original name of this method.'''

        self.wrapped.SetFaceWidthsForSpecifiedSafetyFactorsFromPowerFlow()

    def create_time_series_load_case(self):
        ''' 'CreateTimeSeriesLoadCase' is the original name of this method.'''

        self.wrapped.CreateTimeSeriesLoadCase()

    def duplicate(self, new_design_state_group: '_5315.DesignState', name: Optional['str'] = 'None') -> 'StaticLoadCase':
        ''' 'Duplicate' is the original name of this method.

        Args:
            new_design_state_group (mastapy.system_model.analyses_and_results.load_case_groups.DesignState)
            name (str, optional)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase
        '''

        name = str(name)
        method_result = self.wrapped.Duplicate(new_design_state_group.wrapped if new_design_state_group else None, name if name else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
