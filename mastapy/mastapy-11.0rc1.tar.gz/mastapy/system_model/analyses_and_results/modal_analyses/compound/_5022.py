'''_5022.py

VirtualComponentCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4977
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'VirtualComponentCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentCompoundModalAnalysis',)


class VirtualComponentCompoundModalAnalysis(_4977.MountableComponentCompoundModalAnalysis):
    '''VirtualComponentCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
