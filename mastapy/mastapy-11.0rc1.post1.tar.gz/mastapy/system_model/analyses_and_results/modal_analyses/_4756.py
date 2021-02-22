'''_4756.py

BeltConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1944, _1949
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6452, _6485
from mastapy.system_model.analyses_and_results.system_deflections import _2363, _2396
from mastapy.system_model.analyses_and_results.modal_analyses import _4814
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BeltConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionModalAnalysis',)


class BeltConnectionModalAnalysis(_4814.InterMountableComponentConnectionModalAnalysis):
    '''BeltConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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

    @property
    def system_deflection_results(self) -> '_2363.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2363.BeltConnectionSystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
