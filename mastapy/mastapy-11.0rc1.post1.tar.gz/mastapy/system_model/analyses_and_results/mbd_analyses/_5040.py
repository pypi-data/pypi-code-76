'''_5040.py

BeltConnectionMultibodyDynamicsAnalysis
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _67
from mastapy.system_model.connections_and_sockets import _1944, _1949
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6452, _6485
from mastapy.system_model.analyses_and_results.mbd_analyses import _5102
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BeltConnectionMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionMultibodyDynamicsAnalysis',)


class BeltConnectionMultibodyDynamicsAnalysis(_5102.InterMountableComponentConnectionMultibodyDynamicsAnalysis):
    '''BeltConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def extension(self) -> 'float':
        '''float: 'Extension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Extension

    @property
    def tension(self) -> 'float':
        '''float: 'Tension' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Tension

    @property
    def loading_status(self) -> '_67.LoadingStatus':
        '''LoadingStatus: 'LoadingStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.LoadingStatus)
        return constructor.new(_67.LoadingStatus)(value) if value else None

    @property
    def connection_design(self) -> '_1944.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6452.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6452.BeltConnectionLoadCase.TYPE not in self.wrapped.ConnectionLoadCase.__class__.__mro__:
            raise CastException('Failed to cast connection_load_case to BeltConnectionLoadCase. Expected: {}.'.format(self.wrapped.ConnectionLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionLoadCase.__class__)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
