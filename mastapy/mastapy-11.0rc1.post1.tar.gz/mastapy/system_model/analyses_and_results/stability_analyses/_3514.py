'''_3514.py

PulleyStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2261, _2258
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6569, _6487
from mastapy.system_model.analyses_and_results.stability_analyses import _3463
from mastapy._internal.python_net import python_net_import

_PULLEY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'PulleyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyStabilityAnalysis',)


class PulleyStabilityAnalysis(_3463.CouplingHalfStabilityAnalysis):
    '''PulleyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2261.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.Pulley.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6569.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6569.PulleyLoadCase.TYPE not in self.wrapped.ComponentLoadCase.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to PulleyLoadCase. Expected: {}.'.format(self.wrapped.ComponentLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentLoadCase.__class__)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
