'''_2433.py

KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _1995
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6545
from mastapy.system_model.analyses_and_results.power_flows import _3762
from mastapy.gears.rating.klingelnberg_hypoid import _368
from mastapy.system_model.analyses_and_results.system_deflections import _2430
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection(_2430.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1995.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1995.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6545.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6545.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3762.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidHypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3762.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_368.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.KlingelnbergCycloPalloidHypoidGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_368.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.KlingelnbergCycloPalloidHypoidGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
