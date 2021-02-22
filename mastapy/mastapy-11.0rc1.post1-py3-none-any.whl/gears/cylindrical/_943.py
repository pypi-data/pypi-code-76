'''_943.py

CylindricalGearLTCAContactChartDataAsTextFile
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.cylindrical import _945
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'CylindricalGearLTCAContactChartDataAsTextFile')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLTCAContactChartDataAsTextFile',)


class CylindricalGearLTCAContactChartDataAsTextFile(_945.GearLTCAContactChartDataAsTextFile):
    '''CylindricalGearLTCAContactChartDataAsTextFile

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearLTCAContactChartDataAsTextFile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pressure_velocity_pv(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PressureVelocityPV

    @property
    def sliding_velocity(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingVelocity

    @property
    def minimum_film_thickness_isotr1514412014(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MinimumFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumFilmThicknessISOTR1514412014

    @property
    def specific_film_thickness_isotr1514412014(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SpecificFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpecificFilmThicknessISOTR1514412014

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingSafetyFactorISOTR1514412014

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingFlashTemperatureISOTR1514412014

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MicropittingContactTemperatureISOTR1514412014

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfFrictionBenedictAndKelley

    @property
    def sliding_power_loss(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SlidingPowerLoss

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperatureISOTR1398912000

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperatureISOTR1398912000

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorISOTR1398912000

    @property
    def scuffing_flash_temperature_agma925a03(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperatureAGMA925A03

    @property
    def scuffing_contact_temperature_agma925a03(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperatureAGMA925A03

    @property
    def scuffing_safety_factor_agma925a03(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorAGMA925A03

    @property
    def scuffing_flash_temperature_din399041987(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingFlashTemperatureDIN399041987

    @property
    def scuffing_contact_temperature_din399041987(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingContactTemperatureDIN399041987

    @property
    def scuffing_safety_factor_din399041987(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ScuffingSafetyFactorDIN399041987

    @property
    def gap_between_unloaded_flanks_transverse(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GapBetweenUnloadedFlanksTransverse
