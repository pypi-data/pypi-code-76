'''_3676.py

TorqueConverterPumpCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3546
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3596
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'TorqueConverterPumpCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundStabilityAnalysis',)


class TorqueConverterPumpCompoundStabilityAnalysis(_3596.CouplingHalfCompoundStabilityAnalysis):
    '''TorqueConverterPumpCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2279.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2279.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3546.TorqueConverterPumpStabilityAnalysis]':
        '''List[TorqueConverterPumpStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3546.TorqueConverterPumpStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3546.TorqueConverterPumpStabilityAnalysis]':
        '''List[TorqueConverterPumpStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3546.TorqueConverterPumpStabilityAnalysis))
        return value
