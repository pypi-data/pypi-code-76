'''_5433.py

NodeSelection
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _5436
from mastapy._internal.python_net import python_net_import

_NODE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'NodeSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeSelection',)


class NodeSelection(_5436.ResultNodeSelection):
    '''NodeSelection

    This is a mastapy class.
    '''

    TYPE = _NODE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'NodeSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
