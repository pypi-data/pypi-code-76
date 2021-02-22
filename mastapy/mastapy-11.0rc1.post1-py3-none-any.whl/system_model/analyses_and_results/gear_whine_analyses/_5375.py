'''_5375.py

ElectricMachineStatorToothRadialLoadsExcitationDetail
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5374
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_STATOR_TOOTH_RADIAL_LOADS_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ElectricMachineStatorToothRadialLoadsExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineStatorToothRadialLoadsExcitationDetail',)


class ElectricMachineStatorToothRadialLoadsExcitationDetail(_5374.ElectricMachineStatorToothLoadsExcitationDetail):
    '''ElectricMachineStatorToothRadialLoadsExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_STATOR_TOOTH_RADIAL_LOADS_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
