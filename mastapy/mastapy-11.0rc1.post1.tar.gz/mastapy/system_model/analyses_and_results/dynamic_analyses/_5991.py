'''_5991.py

OilSealDynamicAnalysis
'''


from mastapy.system_model.part_model import _2139
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6555
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5948
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'OilSealDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealDynamicAnalysis',)


class OilSealDynamicAnalysis(_5948.ConnectorDynamicAnalysis):
    '''OilSealDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6555.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6555.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
