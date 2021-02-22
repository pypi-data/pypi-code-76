'''_5266.py

PlanetCarrierCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2142
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5125
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5258
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'PlanetCarrierCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundMultibodyDynamicsAnalysis',)


class PlanetCarrierCompoundMultibodyDynamicsAnalysis(_5258.MountableComponentCompoundMultibodyDynamicsAnalysis):
    '''PlanetCarrierCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5125.PlanetCarrierMultibodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5125.PlanetCarrierMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5125.PlanetCarrierMultibodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5125.PlanetCarrierMultibodyDynamicsAnalysis))
        return value
