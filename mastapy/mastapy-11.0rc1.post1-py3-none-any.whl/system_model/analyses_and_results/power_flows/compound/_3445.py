'''_3445.py

CVTPulleyCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3487
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CVTPulleyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundPowerFlow',)


class CVTPulleyCompoundPowerFlow(_3487.PulleyCompoundPowerFlow):
    '''CVTPulleyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
