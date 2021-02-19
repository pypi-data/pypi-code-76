'''_2003.py

ImportedFEPointLoadLink
'''


from mastapy.system_model.imported_fes import _1998
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_POINT_LOAD_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFEPointLoadLink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEPointLoadLink',)


class ImportedFEPointLoadLink(_1998.ImportedFEMultiNodeLink):
    '''ImportedFEPointLoadLink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_POINT_LOAD_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEPointLoadLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
