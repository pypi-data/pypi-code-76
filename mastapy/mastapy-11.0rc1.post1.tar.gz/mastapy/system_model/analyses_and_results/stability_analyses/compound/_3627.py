'''_3627.py

KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1995
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3495
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3624
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis',)


class KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis(_3624.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1995.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1995.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1995.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1995.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3495.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3495.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis))
        return value

    @property
    def connection_stability_analysis_load_cases(self) -> 'List[_3495.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]: 'ConnectionStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionStabilityAnalysisLoadCases, constructor.new(_3495.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis))
        return value
