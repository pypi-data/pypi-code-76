'''_3610.py

FaceGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3481
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3615
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'FaceGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundStabilityAnalysis',)


class FaceGearCompoundStabilityAnalysis(_3615.GearCompoundStabilityAnalysis):
    '''FaceGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2199.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3481.FaceGearStabilityAnalysis]':
        '''List[FaceGearStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3481.FaceGearStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3481.FaceGearStabilityAnalysis]':
        '''List[FaceGearStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3481.FaceGearStabilityAnalysis))
        return value
