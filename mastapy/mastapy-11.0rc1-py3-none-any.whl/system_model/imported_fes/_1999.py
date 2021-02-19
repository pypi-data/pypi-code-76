'''_1999.py

ImportedFENodeLink
'''


from mastapy.system_model.imported_fes import _1963
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_NODE_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFENodeLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFENodeLink',)


class ImportedFENodeLink(_1963.ImportedFELink):
    '''ImportedFENodeLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_NODE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFENodeLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
