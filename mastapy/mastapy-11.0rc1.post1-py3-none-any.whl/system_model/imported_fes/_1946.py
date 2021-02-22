'''_1946.py

ElementFaceGroupWithSelection
'''


from mastapy.system_model.imported_fes import _1949
from mastapy.nodal_analysis.component_mode_synthesis import _1497
from mastapy.fe_tools.vis_tools_global import _965
from mastapy._internal.python_net import python_net_import

_ELEMENT_FACE_GROUP_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ElementFaceGroupWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementFaceGroupWithSelection',)


class ElementFaceGroupWithSelection(_1949.FEEntityGroupWithSelection['_1497.CMSElementFaceGroup', '_965.ElementFace']):
    '''ElementFaceGroupWithSelection

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_FACE_GROUP_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementFaceGroupWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
