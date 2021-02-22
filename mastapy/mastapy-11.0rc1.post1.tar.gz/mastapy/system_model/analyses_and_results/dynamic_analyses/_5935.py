'''_5935.py

ClutchHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2250
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6465
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5951
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ClutchHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfDynamicAnalysis',)


class ClutchHalfDynamicAnalysis(_5951.CouplingHalfDynamicAnalysis):
    '''ClutchHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2250.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2250.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6465.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6465.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
