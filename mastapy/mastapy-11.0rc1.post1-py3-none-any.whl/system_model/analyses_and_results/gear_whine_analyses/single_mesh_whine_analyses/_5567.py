'''_5567.py

ShaftSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2081
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6244
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5479
from mastapy._internal.python_net import python_net_import

_SHAFT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ShaftSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSingleMeshWhineAnalysis',)


class ShaftSingleMeshWhineAnalysis(_5479.AbstractShaftOrHousingSingleMeshWhineAnalysis):
    '''ShaftSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2081.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6244.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6244.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftSingleMeshWhineAnalysis]':
        '''List[ShaftSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftSingleMeshWhineAnalysis))
        return value
