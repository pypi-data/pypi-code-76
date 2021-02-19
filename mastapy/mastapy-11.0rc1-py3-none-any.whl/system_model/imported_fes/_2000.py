'''_2000.py

ImportedFEPlanetaryConnectorMultiNodeLink
'''


from mastapy.system_model.imported_fes import _2001
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_PLANETARY_CONNECTOR_MULTI_NODE_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEPlanetaryConnectorMultiNodeLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEPlanetaryConnectorMultiNodeLink',)


class ImportedFEPlanetaryConnectorMultiNodeLink(_2001.ImportedFEPlanetBasedLink):
    '''ImportedFEPlanetaryConnectorMultiNodeLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_PLANETARY_CONNECTOR_MULTI_NODE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEPlanetaryConnectorMultiNodeLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
