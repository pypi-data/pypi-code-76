'''_6761.py

TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model.couplings import _2279
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6606
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6680
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation',)


class TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation(_6680.CouplingHalfAdvancedTimeSteppingAnalysisForModulation):
    '''TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def component_load_case(self) -> '_6606.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6606.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
