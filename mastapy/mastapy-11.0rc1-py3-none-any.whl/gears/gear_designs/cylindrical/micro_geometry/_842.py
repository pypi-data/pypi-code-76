'''_842.py

CylindricalGearBiasModification
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _783
from mastapy.gears.micro_geometry import _352
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BIAS_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearBiasModification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBiasModification',)


class CylindricalGearBiasModification(_352.BiasModification):
    '''CylindricalGearBiasModification

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_BIAS_MODIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearBiasModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_evaluation_upper_limit(self) -> 'float':
        '''float: 'LeadEvaluationUpperLimit' is the original name of this property.'''

        return self.wrapped.LeadEvaluationUpperLimit

    @lead_evaluation_upper_limit.setter
    def lead_evaluation_upper_limit(self, value: 'float'):
        self.wrapped.LeadEvaluationUpperLimit = float(value) if value else 0.0

    @property
    def lead_evaluation_lower_limit(self) -> 'float':
        '''float: 'LeadEvaluationLowerLimit' is the original name of this property.'''

        return self.wrapped.LeadEvaluationLowerLimit

    @lead_evaluation_lower_limit.setter
    def lead_evaluation_lower_limit(self, value: 'float'):
        self.wrapped.LeadEvaluationLowerLimit = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_roll_distance(self) -> 'float':
        '''float: 'ProfileEvaluationUpperLimitRollDistance' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationUpperLimitRollDistance

    @profile_evaluation_upper_limit_roll_distance.setter
    def profile_evaluation_upper_limit_roll_distance(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRollDistance = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_roll_distance(self) -> 'float':
        '''float: 'ProfileEvaluationLowerLimitRollDistance' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationLowerLimitRollDistance

    @profile_evaluation_lower_limit_roll_distance.setter
    def profile_evaluation_lower_limit_roll_distance(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRollDistance = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_diameter(self) -> 'float':
        '''float: 'ProfileEvaluationUpperLimitDiameter' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationUpperLimitDiameter

    @profile_evaluation_upper_limit_diameter.setter
    def profile_evaluation_upper_limit_diameter(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitDiameter = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_radius(self) -> 'float':
        '''float: 'ProfileEvaluationUpperLimitRadius' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationUpperLimitRadius

    @profile_evaluation_upper_limit_radius.setter
    def profile_evaluation_upper_limit_radius(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRadius = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit_roll_angle(self) -> 'float':
        '''float: 'ProfileEvaluationUpperLimitRollAngle' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationUpperLimitRollAngle

    @profile_evaluation_upper_limit_roll_angle.setter
    def profile_evaluation_upper_limit_roll_angle(self, value: 'float'):
        self.wrapped.ProfileEvaluationUpperLimitRollAngle = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_diameter(self) -> 'float':
        '''float: 'ProfileEvaluationLowerLimitDiameter' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationLowerLimitDiameter

    @profile_evaluation_lower_limit_diameter.setter
    def profile_evaluation_lower_limit_diameter(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitDiameter = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_radius(self) -> 'float':
        '''float: 'ProfileEvaluationLowerLimitRadius' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationLowerLimitRadius

    @profile_evaluation_lower_limit_radius.setter
    def profile_evaluation_lower_limit_radius(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRadius = float(value) if value else 0.0

    @property
    def profile_evaluation_lower_limit_roll_angle(self) -> 'float':
        '''float: 'ProfileEvaluationLowerLimitRollAngle' is the original name of this property.'''

        return self.wrapped.ProfileEvaluationLowerLimitRollAngle

    @profile_evaluation_lower_limit_roll_angle.setter
    def profile_evaluation_lower_limit_roll_angle(self, value: 'float'):
        self.wrapped.ProfileEvaluationLowerLimitRollAngle = float(value) if value else 0.0

    @property
    def pressure_angle_mod_at_upper_limit(self) -> 'float':
        '''float: 'PressureAngleModAtUpperLimit' is the original name of this property.'''

        return self.wrapped.PressureAngleModAtUpperLimit

    @pressure_angle_mod_at_upper_limit.setter
    def pressure_angle_mod_at_upper_limit(self, value: 'float'):
        self.wrapped.PressureAngleModAtUpperLimit = float(value) if value else 0.0

    @property
    def pressure_angle_mod_at_lower_limit(self) -> 'float':
        '''float: 'PressureAngleModAtLowerLimit' is the original name of this property.'''

        return self.wrapped.PressureAngleModAtLowerLimit

    @pressure_angle_mod_at_lower_limit.setter
    def pressure_angle_mod_at_lower_limit(self, value: 'float'):
        self.wrapped.PressureAngleModAtLowerLimit = float(value) if value else 0.0

    @property
    def relief_at_upper_limit_isoagmadin(self) -> 'float':
        '''float: 'ReliefAtUpperLimitISOAGMADIN' is the original name of this property.'''

        return self.wrapped.ReliefAtUpperLimitISOAGMADIN

    @relief_at_upper_limit_isoagmadin.setter
    def relief_at_upper_limit_isoagmadin(self, value: 'float'):
        self.wrapped.ReliefAtUpperLimitISOAGMADIN = float(value) if value else 0.0

    @property
    def relief_at_upper_limit_vdi(self) -> 'float':
        '''float: 'ReliefAtUpperLimitVDI' is the original name of this property.'''

        return self.wrapped.ReliefAtUpperLimitVDI

    @relief_at_upper_limit_vdi.setter
    def relief_at_upper_limit_vdi(self, value: 'float'):
        self.wrapped.ReliefAtUpperLimitVDI = float(value) if value else 0.0

    @property
    def relief_at_upper_limit_ldp(self) -> 'float':
        '''float: 'ReliefAtUpperLimitLDP' is the original name of this property.'''

        return self.wrapped.ReliefAtUpperLimitLDP

    @relief_at_upper_limit_ldp.setter
    def relief_at_upper_limit_ldp(self, value: 'float'):
        self.wrapped.ReliefAtUpperLimitLDP = float(value) if value else 0.0

    @property
    def relief_at_lower_limit_isoagmadin(self) -> 'float':
        '''float: 'ReliefAtLowerLimitISOAGMADIN' is the original name of this property.'''

        return self.wrapped.ReliefAtLowerLimitISOAGMADIN

    @relief_at_lower_limit_isoagmadin.setter
    def relief_at_lower_limit_isoagmadin(self, value: 'float'):
        self.wrapped.ReliefAtLowerLimitISOAGMADIN = float(value) if value else 0.0

    @property
    def relief_at_lower_limit_vdi(self) -> 'float':
        '''float: 'ReliefAtLowerLimitVDI' is the original name of this property.'''

        return self.wrapped.ReliefAtLowerLimitVDI

    @relief_at_lower_limit_vdi.setter
    def relief_at_lower_limit_vdi(self, value: 'float'):
        self.wrapped.ReliefAtLowerLimitVDI = float(value) if value else 0.0

    @property
    def relief_at_lower_limit_ldp(self) -> 'float':
        '''float: 'ReliefAtLowerLimitLDP' is the original name of this property.'''

        return self.wrapped.ReliefAtLowerLimitLDP

    @relief_at_lower_limit_ldp.setter
    def relief_at_lower_limit_ldp(self, value: 'float'):
        self.wrapped.ReliefAtLowerLimitLDP = float(value) if value else 0.0

    @property
    def profile_evaluation_upper_limit(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ProfileEvaluationUpperLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.ProfileEvaluationUpperLimit) if self.wrapped.ProfileEvaluationUpperLimit else None

    @property
    def profile_evaluation_lower_limit(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ProfileEvaluationLowerLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.ProfileEvaluationLowerLimit) if self.wrapped.ProfileEvaluationLowerLimit else None

    @property
    def zero_bias_relief(self) -> '_783.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'ZeroBiasRelief' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_783.CylindricalGearProfileMeasurement)(self.wrapped.ZeroBiasRelief) if self.wrapped.ZeroBiasRelief else None

    def relief_of(self, face_width: 'float', roll_distance: 'float') -> 'float':
        ''' 'ReliefOf' is the original name of this method.

        Args:
            face_width (float)
            roll_distance (float)

        Returns:
            float
        '''

        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = self.wrapped.ReliefOf(face_width if face_width else 0.0, roll_distance if roll_distance else 0.0)
        return method_result
