'''_5894.py

TorqueConverterTurbineCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2281
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5737
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5813
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'TorqueConverterTurbineCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundHarmonicAnalysis',)


class TorqueConverterTurbineCompoundHarmonicAnalysis(_5813.CouplingHalfCompoundHarmonicAnalysis):
    '''TorqueConverterTurbineCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2281.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5737.TorqueConverterTurbineHarmonicAnalysis]':
        '''List[TorqueConverterTurbineHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5737.TorqueConverterTurbineHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5737.TorqueConverterTurbineHarmonicAnalysis]':
        '''List[TorqueConverterTurbineHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5737.TorqueConverterTurbineHarmonicAnalysis))
        return value
