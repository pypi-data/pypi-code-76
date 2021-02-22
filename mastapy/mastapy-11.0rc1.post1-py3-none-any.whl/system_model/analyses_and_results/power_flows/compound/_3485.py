'''_3485.py

PointLoadCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3361
from mastapy.system_model.analyses_and_results.power_flows.compound import _3519
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PointLoadCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundPowerFlow',)


class PointLoadCompoundPowerFlow(_3519.VirtualComponentCompoundPowerFlow):
    '''PointLoadCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2071.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3361.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3361.PointLoadPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3361.PointLoadPowerFlow]':
        '''List[PointLoadPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3361.PointLoadPowerFlow))
        return value
