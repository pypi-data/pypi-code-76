'''_5300.py

TorqueConverterPumpCompoundMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5163
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5220
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'TorqueConverterPumpCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpCompoundMultibodyDynamicsAnalysis',)


class TorqueConverterPumpCompoundMultibodyDynamicsAnalysis(_5220.CouplingHalfCompoundMultibodyDynamicsAnalysis):
    '''TorqueConverterPumpCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpCompoundMultibodyDynamicsAnalysis.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_5163.TorqueConverterPumpMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterPumpMultibodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5163.TorqueConverterPumpMultibodyDynamicsAnalysis))
        return value

    @property
    def component_multibody_dynamics_analysis_load_cases(self) -> 'List[_5163.TorqueConverterPumpMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterPumpMultibodyDynamicsAnalysis]: 'ComponentMultibodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultibodyDynamicsAnalysisLoadCases, constructor.new(_5163.TorqueConverterPumpMultibodyDynamicsAnalysis))
        return value
