'''_3577.py

BoltedJointCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2117
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3444
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3655
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'BoltedJointCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundStabilityAnalysis',)


class BoltedJointCompoundStabilityAnalysis(_3655.SpecialisedAssemblyCompoundStabilityAnalysis):
    '''BoltedJointCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2117.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2117.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3444.BoltedJointStabilityAnalysis]':
        '''List[BoltedJointStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3444.BoltedJointStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3444.BoltedJointStabilityAnalysis]':
        '''List[BoltedJointStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3444.BoltedJointStabilityAnalysis))
        return value
