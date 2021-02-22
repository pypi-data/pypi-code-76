'''_2582.py

KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2547
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection',)


class KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection(_2547.ConicalGearSetCompoundSystemDeflection):
    '''KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
