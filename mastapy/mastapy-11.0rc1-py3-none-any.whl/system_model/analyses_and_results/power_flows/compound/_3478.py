'''_3478.py

PartCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _6562
from mastapy._internal.python_net import python_net_import

_PART_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PartCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PartCompoundPowerFlow',)


class PartCompoundPowerFlow(_6562.PartCompoundAnalysis):
    '''PartCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PART_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
