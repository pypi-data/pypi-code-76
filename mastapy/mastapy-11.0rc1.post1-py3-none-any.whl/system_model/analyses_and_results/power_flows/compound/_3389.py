'''_3389.py

AGMAGleasonConicalGearCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3417
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AGMAGleasonConicalGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearCompoundPowerFlow',)


class AGMAGleasonConicalGearCompoundPowerFlow(_3417.ConicalGearCompoundPowerFlow):
    '''AGMAGleasonConicalGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
