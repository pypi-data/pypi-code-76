'''_5203.py

ClutchConnectionCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5052
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5219
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ClutchConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundMultibodyDynamicsAnalysis',)


class ClutchConnectionCompoundMultibodyDynamicsAnalysis(_5219.CouplingConnectionCompoundMultibodyDynamicsAnalysis):
    '''ClutchConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5052.ClutchConnectionMultibodyDynamicsAnalysis]':
        '''List[ClutchConnectionMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5052.ClutchConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def connection_multibody_dynamics_analysis_load_cases(self) -> 'List[_5052.ClutchConnectionMultibodyDynamicsAnalysis]':
        '''List[ClutchConnectionMultibodyDynamicsAnalysis]: 'ConnectionMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionMultibodyDynamicsAnalysisLoadCases, constructor.new(_5052.ClutchConnectionMultibodyDynamicsAnalysis))
        return value
