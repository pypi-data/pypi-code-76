'''_3831.py

AGMAGleasonConicalGearSetCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3859
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AGMAGleasonConicalGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearSetCompoundPowerFlow',)


class AGMAGleasonConicalGearSetCompoundPowerFlow(_3859.ConicalGearSetCompoundPowerFlow):
    '''AGMAGleasonConicalGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
