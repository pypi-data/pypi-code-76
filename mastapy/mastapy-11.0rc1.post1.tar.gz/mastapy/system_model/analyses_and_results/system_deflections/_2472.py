'''_2472.py

SpringDamperConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _2026
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6586
from mastapy.system_model.analyses_and_results.power_flows import _3797
from mastapy.system_model.analyses_and_results.system_deflections import _2393
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SpringDamperConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionSystemDeflection',)


class SpringDamperConnectionSystemDeflection(_2393.CouplingConnectionSystemDeflection):
    '''SpringDamperConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2026.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2026.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6586.SpringDamperConnectionLoadCase':
        '''SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6586.SpringDamperConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3797.SpringDamperConnectionPowerFlow':
        '''SpringDamperConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3797.SpringDamperConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
