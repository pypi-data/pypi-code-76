'''_4078.py

DynamicModelForAtSpeeds
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses import _5911
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODEL_FOR_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'DynamicModelForAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelForAtSpeeds',)


class DynamicModelForAtSpeeds(_5911.DynamicAnalysis):
    '''DynamicModelForAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODEL_FOR_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelForAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
