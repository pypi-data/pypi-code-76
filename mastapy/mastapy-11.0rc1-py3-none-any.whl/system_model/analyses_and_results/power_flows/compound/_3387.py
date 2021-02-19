'''_3387.py

AbstractAssemblyCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3460
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'AbstractAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundPowerFlow',)


class AbstractAssemblyCompoundPowerFlow(_3460.PartCompoundPowerFlow):
    '''AbstractAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
