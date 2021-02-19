'''_1511.py

CustomTableAndChart
'''


from mastapy.math_utility import _1060
from mastapy._internal import constructor
from mastapy.math_utility.measured_ranges import _1124
from mastapy._internal.cast_exception import CastException
from mastapy.utility.report import _1307
from mastapy._internal.python_net import python_net_import

_CUSTOM_TABLE_AND_CHART = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'CustomTableAndChart')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomTableAndChart',)


class CustomTableAndChart(_1307.CustomTable):
    '''CustomTableAndChart

    This is a mastapy class.
    '''

    TYPE = _CUSTOM_TABLE_AND_CHART

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CustomTableAndChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def primary_axis_range(self) -> '_1060.Range':
        '''Range: 'PrimaryAxisRange' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1060.Range.TYPE not in self.wrapped.PrimaryAxisRange.__class__.__mro__:
            raise CastException('Failed to cast primary_axis_range to Range. Expected: {}.'.format(self.wrapped.PrimaryAxisRange.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PrimaryAxisRange.__class__)(self.wrapped.PrimaryAxisRange) if self.wrapped.PrimaryAxisRange else None
