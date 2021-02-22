'''_6200.py

HarmonicLoadDataJMAGImport
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6168, _6199, _6180
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_JMAG_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataJMAGImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataJMAGImport',)


class HarmonicLoadDataJMAGImport(_6199.HarmonicLoadDataImportFromMotorPackages['_6180.ElectricMachineHarmonicLoadJMAGImportOptions']):
    '''HarmonicLoadDataJMAGImport

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_LOAD_DATA_JMAG_IMPORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataJMAGImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def select_jmag_file(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'SelectJMAGFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectJMAGFile

    @property
    def electric_machine_data_per_speed(self) -> 'List[_6168.DataFromJMAGPerSpeed]':
        '''List[DataFromJMAGPerSpeed]: 'ElectricMachineDataPerSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElectricMachineDataPerSpeed, constructor.new(_6168.DataFromJMAGPerSpeed))
        return value
