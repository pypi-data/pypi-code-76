'''_3517.py

TorqueConverterTurbineCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2204
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3396
from mastapy.system_model.analyses_and_results.power_flows.compound import _3442
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterTurbineCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundPowerFlow',)


class TorqueConverterTurbineCompoundPowerFlow(_3442.CouplingHalfCompoundPowerFlow):
    '''TorqueConverterTurbineCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2204.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2204.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3396.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3396.TorqueConverterTurbinePowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3396.TorqueConverterTurbinePowerFlow]':
        '''List[TorqueConverterTurbinePowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3396.TorqueConverterTurbinePowerFlow))
        return value
