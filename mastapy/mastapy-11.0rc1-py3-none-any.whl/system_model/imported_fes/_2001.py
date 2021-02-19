'''_2001.py

ImportedFEPlanetBasedLink
'''


from mastapy.system_model.imported_fes import _1998
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_PLANET_BASED_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEPlanetBasedLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEPlanetBasedLink',)


class ImportedFEPlanetBasedLink(_1998.ImportedFEMultiNodeLink):
    '''ImportedFEPlanetBasedLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_PLANET_BASED_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEPlanetBasedLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
