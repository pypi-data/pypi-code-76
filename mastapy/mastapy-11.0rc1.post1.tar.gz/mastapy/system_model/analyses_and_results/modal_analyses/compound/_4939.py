'''_4939.py

CouplingHalfCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4977
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CouplingHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfCompoundModalAnalysis',)


class CouplingHalfCompoundModalAnalysis(_4977.MountableComponentCompoundModalAnalysis):
    '''CouplingHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
