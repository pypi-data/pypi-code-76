'''_7041.py

AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection
'''


from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7069
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection',)


class AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection(_7069.ConicalGearMeshCompoundAdvancedSystemDeflection):
    '''AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
