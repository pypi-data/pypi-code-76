'''_4958.py

GearCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4977
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'GearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundModalAnalysis',)


class GearCompoundModalAnalysis(_4977.MountableComponentCompoundModalAnalysis):
    '''GearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
