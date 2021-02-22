'''_5884.py

ClutchConnectionDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _1950
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6137
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5900
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionDynamicAnalysis',)


class ClutchConnectionDynamicAnalysis(_5900.CouplingConnectionDynamicAnalysis):
    '''ClutchConnectionDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1950.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1950.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6137.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6137.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
