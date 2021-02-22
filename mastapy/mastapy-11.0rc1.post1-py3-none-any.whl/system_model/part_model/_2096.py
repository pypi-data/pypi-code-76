'''_2096.py

Connector
'''


from typing import Optional

from mastapy.system_model.connections_and_sockets import (
    _1930, _1921, _1928, _1933,
    _1934, _1935, _1936, _1938,
    _1939, _1941, _1942, _1943,
    _1946, _1947, _1948, _1926,
    _1920, _1922, _1923, _1927,
    _1937, _1940, _1945, _1949
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1964, _1953, _1955, _1957,
    _1959, _1961, _1963, _1965,
    _1967, _1969, _1972, _1973,
    _1974, _1977, _1979, _1981,
    _1983, _1985
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _1988, _1989, _1991, _1992,
    _1987, _1990, _1993
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1995, _1997, _1999, _2001,
    _2003, _2005, _2006, _1994,
    _1996, _1998, _2000, _2002,
    _2004
)
from mastapy.system_model.part_model import (
    _2085, _2094, _2093, _2112
)
from mastapy.system_model.part_model.shaft_model import _2129
from mastapy.system_model.part_model.cycloidal import _2215
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2112.MountableComponent):
    '''Connector

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def outer_socket(self) -> '_1930.CylindricalSocket':
        '''CylindricalSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1930.CylindricalSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_bearing_outer_socket(self) -> '_1921.BearingOuterSocket':
        '''BearingOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1921.BearingOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to BearingOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cvt_pulley_socket(self) -> '_1928.CVTPulleySocket':
        '''CVTPulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1928.CVTPulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_connecting_socket(self) -> '_1933.InnerShaftConnectingSocket':
        '''InnerShaftConnectingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1933.InnerShaftConnectingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftConnectingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_connecting_socket_base(self) -> '_1934.InnerShaftConnectingSocketBase':
        '''InnerShaftConnectingSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1934.InnerShaftConnectingSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftConnectingSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_socket(self) -> '_1935.InnerShaftSocket':
        '''InnerShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1935.InnerShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_inner_shaft_socket_base(self) -> '_1936.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1936.InnerShaftSocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_outer_shaft_connecting_socket(self) -> '_1938.OuterShaftConnectingSocket':
        '''OuterShaftConnectingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1938.OuterShaftConnectingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftConnectingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_outer_shaft_socket(self) -> '_1939.OuterShaftSocket':
        '''OuterShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1939.OuterShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_planetary_socket(self) -> '_1941.PlanetarySocket':
        '''PlanetarySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1941.PlanetarySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_planetary_socket_base(self) -> '_1942.PlanetarySocketBase':
        '''PlanetarySocketBase: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1942.PlanetarySocketBase.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_pulley_socket(self) -> '_1943.PulleySocket':
        '''PulleySocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1943.PulleySocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PulleySocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_rolling_ring_socket(self) -> '_1946.RollingRingSocket':
        '''RollingRingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.RollingRingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_shaft_connecting_socket(self) -> '_1947.ShaftConnectingSocket':
        '''ShaftConnectingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.ShaftConnectingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftConnectingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_shaft_socket(self) -> '_1948.ShaftSocket':
        '''ShaftSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.ShaftSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ShaftSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cylindrical_gear_teeth_socket(self) -> '_1964.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.CylindricalGearTeethSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_inner_socket(self) -> '_1988.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.CycloidalDiscInnerSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_outer_socket(self) -> '_1989.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.CycloidalDiscOuterSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_1991.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_ring_pins_socket(self) -> '_1992.RingPinsSocket':
        '''RingPinsSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.RingPinsSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to RingPinsSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_clutch_socket(self) -> '_1995.ClutchSocket':
        '''ClutchSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.ClutchSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ClutchSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_concept_coupling_socket(self) -> '_1997.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.ConceptCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_coupling_socket(self) -> '_1999.CouplingSocket':
        '''CouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.CouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to CouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_part_to_part_shear_coupling_socket(self) -> '_2001.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.PartToPartShearCouplingSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_spring_damper_socket(self) -> '_2003.SpringDamperSocket':
        '''SpringDamperSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.SpringDamperSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_torque_converter_pump_socket(self) -> '_2005.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.TorqueConverterPumpSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_socket_of_type_torque_converter_turbine_socket(self) -> '_2006.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'OuterSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.TorqueConverterTurbineSocket.TYPE not in self.wrapped.OuterSocket.__class__.__mro__:
            raise CastException('Failed to cast outer_socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.OuterSocket.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterSocket.__class__)(self.wrapped.OuterSocket) if self.wrapped.OuterSocket else None

    @property
    def outer_connection(self) -> '_1926.Connection':
        '''Connection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.Connection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to Connection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1920.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_belt_connection(self) -> '_1922.BeltConnection':
        '''BeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.BeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_coaxial_connection(self) -> '_1923.CoaxialConnection':
        '''CoaxialConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1923.CoaxialConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CoaxialConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cvt_belt_connection(self) -> '_1927.CVTBeltConnection':
        '''CVTBeltConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1927.CVTBeltConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CVTBeltConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_inter_mountable_component_connection(self) -> '_1937.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1937.InterMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_planetary_connection(self) -> '_1940.PlanetaryConnection':
        '''PlanetaryConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1940.PlanetaryConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PlanetaryConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_rolling_ring_connection(self) -> '_1945.RollingRingConnection':
        '''RollingRingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.RollingRingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RollingRingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_shaft_to_mountable_component_connection(self) -> '_1949.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.ShaftToMountableComponentConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_agma_gleason_conical_gear_mesh(self) -> '_1953.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_bevel_differential_gear_mesh(self) -> '_1955.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.BevelDifferentialGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_bevel_gear_mesh(self) -> '_1957.BevelGearMesh':
        '''BevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.BevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to BevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_concept_gear_mesh(self) -> '_1959.ConceptGearMesh':
        '''ConceptGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.ConceptGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_conical_gear_mesh(self) -> '_1961.ConicalGearMesh':
        '''ConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.ConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cylindrical_gear_mesh(self) -> '_1963.CylindricalGearMesh':
        '''CylindricalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.CylindricalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_face_gear_mesh(self) -> '_1965.FaceGearMesh':
        '''FaceGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.FaceGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to FaceGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_gear_mesh(self) -> '_1967.GearMesh':
        '''GearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1967.GearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to GearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_hypoid_gear_mesh(self) -> '_1969.HypoidGearMesh':
        '''HypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.HypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to HypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1972.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1972.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1973.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1974.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_spiral_bevel_gear_mesh(self) -> '_1977.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.SpiralBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_straight_bevel_diff_gear_mesh(self) -> '_1979.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.StraightBevelDiffGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_straight_bevel_gear_mesh(self) -> '_1981.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.StraightBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_worm_gear_mesh(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.WormGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to WormGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_zerol_bevel_gear_mesh(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.ZerolBevelGearMesh.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cycloidal_disc_central_bearing_connection(self) -> '_1987.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_ring_pins_to_disc_connection(self) -> '_1993.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.RingPinsToDiscConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_clutch_connection(self) -> '_1994.ClutchConnection':
        '''ClutchConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.ClutchConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ClutchConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_concept_coupling_connection(self) -> '_1996.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.ConceptCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_coupling_connection(self) -> '_1998.CouplingConnection':
        '''CouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.CouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to CouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_part_to_part_shear_coupling_connection(self) -> '_2000.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.PartToPartShearCouplingConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_spring_damper_connection(self) -> '_2002.SpringDamperConnection':
        '''SpringDamperConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.SpringDamperConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to SpringDamperConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_connection_of_type_torque_converter_connection(self) -> '_2004.TorqueConverterConnection':
        '''TorqueConverterConnection: 'OuterConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.TorqueConverterConnection.TYPE not in self.wrapped.OuterConnection.__class__.__mro__:
            raise CastException('Failed to cast outer_connection to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.OuterConnection.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterConnection.__class__)(self.wrapped.OuterConnection) if self.wrapped.OuterConnection else None

    @property
    def outer_component(self) -> '_2085.AbstractShaft':
        '''AbstractShaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.AbstractShaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to AbstractShaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    @property
    def outer_component_of_type_shaft(self) -> '_2129.Shaft':
        '''Shaft: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.Shaft.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to Shaft. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    @property
    def outer_component_of_type_cycloidal_disc(self) -> '_2215.CycloidalDisc':
        '''CycloidalDisc: 'OuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.CycloidalDisc.TYPE not in self.wrapped.OuterComponent.__class__.__mro__:
            raise CastException('Failed to cast outer_component to CycloidalDisc. Expected: {}.'.format(self.wrapped.OuterComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OuterComponent.__class__)(self.wrapped.OuterComponent) if self.wrapped.OuterComponent else None

    def house_in(self, shaft: '_2085.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_1926.Connection':
        ''' 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def try_house_in(self, shaft: '_2085.AbstractShaft', offset: Optional['float'] = float('nan')) -> '_2094.ComponentsConnectedResult':
        ''' 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_component(self, component: '_2093.Component') -> '_2085.AbstractShaft':
        ''' 'OtherComponent' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.AbstractShaft
        '''

        method_result = self.wrapped.OtherComponent(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None
