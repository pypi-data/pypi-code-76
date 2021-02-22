'''_6975.py

KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1995
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6545
from mastapy.gears.rating.klingelnberg_hypoid import _368
from mastapy.system_model.analyses_and_results.system_deflections import _2433
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6972
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection(_6972.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection.TYPE'):
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
    def component_detailed_analysis(self) -> '_368.KlingelnbergCycloPalloidHypoidGearMeshRating':
        '''KlingelnbergCycloPalloidHypoidGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_368.KlingelnbergCycloPalloidHypoidGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection))
        return value
