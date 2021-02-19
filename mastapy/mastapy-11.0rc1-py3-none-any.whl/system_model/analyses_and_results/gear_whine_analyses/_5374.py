'''_5374.py

ElectricMachineStatorToothLoadsExcitationDetail
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5367
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_STATOR_TOOTH_LOADS_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ElectricMachineStatorToothLoadsExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineStatorToothLoadsExcitationDetail',)


class ElectricMachineStatorToothLoadsExcitationDetail(_5367.ElectricMachinePeriodicExcitationDetail):
    '''ElectricMachineStatorToothLoadsExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_STATOR_TOOTH_LOADS_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineStatorToothLoadsExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
