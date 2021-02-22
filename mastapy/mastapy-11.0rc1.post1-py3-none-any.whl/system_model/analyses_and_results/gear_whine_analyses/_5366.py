'''_5366.py

DynamicModelForGearWhine
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses import _5911
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODEL_FOR_GEAR_WHINE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'DynamicModelForGearWhine')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelForGearWhine',)


class DynamicModelForGearWhine(_5911.DynamicAnalysis):
    '''DynamicModelForGearWhine

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODEL_FOR_GEAR_WHINE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelForGearWhine.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
