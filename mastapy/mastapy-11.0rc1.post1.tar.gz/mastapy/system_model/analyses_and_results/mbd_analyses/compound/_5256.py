'''_5256.py

MassDiscCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2135
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5112
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5303
from mastapy._internal.python_net import python_net_import

_MASS_DISC_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'MassDiscCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscCompoundMultibodyDynamicsAnalysis',)


class MassDiscCompoundMultibodyDynamicsAnalysis(_5303.VirtualComponentCompoundMultibodyDynamicsAnalysis):
    '''MassDiscCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MASS_DISC_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MassDiscCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5112.MassDiscMultibodyDynamicsAnalysis]':
        '''List[MassDiscMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5112.MassDiscMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5112.MassDiscMultibodyDynamicsAnalysis]':
        '''List[MassDiscMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5112.MassDiscMultibodyDynamicsAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[MassDiscCompoundMultibodyDynamicsAnalysis]':
        '''List[MassDiscCompoundMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(MassDiscCompoundMultibodyDynamicsAnalysis))
        return value
