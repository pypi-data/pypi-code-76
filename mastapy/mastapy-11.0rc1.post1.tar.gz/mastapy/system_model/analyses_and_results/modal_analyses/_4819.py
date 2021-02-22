'''_4819.py

KlingelnbergCycloPalloidHypoidGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2209
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6544
from mastapy.system_model.analyses_and_results.system_deflections import _2435
from mastapy.system_model.analyses_and_results.modal_analyses import _4816
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'KlingelnbergCycloPalloidHypoidGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearModalAnalysis',)


class KlingelnbergCycloPalloidHypoidGearModalAnalysis(_4816.KlingelnbergCycloPalloidConicalGearModalAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2209.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2209.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6544.KlingelnbergCycloPalloidHypoidGearLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6544.KlingelnbergCycloPalloidHypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2435.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2435.KlingelnbergCycloPalloidHypoidGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
