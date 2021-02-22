'''_100.py

OilPumpDetail
'''


from mastapy.materials.efficiency import _101
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility import _1152
from mastapy._internal.python_net import python_net_import

_OIL_PUMP_DETAIL = python_net_import('SMT.MastaAPI.Materials.Efficiency', 'OilPumpDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('OilPumpDetail',)


class OilPumpDetail(_1152.IndependentReportablePropertiesBase['OilPumpDetail']):
    '''OilPumpDetail

    This is a mastapy class.
    '''

    TYPE = _OIL_PUMP_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilPumpDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def oil_pump_drive_type(self) -> '_101.OilPumpDriveType':
        '''OilPumpDriveType: 'OilPumpDriveType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OilPumpDriveType)
        return constructor.new(_101.OilPumpDriveType)(value) if value else None

    @oil_pump_drive_type.setter
    def oil_pump_drive_type(self, value: '_101.OilPumpDriveType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilPumpDriveType = value

    @property
    def oil_pump_efficiency(self) -> 'float':
        '''float: 'OilPumpEfficiency' is the original name of this property.'''

        return self.wrapped.OilPumpEfficiency

    @oil_pump_efficiency.setter
    def oil_pump_efficiency(self, value: 'float'):
        self.wrapped.OilPumpEfficiency = float(value) if value else 0.0

    @property
    def electric_motor_efficiency(self) -> 'float':
        '''float: 'ElectricMotorEfficiency' is the original name of this property.'''

        return self.wrapped.ElectricMotorEfficiency

    @electric_motor_efficiency.setter
    def electric_motor_efficiency(self, value: 'float'):
        self.wrapped.ElectricMotorEfficiency = float(value) if value else 0.0
