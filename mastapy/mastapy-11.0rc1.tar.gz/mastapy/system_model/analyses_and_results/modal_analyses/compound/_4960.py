'''_4960.py

GearSetCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4998
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'GearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundModalAnalysis',)


class GearSetCompoundModalAnalysis(_4998.SpecialisedAssemblyCompoundModalAnalysis):
    '''GearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
