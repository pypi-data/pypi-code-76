'''_5360.py

CVTPulleyGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2310
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5424
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CVTPulleyGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyGearWhineAnalysis',)


class CVTPulleyGearWhineAnalysis(_5424.PulleyGearWhineAnalysis):
    '''CVTPulleyGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2310.CVTPulleySystemDeflection':
        '''CVTPulleySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2310.CVTPulleySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
