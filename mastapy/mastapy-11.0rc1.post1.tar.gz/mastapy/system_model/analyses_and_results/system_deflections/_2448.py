'''_2448.py

PartToPartShearCouplingConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _2024
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6558
from mastapy.system_model.analyses_and_results.power_flows import _3773
from mastapy.system_model.analyses_and_results.system_deflections import _2393
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PartToPartShearCouplingConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionSystemDeflection',)


class PartToPartShearCouplingConnectionSystemDeflection(_2393.CouplingConnectionSystemDeflection):
    '''PartToPartShearCouplingConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2024.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2024.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6558.PartToPartShearCouplingConnectionLoadCase':
        '''PartToPartShearCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6558.PartToPartShearCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3773.PartToPartShearCouplingConnectionPowerFlow':
        '''PartToPartShearCouplingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3773.PartToPartShearCouplingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
