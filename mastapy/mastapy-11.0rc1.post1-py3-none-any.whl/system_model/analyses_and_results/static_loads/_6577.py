'''_6577.py

RootAssemblyLoadCase
'''


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2147
from mastapy.nodal_analysis.varying_input_components import _86, _85, _90
from mastapy.math_utility.control import _1334
from mastapy.system_model.analyses_and_results.static_loads import (
    _6589, _6443, _6496, _6450
)
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4045
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RootAssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyLoadCase',)


class RootAssemblyLoadCase(_6450.AssemblyLoadCase):
    '''RootAssemblyLoadCase

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rayleigh_damping_alpha(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RayleighDampingAlpha' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RayleighDampingAlpha) if self.wrapped.RayleighDampingAlpha else None

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RayleighDampingAlpha = value

    @property
    def max_brake_force(self) -> 'float':
        '''float: 'MaxBrakeForce' is the original name of this property.'''

        return self.wrapped.MaxBrakeForce

    @max_brake_force.setter
    def max_brake_force(self, value: 'float'):
        self.wrapped.MaxBrakeForce = float(value) if value else 0.0

    @property
    def brake_force_gain(self) -> 'float':
        '''float: 'BrakeForceGain' is the original name of this property.'''

        return self.wrapped.BrakeForceGain

    @brake_force_gain.setter
    def brake_force_gain(self, value: 'float'):
        self.wrapped.BrakeForceGain = float(value) if value else 0.0

    @property
    def oil_initial_temperature(self) -> 'float':
        '''float: 'OilInitialTemperature' is the original name of this property.'''

        return self.wrapped.OilInitialTemperature

    @oil_initial_temperature.setter
    def oil_initial_temperature(self, value: 'float'):
        self.wrapped.OilInitialTemperature = float(value) if value else 0.0

    @property
    def assembly_design(self) -> '_2147.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2147.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def brake_force_input_values(self) -> '_86.ForceInputComponent':
        '''ForceInputComponent: 'BrakeForceInputValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_86.ForceInputComponent)(self.wrapped.BrakeForceInputValues) if self.wrapped.BrakeForceInputValues else None

    @property
    def road_incline_input_values(self) -> '_85.AngleInputComponent':
        '''AngleInputComponent: 'RoadInclineInputValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_85.AngleInputComponent)(self.wrapped.RoadInclineInputValues) if self.wrapped.RoadInclineInputValues else None

    @property
    def drive_cycle_pid_control_settings(self) -> '_1334.PIDControlSettings':
        '''PIDControlSettings: 'DriveCyclePIDControlSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1334.PIDControlSettings)(self.wrapped.DriveCyclePIDControlSettings) if self.wrapped.DriveCyclePIDControlSettings else None

    @property
    def target_vehicle_speed(self) -> '_90.VelocityInputComponent':
        '''VelocityInputComponent: 'TargetVehicleSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_90.VelocityInputComponent)(self.wrapped.TargetVehicleSpeed) if self.wrapped.TargetVehicleSpeed else None

    @property
    def load_case(self) -> '_6589.StaticLoadCase':
        '''StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6589.StaticLoadCase.TYPE not in self.wrapped.LoadCase.__class__.__mro__:
            raise CastException('Failed to cast load_case to StaticLoadCase. Expected: {}.'.format(self.wrapped.LoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadCase.__class__)(self.wrapped.LoadCase) if self.wrapped.LoadCase else None

    @property
    def supercharger_rotor_sets(self) -> 'List[_6496.CylindricalGearSetLoadCase]':
        '''List[CylindricalGearSetLoadCase]: 'SuperchargerRotorSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SuperchargerRotorSets, constructor.new(_6496.CylindricalGearSetLoadCase))
        return value
