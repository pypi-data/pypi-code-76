'''_3482.py

PlanetaryConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3358
from mastapy.system_model.analyses_and_results.power_flows.compound import _3494
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetaryConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundPowerFlow',)


class PlanetaryConnectionCompoundPowerFlow(_3494.ShaftToMountableComponentConnectionCompoundPowerFlow):
    '''PlanetaryConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1904.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1904.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3358.PlanetaryConnectionPowerFlow]':
        '''List[PlanetaryConnectionPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3358.PlanetaryConnectionPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3358.PlanetaryConnectionPowerFlow]':
        '''List[PlanetaryConnectionPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3358.PlanetaryConnectionPowerFlow))
        return value
