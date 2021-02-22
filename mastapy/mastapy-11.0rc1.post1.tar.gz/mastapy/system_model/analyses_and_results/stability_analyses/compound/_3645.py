'''_3645.py

PulleyCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2261, _2258
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _3514
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3596
from mastapy._internal.python_net import python_net_import

_PULLEY_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'PulleyCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyCompoundStabilityAnalysis',)


class PulleyCompoundStabilityAnalysis(_3596.CouplingHalfCompoundStabilityAnalysis):
    '''PulleyCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3514.PulleyStabilityAnalysis]':
        '''List[PulleyStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3514.PulleyStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3514.PulleyStabilityAnalysis]':
        '''List[PulleyStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3514.PulleyStabilityAnalysis))
        return value
