'''_2015.py

MultiAngleConnectionLink
'''


from mastapy.system_model.imported_fes import _1998
from mastapy._internal.python_net import python_net_import

_MULTI_ANGLE_CONNECTION_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'MultiAngleConnectionLink')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiAngleConnectionLink',)


class MultiAngleConnectionLink(_1998.ImportedFEMultiNodeLink):
    '''MultiAngleConnectionLink

    This is a mastapy class.
    '''

    TYPE = _MULTI_ANGLE_CONNECTION_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MultiAngleConnectionLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
