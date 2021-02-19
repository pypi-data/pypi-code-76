'''_5714.py

ComponentSelection
'''


from mastapy.system_model.analyses_and_results.harmonic_analyses.results import _5727
from mastapy._internal.python_net import python_net_import

_COMPONENT_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results', 'ComponentSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentSelection',)


class ComponentSelection(_5727.ResultNodeSelection):
    '''ComponentSelection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
