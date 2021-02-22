'''_6663.py

ClutchConnectionAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets.couplings import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6464
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6679
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'ClutchConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionAdvancedTimeSteppingAnalysisForModulation',)


class ClutchConnectionAdvancedTimeSteppingAnalysisForModulation(_6679.CouplingConnectionAdvancedTimeSteppingAnalysisForModulation):
    '''ClutchConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2018.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6464.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6464.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
