'''_2096.py

MultiAngleConnectionFELink
'''


from mastapy.system_model.fe.links import _2098
from mastapy._internal.python_net import python_net_import

_MULTI_ANGLE_CONNECTION_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'MultiAngleConnectionFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiAngleConnectionFELink',)


class MultiAngleConnectionFELink(_2098.MultiNodeFELink):
    '''MultiAngleConnectionFELink

    This is a mastapy class.
    '''

    TYPE = _MULTI_ANGLE_CONNECTION_FE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MultiAngleConnectionFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
