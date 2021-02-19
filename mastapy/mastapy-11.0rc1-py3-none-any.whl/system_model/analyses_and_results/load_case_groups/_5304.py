'''_5304.py

DutyCycle
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import _5308, _5300
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6298
from mastapy.system_model.analyses_and_results.static_loads import _6254
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'DutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycle',)


class DutyCycle(_5300.AbstractStaticLoadCaseGroup):
    '''DutyCycle

    This is a mastapy class.
    '''

    TYPE = _DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def convert_to_condensed_parametric_study_tool_duty_cycle(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'ConvertToCondensedParametricStudyToolDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConvertToCondensedParametricStudyToolDutyCycle

    @property
    def duty_cycle_design_states(self) -> 'List[_5308.SubGroupInSingleDesignState]':
        '''List[SubGroupInSingleDesignState]: 'DutyCycleDesignStates' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DutyCycleDesignStates, constructor.new(_5308.SubGroupInSingleDesignState))
        return value

    @property
    def time_series_importer(self) -> '_6298.TimeSeriesImporter':
        '''TimeSeriesImporter: 'TimeSeriesImporter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6298.TimeSeriesImporter)(self.wrapped.TimeSeriesImporter) if self.wrapped.TimeSeriesImporter else None

    def add_static_load(self, static_load: '_6254.StaticLoadCase'):
        ''' 'AddStaticLoad' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        '''

        self.wrapped.AddStaticLoad(static_load.wrapped if static_load else None)

    def remove_static_load(self, static_load: '_6254.StaticLoadCase'):
        ''' 'RemoveStaticLoad' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
        '''

        self.wrapped.RemoveStaticLoad(static_load.wrapped if static_load else None)

    def remove_design_state_sub_group(self, sub_group: '_5308.SubGroupInSingleDesignState'):
        ''' 'RemoveDesignStateSubGroup' is the original name of this method.

        Args:
            sub_group (mastapy.system_model.analyses_and_results.load_case_groups.SubGroupInSingleDesignState)
        '''

        self.wrapped.RemoveDesignStateSubGroup(sub_group.wrapped if sub_group else None)

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()
