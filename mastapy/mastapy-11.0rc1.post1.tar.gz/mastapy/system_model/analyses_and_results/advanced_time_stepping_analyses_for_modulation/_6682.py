'''_6682.py

CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets import _1949
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6650
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation',)


class CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation(_6650.BeltConnectionAdvancedTimeSteppingAnalysisForModulation):
    '''CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1949.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1949.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
