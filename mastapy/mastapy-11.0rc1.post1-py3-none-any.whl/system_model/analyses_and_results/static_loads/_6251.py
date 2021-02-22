'''_6251.py

SpringDamperConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets.couplings import _1958
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6155
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionLoadCase',)


class SpringDamperConnectionLoadCase(_6155.CouplingConnectionLoadCase):
    '''SpringDamperConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1958.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1958.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
