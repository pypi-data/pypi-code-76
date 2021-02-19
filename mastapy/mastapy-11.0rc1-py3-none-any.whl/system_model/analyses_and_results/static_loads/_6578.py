'''_6578.py

ShaftHubConnectionLoadCase
'''


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import _2269, _2270, _2264
from mastapy.system_model.analyses_and_results.static_loads import _6481
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ShaftHubConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionLoadCase',)


class ShaftHubConnectionLoadCase(_6481.ConnectorLoadCase):
    '''ShaftHubConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def torsional_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TorsionalStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TorsionalStiffness) if self.wrapped.TorsionalStiffness else None

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TorsionalStiffness = value

    @property
    def additional_tilt_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AdditionalTiltStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AdditionalTiltStiffness) if self.wrapped.AdditionalTiltStiffness else None

    @additional_tilt_stiffness.setter
    def additional_tilt_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AdditionalTiltStiffness = value

    @property
    def tilt_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TiltStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TiltStiffness) if self.wrapped.TiltStiffness else None

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TiltStiffness = value

    @property
    def radial_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialStiffness) if self.wrapped.RadialStiffness else None

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadialStiffness = value

    @property
    def axial_stiffness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialStiffness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialStiffness) if self.wrapped.AxialStiffness else None

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialStiffness = value

    @property
    def radial_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadialClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadialClearance) if self.wrapped.RadialClearance else None

    @radial_clearance.setter
    def radial_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadialClearance = value

    @property
    def tilt_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TiltClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TiltClearance) if self.wrapped.TiltClearance else None

    @tilt_clearance.setter
    def tilt_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TiltClearance = value

    @property
    def normal_clearance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NormalClearance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NormalClearance) if self.wrapped.NormalClearance else None

    @normal_clearance.setter
    def normal_clearance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.NormalClearance = value

    @property
    def angular_backlash(self) -> 'float':
        '''float: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularBacklash

    @property
    def specified_application_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedApplicationFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedApplicationFactor) if self.wrapped.SpecifiedApplicationFactor else None

    @specified_application_factor.setter
    def specified_application_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpecifiedApplicationFactor = value

    @property
    def specified_backlash_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedBacklashFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedBacklashFactor) if self.wrapped.SpecifiedBacklashFactor else None

    @specified_backlash_factor.setter
    def specified_backlash_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpecifiedBacklashFactor = value

    @property
    def specified_load_distribution_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedLoadDistributionFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedLoadDistributionFactor) if self.wrapped.SpecifiedLoadDistributionFactor else None

    @specified_load_distribution_factor.setter
    def specified_load_distribution_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpecifiedLoadDistributionFactor = value

    @property
    def specified_load_sharing_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpecifiedLoadSharingFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpecifiedLoadSharingFactor) if self.wrapped.SpecifiedLoadSharingFactor else None

    @specified_load_sharing_factor.setter
    def specified_load_sharing_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SpecifiedLoadSharingFactor = value

    @property
    def load_distribution_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LoadDistributionFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LoadDistributionFactor) if self.wrapped.LoadDistributionFactor else None

    @load_distribution_factor.setter
    def load_distribution_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.LoadDistributionFactor = value

    @property
    def torsional_twist_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TorsionalTwistPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TorsionalTwistPreload) if self.wrapped.TorsionalTwistPreload else None

    @torsional_twist_preload.setter
    def torsional_twist_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.TorsionalTwistPreload = value

    @property
    def axial_preload(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AxialPreload' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AxialPreload) if self.wrapped.AxialPreload else None

    @axial_preload.setter
    def axial_preload(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.AxialPreload = value

    @property
    def application_factor(self) -> 'float':
        '''float: 'ApplicationFactor' is the original name of this property.'''

        return self.wrapped.ApplicationFactor

    @application_factor.setter
    def application_factor(self, value: 'float'):
        self.wrapped.ApplicationFactor = float(value) if value else 0.0

    @property
    def load_distribution_factor_single_key(self) -> 'float':
        '''float: 'LoadDistributionFactorSingleKey' is the original name of this property.'''

        return self.wrapped.LoadDistributionFactorSingleKey

    @load_distribution_factor_single_key.setter
    def load_distribution_factor_single_key(self, value: 'float'):
        self.wrapped.LoadDistributionFactorSingleKey = float(value) if value else 0.0

    @property
    def number_of_torque_reversals(self) -> 'float':
        '''float: 'NumberOfTorqueReversals' is the original name of this property.'''

        return self.wrapped.NumberOfTorqueReversals

    @number_of_torque_reversals.setter
    def number_of_torque_reversals(self, value: 'float'):
        self.wrapped.NumberOfTorqueReversals = float(value) if value else 0.0

    @property
    def number_of_torque_peaks(self) -> 'float':
        '''float: 'NumberOfTorquePeaks' is the original name of this property.'''

        return self.wrapped.NumberOfTorquePeaks

    @number_of_torque_peaks.setter
    def number_of_torque_peaks(self, value: 'float'):
        self.wrapped.NumberOfTorquePeaks = float(value) if value else 0.0

    @property
    def component_design(self) -> '_2269.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2269.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def left_flank_lead_relief(self) -> '_2270.SplineLeadRelief':
        '''SplineLeadRelief: 'LeftFlankLeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2270.SplineLeadRelief)(self.wrapped.LeftFlankLeadRelief) if self.wrapped.LeftFlankLeadRelief else None

    @property
    def right_flank_lead_relief(self) -> '_2270.SplineLeadRelief':
        '''SplineLeadRelief: 'RightFlankLeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2270.SplineLeadRelief)(self.wrapped.RightFlankLeadRelief) if self.wrapped.RightFlankLeadRelief else None

    @property
    def tooth_locations_external_spline_half(self) -> 'List[_2264.RigidConnectorToothLocation]':
        '''List[RigidConnectorToothLocation]: 'ToothLocationsExternalSplineHalf' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ToothLocationsExternalSplineHalf, constructor.new(_2264.RigidConnectorToothLocation))
        return value

    @property
    def lead_reliefs(self) -> 'List[_2270.SplineLeadRelief]':
        '''List[SplineLeadRelief]: 'LeadReliefs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeadReliefs, constructor.new(_2270.SplineLeadRelief))
        return value
