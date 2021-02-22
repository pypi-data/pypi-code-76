'''_2573.py

GearMeshCompoundSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2579
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'GearMeshCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundSystemDeflection',)


class GearMeshCompoundSystemDeflection(_2579.InterMountableComponentConnectionCompoundSystemDeflection):
    '''GearMeshCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
