'''_3862.py

CouplingCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3923
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'CouplingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundPowerFlow',)


class CouplingCompoundPowerFlow(_3923.SpecialisedAssemblyCompoundPowerFlow):
    '''CouplingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
