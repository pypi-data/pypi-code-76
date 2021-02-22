'''_1874.py

ModalAnalysesAtSpeedsViewable
'''


from mastapy.system_model.drawing import _1880
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSES_AT_SPEEDS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ModalAnalysesAtSpeedsViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysesAtSpeedsViewable',)


class ModalAnalysesAtSpeedsViewable(_1880.RotorDynamicsViewable):
    '''ModalAnalysesAtSpeedsViewable

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSES_AT_SPEEDS_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysesAtSpeedsViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
