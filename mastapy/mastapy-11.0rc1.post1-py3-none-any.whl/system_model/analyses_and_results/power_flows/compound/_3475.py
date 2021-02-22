'''_3475.py

MeasurementComponentCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2063
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3351
from mastapy.system_model.analyses_and_results.power_flows.compound import _3519
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'MeasurementComponentCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundPowerFlow',)


class MeasurementComponentCompoundPowerFlow(_3519.VirtualComponentCompoundPowerFlow):
    '''MeasurementComponentCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2063.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3351.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3351.MeasurementComponentPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3351.MeasurementComponentPowerFlow]':
        '''List[MeasurementComponentPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3351.MeasurementComponentPowerFlow))
        return value
