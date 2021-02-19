'''_945.py

CylindricalGearLTCAContactCharts
'''


from mastapy.scripting import _6574
from mastapy._internal import constructor
from mastapy.gears.cylindrical import _947
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LTCA_CONTACT_CHARTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'CylindricalGearLTCAContactCharts')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLTCAContactCharts',)


class CylindricalGearLTCAContactCharts(_947.GearLTCAContactCharts):
    '''CylindricalGearLTCAContactCharts

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_LTCA_CONTACT_CHARTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearLTCAContactCharts.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pressure_velocity_pv(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.PressureVelocityPV) if self.wrapped.PressureVelocityPV else None

    @property
    def sliding_velocity(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.SlidingVelocity) if self.wrapped.SlidingVelocity else None

    @property
    def minimum_film_thickness_isotr1514412014(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'MinimumFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.MinimumFilmThicknessISOTR1514412014) if self.wrapped.MinimumFilmThicknessISOTR1514412014 else None

    @property
    def specific_film_thickness_isotr1514412014(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'SpecificFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.SpecificFilmThicknessISOTR1514412014) if self.wrapped.SpecificFilmThicknessISOTR1514412014 else None

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.MicropittingSafetyFactorISOTR1514412014) if self.wrapped.MicropittingSafetyFactorISOTR1514412014 else None

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.MicropittingFlashTemperatureISOTR1514412014) if self.wrapped.MicropittingFlashTemperatureISOTR1514412014 else None

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.MicropittingContactTemperatureISOTR1514412014) if self.wrapped.MicropittingContactTemperatureISOTR1514412014 else None

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.CoefficientOfFrictionBenedictAndKelley) if self.wrapped.CoefficientOfFrictionBenedictAndKelley else None

    @property
    def sliding_power_loss(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.SlidingPowerLoss) if self.wrapped.SlidingPowerLoss else None

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingFlashTemperatureISOTR1398912000) if self.wrapped.ScuffingFlashTemperatureISOTR1398912000 else None

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingContactTemperatureISOTR1398912000) if self.wrapped.ScuffingContactTemperatureISOTR1398912000 else None

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingSafetyFactorISOTR1398912000) if self.wrapped.ScuffingSafetyFactorISOTR1398912000 else None

    @property
    def scuffing_flash_temperature_agma925a03(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingFlashTemperatureAGMA925A03) if self.wrapped.ScuffingFlashTemperatureAGMA925A03 else None

    @property
    def scuffing_contact_temperature_agma925a03(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingContactTemperatureAGMA925A03) if self.wrapped.ScuffingContactTemperatureAGMA925A03 else None

    @property
    def scuffing_safety_factor_agma925a03(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingSafetyFactorAGMA925A03) if self.wrapped.ScuffingSafetyFactorAGMA925A03 else None

    @property
    def scuffing_flash_temperature_din399041987(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingFlashTemperatureDIN399041987) if self.wrapped.ScuffingFlashTemperatureDIN399041987 else None

    @property
    def scuffing_contact_temperature_din399041987(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingContactTemperatureDIN399041987) if self.wrapped.ScuffingContactTemperatureDIN399041987 else None

    @property
    def scuffing_safety_factor_din399041987(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.ScuffingSafetyFactorDIN399041987) if self.wrapped.ScuffingSafetyFactorDIN399041987 else None

    @property
    def gap_between_unloaded_flanks_transverse(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.GapBetweenUnloadedFlanksTransverse) if self.wrapped.GapBetweenUnloadedFlanksTransverse else None
