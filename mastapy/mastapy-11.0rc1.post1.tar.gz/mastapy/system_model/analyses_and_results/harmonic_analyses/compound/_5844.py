'''_5844.py

KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1995
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5684
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5841
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis(_5841.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5684.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value
