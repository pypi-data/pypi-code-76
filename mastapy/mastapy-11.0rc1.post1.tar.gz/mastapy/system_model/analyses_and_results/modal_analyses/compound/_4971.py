'''_4971.py

KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2210
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4969, _4970, _4968
from mastapy.system_model.analyses_and_results.modal_analyses import _4820
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis(_4968.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2210.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_modal_analysis(self) -> 'List[_4969.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundModalAnalysis, constructor.new(_4969.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_modal_analysis(self) -> 'List[_4970.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundModalAnalysis, constructor.new(_4970.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4820.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4820.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_4820.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_4820.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value
