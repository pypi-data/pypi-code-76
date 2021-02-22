'''_2249.py

CompoundDynamicModelataStiffnessAnalysis
'''


from mastapy.system_model.analyses_and_results import _2213
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODELATA_STIFFNESS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelataStiffnessAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelataStiffnessAnalysis',)


class CompoundDynamicModelataStiffnessAnalysis(_2213.CompoundAnalysis):
    '''CompoundDynamicModelataStiffnessAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_MODELATA_STIFFNESS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelataStiffnessAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
