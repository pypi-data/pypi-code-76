'''_3587.py

ConceptGearMeshCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3454
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3616
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConceptGearMeshCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshCompoundStabilityAnalysis',)


class ConceptGearMeshCompoundStabilityAnalysis(_3616.GearMeshCompoundStabilityAnalysis):
    '''ConceptGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearMeshCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1981.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3454.ConceptGearMeshStabilityAnalysis]':
        '''List[ConceptGearMeshStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3454.ConceptGearMeshStabilityAnalysis))
        return value

    @property
    def connection_stability_analysis_load_cases(self) -> 'List[_3454.ConceptGearMeshStabilityAnalysis]':
        '''List[ConceptGearMeshStabilityAnalysis]: 'ConnectionStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionStabilityAnalysisLoadCases, constructor.new(_3454.ConceptGearMeshStabilityAnalysis))
        return value
