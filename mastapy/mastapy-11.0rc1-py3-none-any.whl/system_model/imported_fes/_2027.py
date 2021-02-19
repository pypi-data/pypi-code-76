'''_2027.py

ShaftHubConnectionFELink
'''


from mastapy.system_model.imported_fes import _1997
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ShaftHubConnectionFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionFELink',)


class ShaftHubConnectionFELink(_1997.ImportedFEMultiNodeConnectorLink):
    '''ShaftHubConnectionFELink

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_FE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
