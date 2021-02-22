'''_2220.py

DynamicModelforatSpeedsAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODELFORAT_SPEEDS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicModelforatSpeedsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelforatSpeedsAnalysis',)


class DynamicModelforatSpeedsAnalysis(_2214.SingleAnalysis):
    '''DynamicModelforatSpeedsAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODELFORAT_SPEEDS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelforatSpeedsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
