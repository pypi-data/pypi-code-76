'''_4915.py

BevelDifferentialSunGearCompoundModalAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4911
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'BevelDifferentialSunGearCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearCompoundModalAnalysis',)


class BevelDifferentialSunGearCompoundModalAnalysis(_4911.BevelDifferentialGearCompoundModalAnalysis):
    '''BevelDifferentialSunGearCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
