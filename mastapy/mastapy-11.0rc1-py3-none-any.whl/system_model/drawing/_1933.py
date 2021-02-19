'''_1933.py

StabilityAnalysisViewable
'''


from mastapy.system_model.drawing import _1930
from mastapy._internal.python_net import python_net_import

_STABILITY_ANALYSIS_VIEWABLE = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'StabilityAnalysisViewable')


__docformat__ = 'restructuredtext en'
__all__ = ('StabilityAnalysisViewable',)


class StabilityAnalysisViewable(_1930.RotorDynamicsViewable):
    '''StabilityAnalysisViewable

    This is a mastapy class.
    '''

    TYPE = _STABILITY_ANALYSIS_VIEWABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StabilityAnalysisViewable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
