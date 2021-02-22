'''_3416.py

BoltStabilityAnalysis
'''


from mastapy.system_model.part_model import _2091
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6430
from mastapy.system_model.analyses_and_results.stability_analyses import _3421
from mastapy._internal.python_net import python_net_import

_BOLT_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'BoltStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltStabilityAnalysis',)


class BoltStabilityAnalysis(_3421.ComponentStabilityAnalysis):
    '''BoltStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2091.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2091.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6430.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6430.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
