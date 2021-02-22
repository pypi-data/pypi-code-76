'''_1875.py

ModalAnalysesAtStiffnessesViewable
'''


from mastapy.system_model.drawing import _1880
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSES_AT_STIFFNESSES_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ModalAnalysesAtStiffnessesViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesAtStiffnessesViewable',)


class ModalAnalysesAtStiffnessesViewable(_1880.RotorDynamicsViewable):
    '''ModalAnalysesAtStiffnessesViewable

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSES_AT_STIFFNESSES_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesAtStiffnessesViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
