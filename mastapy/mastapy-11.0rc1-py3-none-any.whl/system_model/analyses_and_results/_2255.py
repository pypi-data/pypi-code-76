'''_2255.py

CompoundModalAnalysesataStiffnessAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_MODAL_ANALYSESATA_STIFFNESS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysesataStiffnessAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysesataStiffnessAnalysis',)


class CompoundModalAnalysesataStiffnessAnalysis(_2213.CompoundAnalysis):
    '''CompoundModalAnalysesataStiffnessAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSESATA_STIFFNESS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysesataStiffnessAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
