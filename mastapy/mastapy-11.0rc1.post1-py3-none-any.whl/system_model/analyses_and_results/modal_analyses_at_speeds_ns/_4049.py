'''_4049.py

BoltModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _2044
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6136
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4054
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'BoltModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysesAtSpeeds',)


class BoltModalAnalysesAtSpeeds(_4054.ComponentModalAnalysesAtSpeeds):
    '''BoltModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _BOLT_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2044.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6136.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6136.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
