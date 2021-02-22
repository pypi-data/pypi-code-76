'''_2026.py

RollingRingConnectionLink
'''


from mastapy.system_model.imported_fes import _2015
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'RollingRingConnectionLink')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionLink',)


class RollingRingConnectionLink(_2015.MultiAngleConnectionLink):
    '''RollingRingConnectionLink

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionLink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
