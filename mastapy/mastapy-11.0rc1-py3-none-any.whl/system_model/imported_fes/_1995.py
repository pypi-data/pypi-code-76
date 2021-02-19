'''_1995.py

ImportedFEGearWithDuplicatedMeshesLink
'''


from mastapy.system_model.imported_fes import _2001
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_GEAR_WITH_DUPLICATED_MESHES_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEGearWithDuplicatedMeshesLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEGearWithDuplicatedMeshesLink',)


class ImportedFEGearWithDuplicatedMeshesLink(_2001.ImportedFEPlanetBasedLink):
    '''ImportedFEGearWithDuplicatedMeshesLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_GEAR_WITH_DUPLICATED_MESHES_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEGearWithDuplicatedMeshesLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
