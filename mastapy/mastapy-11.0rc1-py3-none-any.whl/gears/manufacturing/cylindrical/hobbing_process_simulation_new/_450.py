'''_450.py

HobbingProcessLeadCalculation
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _442, _448
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_LEAD_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessLeadCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessLeadCalculation',)


class HobbingProcessLeadCalculation(_448.HobbingProcessCalculation):
    '''HobbingProcessLeadCalculation

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_LEAD_CALCULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessLeadCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_lead_bands(self) -> 'int':
        '''int: 'NumberOfLeadBands' is the original name of this property.'''

        return self.wrapped.NumberOfLeadBands

    @number_of_lead_bands.setter
    def number_of_lead_bands(self, value: 'int'):
        self.wrapped.NumberOfLeadBands = int(value) if value else 0

    @property
    def radius_for_lead_modification_calculation(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RadiusForLeadModificationCalculation' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RadiusForLeadModificationCalculation) if self.wrapped.RadiusForLeadModificationCalculation else None

    @radius_for_lead_modification_calculation.setter
    def radius_for_lead_modification_calculation(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0, is_overridden)
        self.wrapped.RadiusForLeadModificationCalculation = value

    @property
    def right_flank(self) -> '_442.CalculateLeadDeviationAccuracy':
        '''CalculateLeadDeviationAccuracy: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_442.CalculateLeadDeviationAccuracy)(self.wrapped.RightFlank) if self.wrapped.RightFlank else None

    @property
    def left_flank(self) -> '_442.CalculateLeadDeviationAccuracy':
        '''CalculateLeadDeviationAccuracy: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_442.CalculateLeadDeviationAccuracy)(self.wrapped.LeftFlank) if self.wrapped.LeftFlank else None
