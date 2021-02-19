'''_5289.py

GroupOfTimeSeriesLoadCases
'''


from typing import List

from mastapy.system_model.analyses_and_results.static_loads import _6570
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import _5282
from mastapy._internal.python_net import python_net_import

_GROUP_OF_TIME_SERIES_LOAD_CASES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'GroupOfTimeSeriesLoadCases')


__docformat__ = 'restructuredtext en'
__all__ = ('GroupOfTimeSeriesLoadCases',)


class GroupOfTimeSeriesLoadCases(_5282.AbstractLoadCaseGroup):
    '''GroupOfTimeSeriesLoadCases

    This is a mastapy class.
    '''

    TYPE = _GROUP_OF_TIME_SERIES_LOAD_CASES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GroupOfTimeSeriesLoadCases.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_cases(self) -> 'List[_6570.TimeSeriesLoadCase]':
        '''List[TimeSeriesLoadCase]: 'LoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCases, constructor.new(_6570.TimeSeriesLoadCase))
        return value

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()
