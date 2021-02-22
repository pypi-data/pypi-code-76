'''_2312.py

CylindricalGearMeshSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.scripting import _6574
from mastapy.system_model.connections_and_sockets.gears import _1926
from mastapy.system_model.analyses_and_results.static_loads import _6163
from mastapy.system_model.analyses_and_results.power_flows import _3322
from mastapy.gears.rating.cylindrical import _254
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2318, _2319, _2320, _2321,
    _2329
)
from mastapy._internal.cast_exception import CastException
from mastapy.nodal_analysis import _1383
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2412
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CylindricalGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSystemDeflection',)


class CylindricalGearMeshSystemDeflection(_2329.GearMeshSystemDeflection):
    '''CylindricalGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_in_contact(self) -> 'bool':
        '''bool: 'IsInContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInContact

    @property
    def pinion_torque_for_ltca(self) -> 'float':
        '''float: 'PinionTorqueForLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionTorqueForLTCA

    @property
    def separation(self) -> 'float':
        '''float: 'Separation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Separation

    @property
    def separation_to_inactive_flank(self) -> 'float':
        '''float: 'SeparationToInactiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationToInactiveFlank

    @property
    def load_in_loa_from_ltca(self) -> 'float':
        '''float: 'LoadInLOAFromLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadInLOAFromLTCA

    @property
    def transmission_error_including_backlash(self) -> 'float':
        '''float: 'TransmissionErrorIncludingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransmissionErrorIncludingBacklash

    @property
    def transmission_error_no_backlash(self) -> 'float':
        '''float: 'TransmissionErrorNoBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransmissionErrorNoBacklash

    @property
    def angular_misalignment_for_gear_whine_analysis(self) -> 'float':
        '''float: 'AngularMisalignmentForGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularMisalignmentForGearWhineAnalysis

    @property
    def average_interference_normal_to_the_flank(self) -> 'float':
        '''float: 'AverageInterferenceNormalToTheFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageInterferenceNormalToTheFlank

    @property
    def estimated_operating_tooth_temperature(self) -> 'float':
        '''float: 'EstimatedOperatingToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EstimatedOperatingToothTemperature

    @property
    def minimum_operating_backlash(self) -> 'float':
        '''float: 'MinimumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingBacklash

    @property
    def maximum_operating_backlash(self) -> 'float':
        '''float: 'MaximumOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumOperatingBacklash

    @property
    def average_operating_backlash(self) -> 'float':
        '''float: 'AverageOperatingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOperatingBacklash

    @property
    def change_in_operating_backlash_due_to_thermal_effects(self) -> 'float':
        '''float: 'ChangeInOperatingBacklashDueToThermalEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInOperatingBacklashDueToThermalEffects

    @property
    def change_in_backlash_due_to_tooth_expansion(self) -> 'float':
        '''float: 'ChangeInBacklashDueToToothExpansion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInBacklashDueToToothExpansion

    @property
    def minimum_operating_centre_distance(self) -> 'float':
        '''float: 'MinimumOperatingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingCentreDistance

    @property
    def maximum_operating_centre_distance(self) -> 'float':
        '''float: 'MaximumOperatingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumOperatingCentreDistance

    @property
    def smallest_effective_operating_centre_distance(self) -> 'float':
        '''float: 'SmallestEffectiveOperatingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestEffectiveOperatingCentreDistance

    @property
    def minimum_change_in_centre_distance_due_to_misalignment(self) -> 'float':
        '''float: 'MinimumChangeInCentreDistanceDueToMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumChangeInCentreDistanceDueToMisalignment

    @property
    def maximum_change_in_centre_distance_due_to_misalignment(self) -> 'float':
        '''float: 'MaximumChangeInCentreDistanceDueToMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumChangeInCentreDistanceDueToMisalignment

    @property
    def node_pair_changes_in_operating_centre_distance_due_to_misalignment(self) -> 'List[float]':
        '''List[float]: 'NodePairChangesInOperatingCentreDistanceDueToMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodePairChangesInOperatingCentreDistanceDueToMisalignment)
        return value

    @property
    def node_pair_transverse_separations_for_ltca(self) -> 'List[float]':
        '''List[float]: 'NodePairTransverseSeparationsForLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.NodePairTransverseSeparationsForLTCA)
        return value

    @property
    def change_in_operating_pitch_diameter_due_to_thermal_effects(self) -> 'List[float]':
        '''List[float]: 'ChangeInOperatingPitchDiameterDueToThermalEffects' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ChangeInOperatingPitchDiameterDueToThermalEffects)
        return value

    @property
    def minimum_change_in_centre_distance(self) -> 'float':
        '''float: 'MinimumChangeInCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumChangeInCentreDistance

    @property
    def maximum_change_in_centre_distance(self) -> 'float':
        '''float: 'MaximumChangeInCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumChangeInCentreDistance

    @property
    def operating_sap_diameter(self) -> 'List[float]':
        '''List[float]: 'OperatingSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.OperatingSAPDiameter)
        return value

    @property
    def operating_eap_diameter(self) -> 'List[float]':
        '''List[float]: 'OperatingEAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.OperatingEAPDiameter)
        return value

    @property
    def operating_form_diameter(self) -> 'List[float]':
        '''List[float]: 'OperatingFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.OperatingFormDiameter)
        return value

    @property
    def operating_tip_diameter(self) -> 'List[float]':
        '''List[float]: 'OperatingTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.OperatingTipDiameter)
        return value

    @property
    def minimum_operating_transverse_contact_ratio(self) -> 'float':
        '''float: 'MinimumOperatingTransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumOperatingTransverseContactRatio

    @property
    def maximum_operating_transverse_contact_ratio(self) -> 'float':
        '''float: 'MaximumOperatingTransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumOperatingTransverseContactRatio

    @property
    def minimum_operating_tip_clearance(self) -> 'List[float]':
        '''List[float]: 'MinimumOperatingTipClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.MinimumOperatingTipClearance)
        return value

    @property
    def minimum_clearance_from_form_diameter_to_sap_diameter(self) -> 'List[float]':
        '''List[float]: 'MinimumClearanceFromFormDiameterToSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.MinimumClearanceFromFormDiameterToSAPDiameter)
        return value

    @property
    def chart_of_effective_change_in_operating_centre_distance(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ChartOfEffectiveChangeInOperatingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ChartOfEffectiveChangeInOperatingCentreDistance) if self.wrapped.ChartOfEffectiveChangeInOperatingCentreDistance else None

    @property
    def tilt_x(self) -> 'List[float]':
        '''List[float]: 'TiltX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TiltX)
        return value

    @property
    def tilt_y(self) -> 'List[float]':
        '''List[float]: 'TiltY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.TiltY)
        return value

    @property
    def signed_root_mean_square_planetary_equivalent_misalignment(self) -> 'float':
        '''float: 'SignedRootMeanSquarePlanetaryEquivalentMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedRootMeanSquarePlanetaryEquivalentMisalignment

    @property
    def worst_planetary_misalignment(self) -> 'float':
        '''float: 'WorstPlanetaryMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorstPlanetaryMisalignment

    @property
    def calculated_worst_load_sharing_factor(self) -> 'float':
        '''float: 'CalculatedWorstLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculatedWorstLoadSharingFactor

    @property
    def calculated_load_sharing_factor(self) -> 'float':
        '''float: 'CalculatedLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculatedLoadSharingFactor

    @property
    def gear_mesh_tilt_stiffness_method(self) -> 'str':
        '''str: 'GearMeshTiltStiffnessMethod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GearMeshTiltStiffnessMethod

    @property
    def crowning_for_tilt_stiffness_gear_a(self) -> 'float':
        '''float: 'CrowningForTiltStiffnessGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CrowningForTiltStiffnessGearA

    @property
    def crowning_for_tilt_stiffness_gear_b(self) -> 'float':
        '''float: 'CrowningForTiltStiffnessGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CrowningForTiltStiffnessGearB

    @property
    def linear_relief_for_tilt_stiffness_gear_a(self) -> 'float':
        '''float: 'LinearReliefForTiltStiffnessGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinearReliefForTiltStiffnessGearA

    @property
    def linear_relief_for_tilt_stiffness_gear_b(self) -> 'float':
        '''float: 'LinearReliefForTiltStiffnessGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinearReliefForTiltStiffnessGearB

    @property
    def connection_design(self) -> '_1926.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1926.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6163.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6163.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3322.CylindricalGearMeshPowerFlow':
        '''CylindricalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3322.CylindricalGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_254.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_254.CylindricalGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_254.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_254.CylindricalGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gear_a(self) -> '_2318.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2318.CylindricalGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2319.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.CylindricalGearSystemDeflectionTimestep.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2320.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2320.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2321.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2321.CylindricalPlanetGearSystemDeflection.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_2318.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2318.CylindricalGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2319.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2319.CylindricalGearSystemDeflectionTimestep.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2320.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2320.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2321.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2321.CylindricalPlanetGearSystemDeflection.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def misalignment_data(self) -> '_1383.CylindricalMisalignmentCalculator':
        '''CylindricalMisalignmentCalculator: 'MisalignmentData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1383.CylindricalMisalignmentCalculator)(self.wrapped.MisalignmentData) if self.wrapped.MisalignmentData else None

    @property
    def misalignment_data_left_flank(self) -> '_1383.CylindricalMisalignmentCalculator':
        '''CylindricalMisalignmentCalculator: 'MisalignmentDataLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1383.CylindricalMisalignmentCalculator)(self.wrapped.MisalignmentDataLeftFlank) if self.wrapped.MisalignmentDataLeftFlank else None

    @property
    def misalignment_data_right_flank(self) -> '_1383.CylindricalMisalignmentCalculator':
        '''CylindricalMisalignmentCalculator: 'MisalignmentDataRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1383.CylindricalMisalignmentCalculator)(self.wrapped.MisalignmentDataRightFlank) if self.wrapped.MisalignmentDataRightFlank else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshSystemDeflection]':
        '''List[CylindricalGearMeshSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshSystemDeflection))
        return value

    @property
    def cylindrical_gears(self) -> 'List[_2318.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGears, constructor.new(_2318.CylindricalGearSystemDeflection))
        return value

    @property
    def mesh_deflections_left_flank(self) -> 'List[_2412.MeshDeflectionResults]':
        '''List[MeshDeflectionResults]: 'MeshDeflectionsLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshDeflectionsLeftFlank, constructor.new(_2412.MeshDeflectionResults))
        return value

    @property
    def mesh_deflections_right_flank(self) -> 'List[_2412.MeshDeflectionResults]':
        '''List[MeshDeflectionResults]: 'MeshDeflectionsRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshDeflectionsRightFlank, constructor.new(_2412.MeshDeflectionResults))
        return value
