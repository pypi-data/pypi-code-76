'''_6174.py

ElectricMachineHarmonicLoadDataFromExcel
'''


from mastapy.system_model.analyses_and_results.static_loads import _6173
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_EXCEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadDataFromExcel')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadDataFromExcel',)


class ElectricMachineHarmonicLoadDataFromExcel(_6173.ElectricMachineHarmonicLoadData):
    '''ElectricMachineHarmonicLoadDataFromExcel

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_EXCEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadDataFromExcel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
