'''_794.py

CylindricalGearMeshLoadedContactPoint
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _952
from mastapy.gears.ltca import _781
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_POINT = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearMeshLoadedContactPoint')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshLoadedContactPoint',)


class CylindricalGearMeshLoadedContactPoint(_781.GearMeshLoadedContactPoint):
    '''CylindricalGearMeshLoadedContactPoint

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_LOADED_CONTACT_POINT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshLoadedContactPoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width_position_gear_a(self) -> 'float':
        '''float: 'FaceWidthPositionGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthPositionGearA

    @property
    def face_width_position_gear_b(self) -> 'float':
        '''float: 'FaceWidthPositionGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthPositionGearB

    @property
    def sliding_velocity(self) -> 'float':
        '''float: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingVelocity

    @property
    def pressure_velocity_pv(self) -> 'float':
        '''float: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PressureVelocityPV

    @property
    def micropitting_minimum_lubricant_film_thickness(self) -> 'float':
        '''float: 'MicropittingMinimumLubricantFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingMinimumLubricantFilmThickness

    @property
    def micropitting_specific_lubricant_film_thickness(self) -> 'float':
        '''float: 'MicropittingSpecificLubricantFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingSpecificLubricantFilmThickness

    @property
    def micropitting_safety_factor(self) -> 'float':
        '''float: 'MicropittingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingSafetyFactor

    @property
    def micropitting_flash_temperature(self) -> 'float':
        '''float: 'MicropittingFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingFlashTemperature

    @property
    def micropitting_contact_temperature(self) -> 'float':
        '''float: 'MicropittingContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingContactTemperature

    @property
    def sliding_power_loss(self) -> 'float':
        '''float: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingPowerLoss

    @property
    def scuffing_flash_temperature(self) -> 'float':
        '''float: 'ScuffingFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperature

    @property
    def scuffing_contact_temperature(self) -> 'float':
        '''float: 'ScuffingContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperature

    @property
    def scuffing_safety_factor(self) -> 'float':
        '''float: 'ScuffingSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactor

    @property
    def scuffing_flash_temperature_agma925a03(self) -> 'float':
        '''float: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperatureAGMA925A03

    @property
    def scuffing_contact_temperature_agma925a03(self) -> 'float':
        '''float: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperatureAGMA925A03

    @property
    def scuffing_safety_factor_agma925a03(self) -> 'float':
        '''float: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorAGMA925A03

    @property
    def scuffing_flash_temperature_din399041987(self) -> 'float':
        '''float: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperatureDIN399041987

    @property
    def scuffing_contact_temperature_din399041987(self) -> 'float':
        '''float: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperatureDIN399041987

    @property
    def scuffing_safety_factor_din399041987(self) -> 'float':
        '''float: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorDIN399041987

    @property
    def gear_a_profile_measurement(self) -> '_952.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'GearAProfileMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_952.CylindricalGearProfileMeasurement)(self.wrapped.GearAProfileMeasurement) if self.wrapped.GearAProfileMeasurement else None

    @property
    def gear_b_profile_measurement(self) -> '_952.CylindricalGearProfileMeasurement':
        '''CylindricalGearProfileMeasurement: 'GearBProfileMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_952.CylindricalGearProfileMeasurement)(self.wrapped.GearBProfileMeasurement) if self.wrapped.GearBProfileMeasurement else None
