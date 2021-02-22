'''_1855.py

Connection
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1876, _1857, _1859, _1861,
    _1862, _1863, _1865, _1866,
    _1868, _1869, _1872, _1873,
    _1874
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1880, _1882, _1884, _1886,
    _1888, _1890, _1892, _1894,
    _1896, _1897, _1901, _1902,
    _1904, _1906, _1908, _1910,
    _1912
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1914, _1916, _1918, _1920,
    _1922, _1924, _1925
)
from mastapy.system_model.part_model import (
    _2009, _2002, _2005, _2007,
    _2012, _2013, _2016, _2018,
    _2021, _2025, _2026, _2027,
    _2029, _2032, _2034, _2035,
    _2040, _2041
)
from mastapy.system_model.part_model.shaft_model import _2044
from mastapy.system_model.part_model.gears import (
    _2074, _2076, _2078, _2079,
    _2080, _2082, _2084, _2086,
    _2088, _2089, _2091, _2095,
    _2097, _2099, _2101, _2104,
    _2106, _2108, _2110, _2111,
    _2112, _2114
)
from mastapy.system_model.part_model.couplings import (
    _2136, _2139, _2141, _2143,
    _2145, _2146, _2152, _2154,
    _2156, _2159, _2160, _2161,
    _2163, _2165
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _1814

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_1814.DesignEntity):
    '''Connection

    This is a mastapy class.
    '''

    TYPE = _CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.DrawingPosition) if self.wrapped.DrawingPosition else None

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioFromAToB

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioFromAToB

    @property
    def unique_name(self) -> 'str':
        '''str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UniqueName

    @property
    def connection_id(self) -> 'str':
        '''str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectionID

    @property
    def socket_a(self) -> '_1876.Socket':
        '''Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.Socket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_1857.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.CVTPulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_1859.CylindricalSocket':
        '''CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1859.CylindricalSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_1861.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1861.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_connecting_socket(self) -> '_1862.InnerShaftConnectingSocket':
        '''InnerShaftConnectingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1862.InnerShaftConnectingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_1863.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1863.InnerShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_connecting_socket(self) -> '_1865.OuterShaftConnectingSocket':
        '''OuterShaftConnectingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.OuterShaftConnectingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_1866.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1866.OuterShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_1868.PlanetarySocket':
        '''PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1868.PlanetarySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_1869.PulleySocket':
        '''PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.PulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_1872.RollingRingSocket':
        '''RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.RollingRingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_shaft_connecting_socket(self) -> '_1873.ShaftConnectingSocket':
        '''ShaftConnectingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.ShaftConnectingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_1874.ShaftSocket':
        '''ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.ShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_1880.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_1882.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_1884.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1884.BevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_1886.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_1888.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1888.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_1890.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1890.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_1892.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.FaceGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_1894.GearTeethSocket':
        '''GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.GearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_1896.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1896.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_1897.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1897.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_1901.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1901.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_1902.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_1904.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1904.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_1906.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1906.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_1908.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1908.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_1910.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1910.WormGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_1912.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1912.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_1914.ClutchSocket':
        '''ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.ClutchSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_1916.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1916.ConceptCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_1918.CouplingSocket':
        '''CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.CouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_1920.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_1922.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.SpringDamperSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_1924.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1924.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_1925.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1925.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_b(self) -> '_1876.Socket':
        '''Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1876.Socket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_1857.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1857.CVTPulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_1859.CylindricalSocket':
        '''CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1859.CylindricalSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_1861.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1861.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_connecting_socket(self) -> '_1862.InnerShaftConnectingSocket':
        '''InnerShaftConnectingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1862.InnerShaftConnectingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_1863.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1863.InnerShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_connecting_socket(self) -> '_1865.OuterShaftConnectingSocket':
        '''OuterShaftConnectingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.OuterShaftConnectingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_1866.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1866.OuterShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_1868.PlanetarySocket':
        '''PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1868.PlanetarySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_1869.PulleySocket':
        '''PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.PulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_1872.RollingRingSocket':
        '''RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.RollingRingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_shaft_connecting_socket(self) -> '_1873.ShaftConnectingSocket':
        '''ShaftConnectingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.ShaftConnectingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftConnectingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_1874.ShaftSocket':
        '''ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.ShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_1880.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1880.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_1882.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_1884.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1884.BevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_1886.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_1888.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1888.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_1890.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1890.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_1892.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.FaceGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_1894.GearTeethSocket':
        '''GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.GearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_1896.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1896.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_1897.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1897.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_1901.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1901.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_1902.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_1904.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1904.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_1906.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1906.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_1908.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1908.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_1910.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1910.WormGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_1912.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1912.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_1914.ClutchSocket':
        '''ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.ClutchSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_1916.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1916.ConceptCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_1918.CouplingSocket':
        '''CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.CouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_1920.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_1922.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.SpringDamperSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_1924.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1924.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_1925.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1925.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def owner_a(self) -> '_2009.Component':
        '''Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.Component.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2002.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bearing(self) -> '_2005.Bearing':
        '''Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.Bearing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bolt(self) -> '_2007.Bolt':
        '''Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.Bolt.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_connector(self) -> '_2012.Connector':
        '''Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.Connector.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_datum(self) -> '_2013.Datum':
        '''Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.Datum.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2016.ExternalCADModel':
        '''ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.ExternalCADModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2018.GuideDxfModel':
        '''GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.GuideDxfModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_imported_fe_component(self) -> '_2021.ImportedFEComponent':
        '''ImportedFEComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.ImportedFEComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ImportedFEComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2025.MassDisc':
        '''MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.MassDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2026.MeasurementComponent':
        '''MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.MeasurementComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2027.MountableComponent':
        '''MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.MountableComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2029.OilSeal':
        '''OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.OilSeal.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2032.PlanetCarrier':
        '''PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.PlanetCarrier.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_point_load(self) -> '_2034.PointLoad':
        '''PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.PointLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_power_load(self) -> '_2035.PowerLoad':
        '''PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.PowerLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2040.UnbalancedMass':
        '''UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.UnbalancedMass.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2041.VirtualComponent':
        '''VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.VirtualComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft(self) -> '_2044.Shaft':
        '''Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.Shaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2074.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2076.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.BevelDifferentialGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2078.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2079.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2080.BevelGear':
        '''BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.BevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2082.ConceptGear':
        '''ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2084.ConicalGear':
        '''ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.ConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2086.CylindricalGear':
        '''CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.CylindricalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2088.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2089.FaceGear':
        '''FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.FaceGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_gear(self) -> '_2091.Gear':
        '''Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.Gear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2095.HypoidGear':
        '''HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.HypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2097.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2099.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2101.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2104.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2104.SpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2106.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2106.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2108.StraightBevelGear':
        '''StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.StraightBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2110.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2111.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.StraightBevelSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2112.WormGear':
        '''WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.WormGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2114.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ZerolBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2136.ClutchHalf':
        '''ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.ClutchHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2139.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2141.CouplingHalf':
        '''CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.CouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2143.CVTPulley':
        '''CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.CVTPulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2145.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_pulley(self) -> '_2146.Pulley':
        '''Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.Pulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2152.RollingRing':
        '''RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.RollingRing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2154.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.ShaftHubConnection.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2156.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.SpringDamperHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2159.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.SynchroniserHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2160.SynchroniserPart':
        '''SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.SynchroniserPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2161.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.SynchroniserSleeve.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2163.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.TorqueConverterPump.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2165.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2165.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_b(self) -> '_2009.Component':
        '''Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.Component.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2002.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bearing(self) -> '_2005.Bearing':
        '''Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.Bearing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bolt(self) -> '_2007.Bolt':
        '''Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.Bolt.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_connector(self) -> '_2012.Connector':
        '''Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.Connector.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_datum(self) -> '_2013.Datum':
        '''Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.Datum.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2016.ExternalCADModel':
        '''ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2016.ExternalCADModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2018.GuideDxfModel':
        '''GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.GuideDxfModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_imported_fe_component(self) -> '_2021.ImportedFEComponent':
        '''ImportedFEComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.ImportedFEComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ImportedFEComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2025.MassDisc':
        '''MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.MassDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2026.MeasurementComponent':
        '''MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.MeasurementComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2027.MountableComponent':
        '''MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.MountableComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2029.OilSeal':
        '''OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.OilSeal.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2032.PlanetCarrier':
        '''PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.PlanetCarrier.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_point_load(self) -> '_2034.PointLoad':
        '''PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.PointLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_power_load(self) -> '_2035.PowerLoad':
        '''PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.PowerLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2040.UnbalancedMass':
        '''UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.UnbalancedMass.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2041.VirtualComponent':
        '''VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.VirtualComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft(self) -> '_2044.Shaft':
        '''Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.Shaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2074.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2076.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.BevelDifferentialGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2078.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2079.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2080.BevelGear':
        '''BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.BevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2082.ConceptGear':
        '''ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.ConceptGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2084.ConicalGear':
        '''ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.ConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2086.CylindricalGear':
        '''CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.CylindricalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2088.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2089.FaceGear':
        '''FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.FaceGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_gear(self) -> '_2091.Gear':
        '''Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.Gear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2095.HypoidGear':
        '''HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.HypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2097.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2099.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2101.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2104.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2104.SpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2106.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2106.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2108.StraightBevelGear':
        '''StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2108.StraightBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2110.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2111.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.StraightBevelSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2112.WormGear':
        '''WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.WormGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2114.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ZerolBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2136.ClutchHalf':
        '''ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2136.ClutchHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2139.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2141.CouplingHalf':
        '''CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.CouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2143.CVTPulley':
        '''CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.CVTPulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2145.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_pulley(self) -> '_2146.Pulley':
        '''Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.Pulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2152.RollingRing':
        '''RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.RollingRing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2154.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2154.ShaftHubConnection.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2156.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.SpringDamperHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2159.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.SynchroniserHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2160.SynchroniserPart':
        '''SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.SynchroniserPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2161.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.SynchroniserSleeve.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2163.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.TorqueConverterPump.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2165.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2165.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    def socket_for(self, component: '_2009.Component') -> '_1876.Socket':
        ''' 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_owner(self, component: '_2009.Component') -> '_2009.Component':
        ''' 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket_for_component(self, component: '_2009.Component') -> '_1876.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket(self, socket: '_1876.Socket') -> '_1876.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
