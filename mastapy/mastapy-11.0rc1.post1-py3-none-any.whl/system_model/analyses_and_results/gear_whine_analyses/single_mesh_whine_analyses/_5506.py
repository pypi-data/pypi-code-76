'''_5506.py

ConceptGearSetSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6147
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5507, _5505, _5530
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ConceptGearSetSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSingleMeshWhineAnalysis',)


class ConceptGearSetSingleMeshWhineAnalysis(_5530.GearSetSingleMeshWhineAnalysis):
    '''ConceptGearSetSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2120.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6147.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6147.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_single_mesh_whine_analysis(self) -> 'List[_5507.ConceptGearSingleMeshWhineAnalysis]':
        '''List[ConceptGearSingleMeshWhineAnalysis]: 'ConceptGearsSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSingleMeshWhineAnalysis, constructor.new(_5507.ConceptGearSingleMeshWhineAnalysis))
        return value

    @property
    def concept_meshes_single_mesh_whine_analysis(self) -> 'List[_5505.ConceptGearMeshSingleMeshWhineAnalysis]':
        '''List[ConceptGearMeshSingleMeshWhineAnalysis]: 'ConceptMeshesSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSingleMeshWhineAnalysis, constructor.new(_5505.ConceptGearMeshSingleMeshWhineAnalysis))
        return value
