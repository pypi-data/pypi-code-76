'''_196.py

CMSNodeGroup
'''


from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import _169
from mastapy._internal.python_net import python_net_import

_CMS_NODE_GROUP = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'CMSNodeGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSNodeGroup',)


class CMSNodeGroup(_169.NodeGroup):
    '''CMSNodeGroup

    This is a mastapy class.
    '''

    TYPE = _CMS_NODE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CMSNodeGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def create_element_face_group(self):
        ''' 'CreateElementFaceGroup' is the original name of this method.'''

        self.wrapped.CreateElementFaceGroup()
