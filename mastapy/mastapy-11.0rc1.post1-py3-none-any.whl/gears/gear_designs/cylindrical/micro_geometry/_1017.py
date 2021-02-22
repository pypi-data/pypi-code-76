'''_1017.py

CylindricalGearFlankMicroGeometry
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import (
    _1025, _1026, _1018, _1019,
    _1016, _1024, _1043, _1044,
    _1031, _1033, _1039, _1041
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _952, _941, _967
from mastapy.gears.micro_geometry import _517
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearFlankMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFlankMicroGeometry',)


class CylindricalGearFlankMicroGeometry(_517.FlankMicroGeometry):
    '''CylindricalGearFlankMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_FLANK_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearFlankMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def read_micro_geometry_from_an_external_file_using_file_name(self) -> 'str':
        '''str: 'ReadMicroGeometryFromAnExternalFileUsingFileName' is the original name of this property.'''

        return self.wrapped.ReadMicroGeometryFromAnExternalFileUsingFileName

    @read_micro_geometry_from_an_external_file_using_file_name.setter
    def read_micro_geometry_from_an_external_file_using_file_name(self, value: 'str'):
        self.wrapped.ReadMicroGeometryFromAnExternalFileUsingFileName = str(value) if value else None

    @property
    def modified_normal_pressure_angle_due_to_helix_angle_modification_assuming_unmodified_normal_module_and_pressure_angle_modification(self) -> 'float':
        '''float: 'ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModuleAndPressureAngleModification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModuleAndPressureAngleModification

    @property
    def use_measured_map_data(self) -> 'bool':
        '''bool: 'UseMeasuredMapData' is the original name of this property.'''

        return self.wrapped.UseMeasuredMapData

    @use_measured_map_data.setter
    def use_measured_map_data(self, value: 'bool'):
        self.wrapped.UseMeasuredMapData = bool(value) if value else False

    @property
    def profile_relief(self) -> '_1025.CylindricalGearProfileModification':
        '''CylindricalGearProfileModification: 'ProfileRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1025.CylindricalGearProfileModification.TYPE not in self.wrapped.ProfileRelief.__class__.__mro__:
            raise CastException('Failed to cast profile_relief to CylindricalGearProfileModification. Expected: {}.'.format(self.wrapped.ProfileRelief.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ProfileRelief.__class__)(self.wrapped.ProfileRelief) if self.wrapped.ProfileRelief else None

    @property
    def lead_relief(self) -> '_1018.CylindricalGearLeadModification':
        '''CylindricalGearLeadModification: 'LeadRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1018.CylindricalGearLeadModification.TYPE not in self.wrapped.LeadRelief.__class__.__mro__:
            raise CastException('Failed to cast lead_relief to CylindricalGearLeadModification. Expected: {}.'.format(self.wrapped.LeadRelief.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LeadRelief.__class__)(self.wrapped.LeadRelief) if self.wrapped.LeadRelief else None

    @property
    def bias(self) -> '_1016.CylindricalGearBiasModification':
        '''CylindricalGearBiasModification: 'Bias' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1016.CylindricalGearBiasModification)(self.wrapped.Bias) if self.wrapped.Bias else None

    @property
    def profile_control_point(self) -> '_952.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ProfileControlPoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_952.CylindricalGearProfileMeasurement)(self.wrapped.ProfileControlPoint) if self.wrapped.ProfileControlPoint else None

    @property
    def micro_geometry_map(self) -> '_1024.CylindricalGearMicroGeometryMap':
        '''CylindricalGearMicroGeometryMap: 'MicroGeometryMap' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1024.CylindricalGearMicroGeometryMap)(self.wrapped.MicroGeometryMap) if self.wrapped.MicroGeometryMap else None

    @property
    def total_lead_relief_points(self) -> 'List[_1043.TotalLeadReliefWithDeviation]':
        '''List[TotalLeadReliefWithDeviation]: 'TotalLeadReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TotalLeadReliefPoints, constructor.new(_1043.TotalLeadReliefWithDeviation))
        return value

    @property
    def total_profile_relief_points(self) -> 'List[_1044.TotalProfileReliefWithDeviation]':
        '''List[TotalProfileReliefWithDeviation]: 'TotalProfileReliefPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TotalProfileReliefPoints, constructor.new(_1044.TotalProfileReliefWithDeviation))
        return value

    @property
    def lead_form_deviation_points(self) -> 'List[_1031.LeadFormReliefWithDeviation]':
        '''List[LeadFormReliefWithDeviation]: 'LeadFormDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeadFormDeviationPoints, constructor.new(_1031.LeadFormReliefWithDeviation))
        return value

    @property
    def lead_slope_deviation_points(self) -> 'List[_1033.LeadSlopeReliefWithDeviation]':
        '''List[LeadSlopeReliefWithDeviation]: 'LeadSlopeDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LeadSlopeDeviationPoints, constructor.new(_1033.LeadSlopeReliefWithDeviation))
        return value

    @property
    def profile_form_deviation_points(self) -> 'List[_1039.ProfileFormReliefWithDeviation]':
        '''List[ProfileFormReliefWithDeviation]: 'ProfileFormDeviationPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileFormDeviationPoints, constructor.new(_1039.ProfileFormReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_10_percent_face_width(self) -> 'List[_1041.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt10PercentFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt10PercentFaceWidth, constructor.new(_1041.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_50_percent_face_width(self) -> 'List[_1041.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt50PercentFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt50PercentFaceWidth, constructor.new(_1041.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def profile_slope_deviation_at_90_percent_face_width(self) -> 'List[_1041.ProfileSlopeReliefWithDeviation]':
        '''List[ProfileSlopeReliefWithDeviation]: 'ProfileSlopeDeviationAt90PercentFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ProfileSlopeDeviationAt90PercentFaceWidth, constructor.new(_1041.ProfileSlopeReliefWithDeviation))
        return value

    @property
    def gear_design(self) -> '_941.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.CylindricalGearDesign.TYPE not in self.wrapped.GearDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_design to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDesign.__class__)(self.wrapped.GearDesign) if self.wrapped.GearDesign else None

    def read_micro_geometry_from_an_external_file(self):
        ''' 'ReadMicroGeometryFromAnExternalFile' is the original name of this method.'''

        self.wrapped.ReadMicroGeometryFromAnExternalFile()

    def total_relief(self, face_width: 'float', roll_distance: 'float') -> 'float':
        ''' 'TotalRelief' is the original name of this method.

        Args:
            face_width (float)
            roll_distance (float)

        Returns:
            float
        '''

        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = self.wrapped.TotalRelief(face_width if face_width else 0.0, roll_distance if roll_distance else 0.0)
        return method_result
