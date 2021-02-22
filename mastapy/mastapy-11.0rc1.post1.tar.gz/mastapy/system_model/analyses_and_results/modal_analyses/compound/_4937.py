'''_4937.py

CouplingCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4998
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'CouplingCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundModalAnalysis',)


class CouplingCompoundModalAnalysis(_4998.SpecialisedAssemblyCompoundModalAnalysis):
    '''CouplingCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
