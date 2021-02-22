'''_6160.py

TorqueConverterConnectionCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2028
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6030
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6080
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'TorqueConverterConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundDynamicAnalysis',)


class TorqueConverterConnectionCompoundDynamicAnalysis(_6080.CouplingConnectionCompoundDynamicAnalysis):
    '''TorqueConverterConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_2028.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6030.TorqueConverterConnectionDynamicAnalysis]':
        '''List[TorqueConverterConnectionDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6030.TorqueConverterConnectionDynamicAnalysis))
        return value

    @property
    def connection_dynamic_analysis_load_cases(self) -> 'List[_6030.TorqueConverterConnectionDynamicAnalysis]':
        '''List[TorqueConverterConnectionDynamicAnalysis]: 'ConnectionDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDynamicAnalysisLoadCases, constructor.new(_6030.TorqueConverterConnectionDynamicAnalysis))
        return value
