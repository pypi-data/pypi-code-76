'''_628.py

CylindricalGearMeshLoadDistributionAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical import _254
from mastapy.gears.load_case.cylindrical import _655
from mastapy.gears.ltca import _608, _614
from mastapy.gears.ltca.cylindrical import _630, _632
from mastapy._math.vector_2d import Vector2D
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearMeshLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshLoadDistributionAnalysis',)


class CylindricalGearMeshLoadDistributionAnalysis(_614.GearMeshLoadDistributionAnalysis):
    '''CylindricalGearMeshLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso63362006_single_stiffness(self) -> 'float':
        '''float: 'ISO63362006SingleStiffness' is the original name of this property.'''

        return self.wrapped.ISO63362006SingleStiffness

    @iso63362006_single_stiffness.setter
    def iso63362006_single_stiffness(self, value: 'float'):
        self.wrapped.ISO63362006SingleStiffness = float(value) if value else 0.0

    @property
    def iso63362006_single_stiffness_across_face_width(self) -> 'float':
        '''float: 'ISO63362006SingleStiffnessAcrossFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO63362006SingleStiffnessAcrossFaceWidth

    @property
    def iso63362006_mesh_stiffness(self) -> 'float':
        '''float: 'ISO63362006MeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO63362006MeshStiffness

    @property
    def iso63362006_mesh_stiffness_across_face_width(self) -> 'float':
        '''float: 'ISO63362006MeshStiffnessAcrossFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ISO63362006MeshStiffnessAcrossFaceWidth

    @property
    def strip_loads_minimum(self) -> 'float':
        '''float: 'StripLoadsMinimum' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StripLoadsMinimum

    @property
    def strip_loads_maximum(self) -> 'float':
        '''float: 'StripLoadsMaximum' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StripLoadsMaximum

    @property
    def strip_loads_deviation(self) -> 'float':
        '''float: 'StripLoadsDeviation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StripLoadsDeviation

    @property
    def theoretical_total_contact_ratio(self) -> 'float':
        '''float: 'TheoreticalTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TheoreticalTotalContactRatio

    @property
    def misalignment(self) -> 'float':
        '''float: 'Misalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Misalignment

    @property
    def calculated_face_load_factor_contact(self) -> 'float':
        '''float: 'CalculatedFaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculatedFaceLoadFactorContact

    @property
    def maximum_edge_pressure(self) -> 'float':
        '''float: 'MaximumEdgePressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgePressure

    @property
    def mean_te(self) -> 'float':
        '''float: 'MeanTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTE

    @property
    def peak_to_peak_te(self) -> 'float':
        '''float: 'PeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeakTE

    @property
    def utilization_force_per_unit_length_cutoff_value(self) -> 'float':
        '''float: 'UtilizationForcePerUnitLengthCutoffValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UtilizationForcePerUnitLengthCutoffValue

    @property
    def percentage_of_potential_contact_area_loaded(self) -> 'float':
        '''float: 'PercentageOfPotentialContactAreaLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageOfPotentialContactAreaLoaded

    @property
    def percentage_of_potential_contact_area_utilized(self) -> 'float':
        '''float: 'PercentageOfPotentialContactAreaUtilized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageOfPotentialContactAreaUtilized

    @property
    def percentage_of_effective_face_width_utilized(self) -> 'float':
        '''float: 'PercentageOfEffectiveFaceWidthUtilized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageOfEffectiveFaceWidthUtilized

    @property
    def percentage_of_effective_profile_utilized(self) -> 'float':
        '''float: 'PercentageOfEffectiveProfileUtilized' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentageOfEffectiveProfileUtilized

    @property
    def rating(self) -> '_254.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_254.CylindricalGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def cylindrical_mesh_load_case(self) -> '_655.CylindricalMeshLoadCase':
        '''CylindricalMeshLoadCase: 'CylindricalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_655.CylindricalMeshLoadCase)(self.wrapped.CylindricalMeshLoadCase) if self.wrapped.CylindricalMeshLoadCase else None

    @property
    def gear_a_in_mesh(self) -> '_608.CylindricalMeshedGearLoadDistributionAnalysis':
        '''CylindricalMeshedGearLoadDistributionAnalysis: 'GearAInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_608.CylindricalMeshedGearLoadDistributionAnalysis)(self.wrapped.GearAInMesh) if self.wrapped.GearAInMesh else None

    @property
    def gear_b_in_mesh(self) -> '_608.CylindricalMeshedGearLoadDistributionAnalysis':
        '''CylindricalMeshedGearLoadDistributionAnalysis: 'GearBInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_608.CylindricalMeshedGearLoadDistributionAnalysis)(self.wrapped.GearBInMesh) if self.wrapped.GearBInMesh else None

    @property
    def point_with_maximum_contact_pressure(self) -> '_630.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'PointWithMaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_630.CylindricalGearMeshLoadedContactPoint)(self.wrapped.PointWithMaximumContactPressure) if self.wrapped.PointWithMaximumContactPressure else None

    @property
    def load_distribution_analyses_at_single_rotation(self) -> 'List[_632.CylindricalMeshLoadDistributionAtRotation]':
        '''List[CylindricalMeshLoadDistributionAtRotation]: 'LoadDistributionAnalysesAtSingleRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadDistributionAnalysesAtSingleRotation, constructor.new(_632.CylindricalMeshLoadDistributionAtRotation))
        return value

    @property
    def meshed_gears(self) -> 'List[_608.CylindricalMeshedGearLoadDistributionAnalysis]':
        '''List[CylindricalMeshedGearLoadDistributionAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_608.CylindricalMeshedGearLoadDistributionAnalysis))
        return value

    @property
    def transmission_error_against_rotation(self) -> 'List[Vector2D]':
        '''List[Vector2D]: 'TransmissionErrorAgainstRotation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TransmissionErrorAgainstRotation, Vector2D)
        return value
