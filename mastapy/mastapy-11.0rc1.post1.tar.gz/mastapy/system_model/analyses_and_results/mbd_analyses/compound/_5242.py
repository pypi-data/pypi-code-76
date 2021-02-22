'''_5242.py

GuideDxfModelCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5094
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5206
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'GuideDxfModelCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundMultibodyDynamicsAnalysis',)


class GuideDxfModelCompoundMultibodyDynamicsAnalysis(_5206.ComponentCompoundMultibodyDynamicsAnalysis):
    '''GuideDxfModelCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5094.GuideDxfModelMultibodyDynamicsAnalysis]':
        '''List[GuideDxfModelMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5094.GuideDxfModelMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5094.GuideDxfModelMultibodyDynamicsAnalysis]':
        '''List[GuideDxfModelMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5094.GuideDxfModelMultibodyDynamicsAnalysis))
        return value
