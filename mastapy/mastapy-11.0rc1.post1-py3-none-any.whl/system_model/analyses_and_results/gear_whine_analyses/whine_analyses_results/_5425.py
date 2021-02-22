'''_5425.py

ComponentSelection
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _5436
from mastapy._internal.python_net import python_net_import

_COMPONENT_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ComponentSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentSelection',)


class ComponentSelection(_5436.ResultNodeSelection):
    '''ComponentSelection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
