'''_7102.py

KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7068
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection(_7068.ConicalGearCompoundAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
