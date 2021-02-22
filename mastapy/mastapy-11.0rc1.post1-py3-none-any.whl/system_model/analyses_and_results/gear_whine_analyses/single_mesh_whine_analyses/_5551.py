'''_5551.py

OilSealSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2066
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6223
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5512
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'OilSealSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSingleMeshWhineAnalysis',)


class OilSealSingleMeshWhineAnalysis(_5512.ConnectorSingleMeshWhineAnalysis):
    '''OilSealSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2066.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6223.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6223.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
