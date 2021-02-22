'''_5590.py

AbstractPeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6528, _6478, _6495, _6504,
    _6505, _6506, _6507, _6524,
    _6566, _6582, _6611
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    '''AbstractPeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_load_data(self) -> '_6528.HarmonicLoadDataBase':
        '''HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6528.HarmonicLoadDataBase.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to HarmonicLoadDataBase. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6478.ConicalGearSetHarmonicLoadData':
        '''ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6478.ConicalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6495.CylindricalGearSetHarmonicLoadData':
        '''CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6495.CylindricalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6504.ElectricMachineHarmonicLoadData':
        '''ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6504.ElectricMachineHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6505.ElectricMachineHarmonicLoadDataFromExcel':
        '''ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6505.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6506.ElectricMachineHarmonicLoadDataFromJMAG':
        '''ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6506.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6507.ElectricMachineHarmonicLoadDataFromMotorCAD':
        '''ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6507.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6524.GearSetHarmonicLoadData':
        '''GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6524.GearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6566.PointLoadHarmonicLoadData':
        '''PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6566.PointLoadHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_6582.SpeedDependentHarmonicLoadData':
        '''SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6582.SpeedDependentHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6611.UnbalancedMassHarmonicLoadData':
        '''UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6611.UnbalancedMassHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None
