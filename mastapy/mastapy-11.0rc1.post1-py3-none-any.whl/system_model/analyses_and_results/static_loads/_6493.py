'''_6493.py

CylindricalGearManufactureError
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6521
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MANUFACTURE_ERROR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CylindricalGearManufactureError')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearManufactureError',)


class CylindricalGearManufactureError(_6521.GearManufactureError):
    '''CylindricalGearManufactureError

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MANUFACTURE_ERROR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearManufactureError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pitch_error_phase_shift_on_left_flank(self) -> 'float':
        '''float: 'PitchErrorPhaseShiftOnLeftFlank' is the original name of this property.'''

        return self.wrapped.PitchErrorPhaseShiftOnLeftFlank

    @pitch_error_phase_shift_on_left_flank.setter
    def pitch_error_phase_shift_on_left_flank(self, value: 'float'):
        self.wrapped.PitchErrorPhaseShiftOnLeftFlank = float(value) if value else 0.0

    @property
    def pitch_error_phase_shift_on_right_flank(self) -> 'float':
        '''float: 'PitchErrorPhaseShiftOnRightFlank' is the original name of this property.'''

        return self.wrapped.PitchErrorPhaseShiftOnRightFlank

    @pitch_error_phase_shift_on_right_flank.setter
    def pitch_error_phase_shift_on_right_flank(self, value: 'float'):
        self.wrapped.PitchErrorPhaseShiftOnRightFlank = float(value) if value else 0.0

    @property
    def runout_reference_angle(self) -> 'float':
        '''float: 'RunoutReferenceAngle' is the original name of this property.'''

        return self.wrapped.RunoutReferenceAngle

    @runout_reference_angle.setter
    def runout_reference_angle(self, value: 'float'):
        self.wrapped.RunoutReferenceAngle = float(value) if value else 0.0

    @property
    def runout(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Runout' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Runout) if self.wrapped.Runout else None

    @runout.setter
    def runout(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.Runout = value

    @property
    def extra_backlash(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ExtraBacklash' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ExtraBacklash) if self.wrapped.ExtraBacklash else None

    @extra_backlash.setter
    def extra_backlash(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ExtraBacklash = value

    @property
    def clocking_angle_error(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ClockingAngleError' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ClockingAngleError) if self.wrapped.ClockingAngleError else None

    @clocking_angle_error.setter
    def clocking_angle_error(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.ClockingAngleError = value

    @property
    def separation_on_left_flank(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SeparationOnLeftFlank' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SeparationOnLeftFlank) if self.wrapped.SeparationOnLeftFlank else None

    @separation_on_left_flank.setter
    def separation_on_left_flank(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SeparationOnLeftFlank = value

    @property
    def separation_on_right_flank(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SeparationOnRightFlank' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SeparationOnRightFlank) if self.wrapped.SeparationOnRightFlank else None

    @separation_on_right_flank.setter
    def separation_on_right_flank(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.SeparationOnRightFlank = value

    @property
    def pitch_error_measurement_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PitchErrorMeasurementDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PitchErrorMeasurementDiameter) if self.wrapped.PitchErrorMeasurementDiameter else None

    @pitch_error_measurement_diameter.setter
    def pitch_error_measurement_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.PitchErrorMeasurementDiameter = value
