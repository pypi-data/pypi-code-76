'''_617.py

HobbingProcessProfileCalculation
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import _953
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _608, _612
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_PROFILE_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessProfileCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessProfileCalculation',)


class HobbingProcessProfileCalculation(_612.HobbingProcessCalculation):
    '''HobbingProcessProfileCalculation

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_PROFILE_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessProfileCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def result_z_plane(self) -> 'float':
        '''float: 'ResultZPlane' is the original name of this property.'''

        return self.wrapped.ResultZPlane

    @result_z_plane.setter
    def result_z_plane(self, value: 'float'):
        self.wrapped.ResultZPlane = float(value) if value else 0.0

    @property
    def number_of_profile_bands(self) -> 'int':
        '''int: 'NumberOfProfileBands' is the original name of this property.'''

        return self.wrapped.NumberOfProfileBands

    @number_of_profile_bands.setter
    def number_of_profile_bands(self, value: 'int'):
        self.wrapped.NumberOfProfileBands = int(value) if value else 0

    @property
    def chart_display_method(self) -> '_953.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'ChartDisplayMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ChartDisplayMethod)
        return constructor.new(_953.CylindricalGearProfileMeasurementType)(value) if value else None

    @chart_display_method.setter
    def chart_display_method(self, value: '_953.CylindricalGearProfileMeasurementType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartDisplayMethod = value

    @property
    def right_flank(self) -> '_608.CalculateProfileDeviationAccuracy':
        '''CalculateProfileDeviationAccuracy: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_608.CalculateProfileDeviationAccuracy)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def left_flank(self) -> '_608.CalculateProfileDeviationAccuracy':
        '''CalculateProfileDeviationAccuracy: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_608.CalculateProfileDeviationAccuracy)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None
