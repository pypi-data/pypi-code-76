'''_3519.py

RollingRingStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2267
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6576
from mastapy.system_model.analyses_and_results.stability_analyses import _3463
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RollingRingStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingStabilityAnalysis',)


class RollingRingStabilityAnalysis(_3463.CouplingHalfStabilityAnalysis):
    '''RollingRingStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2267.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6576.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6576.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingStabilityAnalysis]':
        '''List[RollingRingStabilityAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingStabilityAnalysis))
        return value
