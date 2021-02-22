'''_5688.py

ShaftCompoundSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2081
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5567
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5602
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'ShaftCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundSingleMeshWhineAnalysis',)


class ShaftCompoundSingleMeshWhineAnalysis(_5602.AbstractShaftOrHousingCompoundSingleMeshWhineAnalysis):
    '''ShaftCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2081.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5567.ShaftSingleMeshWhineAnalysis]':
        '''List[ShaftSingleMeshWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5567.ShaftSingleMeshWhineAnalysis))
        return value

    @property
    def component_single_mesh_whine_analysis_load_cases(self) -> 'List[_5567.ShaftSingleMeshWhineAnalysis]':
        '''List[ShaftSingleMeshWhineAnalysis]: 'ComponentSingleMeshWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSingleMeshWhineAnalysisLoadCases, constructor.new(_5567.ShaftSingleMeshWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundSingleMeshWhineAnalysis]':
        '''List[ShaftCompoundSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundSingleMeshWhineAnalysis))
        return value
