'''_5267.py

PointLoadCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2144
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5126
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5303
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'PointLoadCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundMultibodyDynamicsAnalysis',)


class PointLoadCompoundMultibodyDynamicsAnalysis(_5303.VirtualComponentCompoundMultibodyDynamicsAnalysis):
    '''PointLoadCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2144.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2144.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5126.PointLoadMultibodyDynamicsAnalysis]':
        '''List[PointLoadMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5126.PointLoadMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5126.PointLoadMultibodyDynamicsAnalysis]':
        '''List[PointLoadMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5126.PointLoadMultibodyDynamicsAnalysis))
        return value
