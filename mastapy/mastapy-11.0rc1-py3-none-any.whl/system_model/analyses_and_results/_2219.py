'''_2219.py

DynamicModelataStiffnessAnalysis
'''


from mastapy.system_model.analyses_and_results import _2214
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODELATA_STIFFNESS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicModelataStiffnessAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelataStiffnessAnalysis',)


class DynamicModelataStiffnessAnalysis(_2214.SingleAnalysis):
    '''DynamicModelataStiffnessAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_MODELATA_STIFFNESS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicModelataStiffnessAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
