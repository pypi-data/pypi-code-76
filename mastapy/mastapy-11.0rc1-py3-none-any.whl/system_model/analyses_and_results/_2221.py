'''_2221.py

DynamicModelforGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODELFOR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicModelforGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelforGearWhineAnalysis',)


class DynamicModelforGearWhineAnalysis(_2214.SingleAnalysis):
    '''DynamicModelforGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODELFOR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelforGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
