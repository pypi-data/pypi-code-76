'''_3495.py

SpecialisedAssemblyCompoundPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows.compound import _3405
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'SpecialisedAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecialisedAssemblyCompoundPowerFlow',)


class SpecialisedAssemblyCompoundPowerFlow(_3405.AbstractAssemblyCompoundPowerFlow):
    '''SpecialisedAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SPECIALISED_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpecialisedAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
