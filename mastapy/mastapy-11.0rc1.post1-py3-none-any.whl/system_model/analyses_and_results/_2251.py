'''_2251.py

CompoundDynamicModelforGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODELFOR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelforGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelforGearWhineAnalysis',)


class CompoundDynamicModelforGearWhineAnalysis(_2213.CompoundAnalysis):
    '''CompoundDynamicModelforGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_MODELFOR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelforGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
