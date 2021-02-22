'''_5804.py

MassDiscCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5410
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5849
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'MassDiscCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundGearWhineAnalysis',)


class MassDiscCompoundGearWhineAnalysis(_5849.VirtualComponentCompoundGearWhineAnalysis):
    '''MassDiscCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2062.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5410.MassDiscGearWhineAnalysis]':
        '''List[MassDiscGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5410.MassDiscGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5410.MassDiscGearWhineAnalysis]':
        '''List[MassDiscGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5410.MassDiscGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundGearWhineAnalysis]':
        '''List[MassDiscCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundGearWhineAnalysis))
        return value
