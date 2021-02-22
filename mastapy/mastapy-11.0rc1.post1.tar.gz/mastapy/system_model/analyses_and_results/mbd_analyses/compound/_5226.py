'''_5226.py

CycloidalDiscCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5077
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5182
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CycloidalDiscCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCompoundMultibodyDynamicsAnalysis',)


class CycloidalDiscCompoundMultibodyDynamicsAnalysis(_5182.AbstractShaftCompoundMultibodyDynamicsAnalysis):
    '''CycloidalDiscCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5077.CycloidalDiscMultibodyDynamicsAnalysis]':
        '''List[CycloidalDiscMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5077.CycloidalDiscMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5077.CycloidalDiscMultibodyDynamicsAnalysis]':
        '''List[CycloidalDiscMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5077.CycloidalDiscMultibodyDynamicsAnalysis))
        return value
