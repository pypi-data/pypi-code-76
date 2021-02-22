'''_1512.py

CustomLineChart
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.utility.report import _1285
from mastapy._internal.python_net import python_net_import

_CUSTOM_LINE_CHART = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'CustomLineChart')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomLineChart',)


class CustomLineChart(_1285.CustomReportChart):
    '''CustomLineChart

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_LINE_CHART

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomLineChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def x_values(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'XValues' is the original name of this property.'''

        return self.wrapped.XValues

    @x_values.setter
    def x_values(self, value: 'Callable[..., None]'):
        value = value if value else None
        self.wrapped.XValues = value

    @property
    def y_values(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'YValues' is the original name of this property.'''

        return self.wrapped.YValues

    @y_values.setter
    def y_values(self, value: 'Callable[..., None]'):
        value = value if value else None
        self.wrapped.YValues = value
