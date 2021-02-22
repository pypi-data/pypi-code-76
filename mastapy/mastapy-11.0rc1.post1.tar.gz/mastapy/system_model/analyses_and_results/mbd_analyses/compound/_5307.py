'''_5307.py

ZerolBevelGearCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2224
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5173
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5197
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ZerolBevelGearCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearCompoundMultibodyDynamicsAnalysis',)


class ZerolBevelGearCompoundMultibodyDynamicsAnalysis(_5197.BevelGearCompoundMultibodyDynamicsAnalysis):
    '''ZerolBevelGearCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2224.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5173.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5173.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5173.ZerolBevelGearMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5173.ZerolBevelGearMultibodyDynamicsAnalysis))
        return value
