'''_5367.py

ElectricMachinePeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5418
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ElectricMachinePeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachinePeriodicExcitationDetail',)


class ElectricMachinePeriodicExcitationDetail(_5418.PeriodicExcitationWithReferenceShaft):
    '''ElectricMachinePeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachinePeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
