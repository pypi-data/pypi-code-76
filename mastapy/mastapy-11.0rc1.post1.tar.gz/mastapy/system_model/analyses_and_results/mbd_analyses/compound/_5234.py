'''_5234.py

FaceGearCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5086
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5239
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'FaceGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundMultibodyDynamicsAnalysis',)


class FaceGearCompoundMultibodyDynamicsAnalysis(_5239.GearCompoundMultibodyDynamicsAnalysis):
    '''FaceGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundMultibodyDynamicsAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5086.FaceGearMultibodyDynamicsAnalysis]':
        '''List[FaceGearMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5086.FaceGearMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5086.FaceGearMultibodyDynamicsAnalysis]':
        '''List[FaceGearMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5086.FaceGearMultibodyDynamicsAnalysis))
        return value
