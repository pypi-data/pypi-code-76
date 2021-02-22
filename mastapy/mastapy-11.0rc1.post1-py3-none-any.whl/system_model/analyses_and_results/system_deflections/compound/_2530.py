'''_2530.py

BevelGearMeshCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2518
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BevelGearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMeshCompoundSystemDeflection',)


class BevelGearMeshCompoundSystemDeflection(_2518.AGMAGleasonConicalGearMeshCompoundSystemDeflection):
    '''BevelGearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
