'''_3983.py

PartCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PartCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundModalAnalysesAtStiffnesses',)


class PartCompoundModalAnalysesAtStiffnesses(_6562.PartCompoundAnalysis):
    '''PartCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
