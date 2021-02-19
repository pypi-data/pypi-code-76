'''_2002.py

ImportedFEPlanetCarrierLink
'''


from mastapy.system_model.imported_fes import _2001
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_PLANET_CARRIER_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEPlanetCarrierLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEPlanetCarrierLink',)


class ImportedFEPlanetCarrierLink(_2001.ImportedFEPlanetBasedLink):
    '''ImportedFEPlanetCarrierLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_PLANET_CARRIER_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEPlanetCarrierLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
