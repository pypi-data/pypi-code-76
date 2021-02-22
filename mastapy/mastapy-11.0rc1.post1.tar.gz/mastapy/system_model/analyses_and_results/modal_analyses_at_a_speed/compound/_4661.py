'''_4661.py

CycloidalAssemblyCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2239
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4532
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4716
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'CycloidalAssemblyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyCompoundModalAnalysisAtASpeed',)


class CycloidalAssemblyCompoundModalAnalysisAtASpeed(_4716.SpecialisedAssemblyCompoundModalAnalysisAtASpeed):
    '''CycloidalAssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2239.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2239.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4532.CycloidalAssemblyModalAnalysisAtASpeed]':
        '''List[CycloidalAssemblyModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4532.CycloidalAssemblyModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4532.CycloidalAssemblyModalAnalysisAtASpeed]':
        '''List[CycloidalAssemblyModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4532.CycloidalAssemblyModalAnalysisAtASpeed))
        return value
