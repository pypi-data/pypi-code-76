'''_4818.py

KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1995
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6545
from mastapy.system_model.analyses_and_results.system_deflections import _2433
from mastapy.system_model.analyses_and_results.modal_analyses import _4815
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis',)


class KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis(_4815.KlingelnbergCycloPalloidConicalGearMeshModalAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2433.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
