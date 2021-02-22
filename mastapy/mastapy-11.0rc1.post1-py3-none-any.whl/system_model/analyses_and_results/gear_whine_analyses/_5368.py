'''_5368.py

ElectricMachineRotorXForcePeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5367
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_ROTOR_X_FORCE_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ElectricMachineRotorXForcePeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineRotorXForcePeriodicExcitationDetail',)


class ElectricMachineRotorXForcePeriodicExcitationDetail(_5367.ElectricMachinePeriodicExcitationDetail):
    '''ElectricMachineRotorXForcePeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_ROTOR_X_FORCE_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
