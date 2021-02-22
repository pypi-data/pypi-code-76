'''_2581.py

KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2546
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection',)


class KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection(_2546.ConicalGearMeshCompoundSystemDeflection):
    '''KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
