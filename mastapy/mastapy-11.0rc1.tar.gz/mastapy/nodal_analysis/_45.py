'''_45.py

AnalysisSettings
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _73, _74
from mastapy.utility import _1348
from mastapy._internal.python_net import python_net_import

_ANALYSIS_SETTINGS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'AnalysisSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('AnalysisSettings',)


class AnalysisSettings(_1348.PerMachineSettings):
    '''AnalysisSettings

    This is a mastapy class.
    '''

    TYPE = _ANALYSIS_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AnalysisSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(self) -> 'bool':
        '''bool: 'RemoveRigidBodyRotationThetaZTwistFromShaftReporting' is the original name of this property.'''

        return self.wrapped.RemoveRigidBodyRotationThetaZTwistFromShaftReporting

    @remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting.setter
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(self, value: 'bool'):
        self.wrapped.RemoveRigidBodyRotationThetaZTwistFromShaftReporting = bool(value) if value else False

    @property
    def rating_type_for_bearing_reliability(self) -> '_73.RatingTypeForBearingReliability':
        '''RatingTypeForBearingReliability: 'RatingTypeForBearingReliability' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RatingTypeForBearingReliability)
        return constructor.new(_73.RatingTypeForBearingReliability)(value) if value else None

    @rating_type_for_bearing_reliability.setter
    def rating_type_for_bearing_reliability(self, value: '_73.RatingTypeForBearingReliability'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RatingTypeForBearingReliability = value

    @property
    def rating_type_for_shaft_reliability(self) -> '_74.RatingTypeForShaftReliability':
        '''RatingTypeForShaftReliability: 'RatingTypeForShaftReliability' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.RatingTypeForShaftReliability)
        return constructor.new(_74.RatingTypeForShaftReliability)(value) if value else None

    @rating_type_for_shaft_reliability.setter
    def rating_type_for_shaft_reliability(self, value: '_74.RatingTypeForShaftReliability'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RatingTypeForShaftReliability = value

    @property
    def system_deflection_maximum_iterations(self) -> 'int':
        '''int: 'SystemDeflectionMaximumIterations' is the original name of this property.'''

        return self.wrapped.SystemDeflectionMaximumIterations

    @system_deflection_maximum_iterations.setter
    def system_deflection_maximum_iterations(self, value: 'int'):
        self.wrapped.SystemDeflectionMaximumIterations = int(value) if value else 0

    @property
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(self) -> 'bool':
        '''bool: 'OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations' is the original name of this property.'''

        return self.wrapped.OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations

    @overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations.setter
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(self, value: 'bool'):
        self.wrapped.OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations = bool(value) if value else False

    @property
    def maximum_section_length_to_diameter_ratio(self) -> 'float':
        '''float: 'MaximumSectionLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.MaximumSectionLengthToDiameterRatio

    @maximum_section_length_to_diameter_ratio.setter
    def maximum_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumSectionLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def spline_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'SplineNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.SplineNodesPerUnitLengthToDiameterRatio

    @spline_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_spline_connections(self) -> 'bool':
        '''bool: 'UseSingleNodeForSplineConnections' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForSplineConnections

    @use_single_node_for_spline_connections.setter
    def use_single_node_for_spline_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineConnections = bool(value) if value else False

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        '''float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property.'''

        return self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value else 0.0

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        '''bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property.'''

        return self.wrapped.UseSingleNodeForCylindricalGearMeshes

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value else False

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        '''int: 'MinimumNumberOfGearMeshNodes' is the original name of this property.'''

        return self.wrapped.MinimumNumberOfGearMeshNodes

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value else 0
