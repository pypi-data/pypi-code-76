'''_1499.py

CMSNodeGroup
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import _1475
from mastapy._internal.python_net import python_net_import

_CMS_NODE_GROUP = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'CMSNodeGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSNodeGroup',)


class CMSNodeGroup(_1475.NodeGroup):
    '''CMSNodeGroup

    This is a mastapy class.
    '''

    TYPE = _CMS_NODE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CMSNodeGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_element_face_group(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CreateElementFaceGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateElementFaceGroup
