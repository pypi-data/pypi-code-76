'''_2403.py

AGMAGleasonConicalGearMeshCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2431
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'AGMAGleasonConicalGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundSystemDeflection',)


class AGMAGleasonConicalGearMeshCompoundSystemDeflection(_2431.ConicalGearMeshCompoundSystemDeflection):
    '''AGMAGleasonConicalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
