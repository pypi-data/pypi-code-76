'''_1320.py

CustomRow
'''


from mastapy._internal import constructor
from mastapy.utility.report import _1315
from mastapy._internal.python_net import python_net_import

_CUSTOM_ROW = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomRow')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomRow',)


class CustomRow(_1315.CustomReportPropertyItem):
    '''CustomRow

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_read_only(self) -> 'bool':
        '''bool: 'IsReadOnly' is the original name of this property.'''

        return self.wrapped.IsReadOnly

    @is_read_only.setter
    def is_read_only(self, value: 'bool'):
        self.wrapped.IsReadOnly = bool(value) if value else False

    @property
    def calculate_sum_of_values(self) -> 'bool':
        '''bool: 'CalculateSumOfValues' is the original name of this property.'''

        return self.wrapped.CalculateSumOfValues

    @calculate_sum_of_values.setter
    def calculate_sum_of_values(self, value: 'bool'):
        self.wrapped.CalculateSumOfValues = bool(value) if value else False

    @property
    def show_maximum_of_values(self) -> 'bool':
        '''bool: 'ShowMaximumOfValues' is the original name of this property.'''

        return self.wrapped.ShowMaximumOfValues

    @show_maximum_of_values.setter
    def show_maximum_of_values(self, value: 'bool'):
        self.wrapped.ShowMaximumOfValues = bool(value) if value else False

    @property
    def show_minimum_of_values(self) -> 'bool':
        '''bool: 'ShowMinimumOfValues' is the original name of this property.'''

        return self.wrapped.ShowMinimumOfValues

    @show_minimum_of_values.setter
    def show_minimum_of_values(self, value: 'bool'):
        self.wrapped.ShowMinimumOfValues = bool(value) if value else False

    @property
    def show_maximum_of_absolute_values(self) -> 'bool':
        '''bool: 'ShowMaximumOfAbsoluteValues' is the original name of this property.'''

        return self.wrapped.ShowMaximumOfAbsoluteValues

    @show_maximum_of_absolute_values.setter
    def show_maximum_of_absolute_values(self, value: 'bool'):
        self.wrapped.ShowMaximumOfAbsoluteValues = bool(value) if value else False

    @property
    def count_values(self) -> 'bool':
        '''bool: 'CountValues' is the original name of this property.'''

        return self.wrapped.CountValues

    @count_values.setter
    def count_values(self, value: 'bool'):
        self.wrapped.CountValues = bool(value) if value else False

    @property
    def override_property_name(self) -> 'bool':
        '''bool: 'OverridePropertyName' is the original name of this property.'''

        return self.wrapped.OverridePropertyName

    @override_property_name.setter
    def override_property_name(self, value: 'bool'):
        self.wrapped.OverridePropertyName = bool(value) if value else False

    @property
    def overridden_property_name(self) -> 'str':
        '''str: 'OverriddenPropertyName' is the original name of this property.'''

        return self.wrapped.OverriddenPropertyName

    @overridden_property_name.setter
    def overridden_property_name(self, value: 'str'):
        self.wrapped.OverriddenPropertyName = str(value) if value else None

    @property
    def is_minor_value(self) -> 'bool':
        '''bool: 'IsMinorValue' is the original name of this property.'''

        return self.wrapped.IsMinorValue

    @is_minor_value.setter
    def is_minor_value(self, value: 'bool'):
        self.wrapped.IsMinorValue = bool(value) if value else False
