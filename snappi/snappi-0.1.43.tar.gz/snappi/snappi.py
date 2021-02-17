import importlib
try:
    from typing import Union
except ImportError:
    pass
try:
    from typing import Literal
except ImportError:
    pass
from .snappicommon import SnappiObject
from .snappicommon import SnappiList
from .snappicommon import SnappiHttpTransport


class Config(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ports': 'PortList',
        'lags': 'LagList',
        'layer1': 'Layer1List',
        'captures': 'CaptureList',
        'devices': 'DeviceList',
        'flows': 'FlowList',
        'options': 'ConfigOptions',
    }

    def __init__(self, parent=None, choice=None):
        super(Config, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def ports(self):
        # type: () -> PortList
        """ports getter

        The ports that will be configured on the traffic generator.

        Returns: list[obj(snappi.Port)]
        """
        return self._get_property('ports', PortList)

    @property
    def lags(self):
        # type: () -> LagList
        """lags getter

        The lags that will be configured on the traffic generator.

        Returns: list[obj(snappi.Lag)]
        """
        return self._get_property('lags', LagList)

    @property
    def layer1(self):
        # type: () -> Layer1List
        """layer1 getter

        The layer1 settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Layer1)]
        """
        return self._get_property('layer1', Layer1List)

    @property
    def captures(self):
        # type: () -> CaptureList
        """captures getter

        The capture settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Capture)]
        """
        return self._get_property('captures', CaptureList)

    @property
    def devices(self):
        # type: () -> DeviceList
        """devices getter

        The emulated device settings that will be configured on the traffic generator.

        Returns: list[obj(snappi.Device)]
        """
        return self._get_property('devices', DeviceList)

    @property
    def flows(self):
        # type: () -> FlowList
        """flows getter

        The flows that will be configured on the traffic generator.

        Returns: list[obj(snappi.Flow)]
        """
        return self._get_property('flows', FlowList)

    @property
    def options(self):
        # type: () -> ConfigOptions
        """options getter

        Global configuration options.

        Returns: obj(snappi.ConfigOptions)
        """
        return self._get_property('options', ConfigOptions)


class Port(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, location=None, name=None):
        super(Port, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('location', location)
        self._set_property('name', name)

    @property
    def location(self):
        # type: () -> str
        """location getter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        Returns: str
        """
        return self._get_property('location')

    @location.setter
    def location(self, value):
        """location setter

        The location of a test port. It is the endpoint where packets will emit from.. Test port locations can be the following:. - physical appliance with multiple ports. - physical chassis with multiple cards and ports. - local interface. - virtual machine, docker container, kubernetes cluster. . The test port location format is implementation specific. Use the /results/capabilities API to determine what formats an implementation supports for the location property.. Get the configured location state by using the /results/port API.

        value: str
        """
        self._set_property('location', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class PortList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Port]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortList
        return self._iter()

    def __next__(self):
        # type: () -> Port
        return self._next()

    def next(self):
        # type: () -> Port
        return self._next()

    def port(self, location=None, name=None):
        # type: () -> PortList
        """Factory method that creates an instance of Port class

        An abstract test port.
        """
        item = Port(location=location, name=name)
        self._add(item)
        return self


class Lag(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'protocol': 'LagProtocol',
        'ethernet': 'DeviceEthernet',
    }

    def __init__(self, parent=None, choice=None, port_names=None, name=None):
        super(Lag, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('name', name)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def protocol(self):
        # type: () -> LagProtocol
        """protocol getter

        Static lag or LACP protocol settings.

        Returns: obj(snappi.LagProtocol)
        """
        return self._get_property('protocol', LagProtocol)

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.Per port ethernet and vlan settings.

        Returns: obj(snappi.DeviceEthernet)
        """
        return self._get_property('ethernet', DeviceEthernet)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class LagProtocol(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'lacp': 'LagLacp',
        'static': 'LagStatic',
    }

    LACP = 'lacp'
    STATIC = 'static'

    def __init__(self, parent=None, choice=None):
        super(LagProtocol, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def lacp(self):
        # type: () -> LagLacp
        """Factory property that returns an instance of the LagLacp class

        TBD
        """
        return self._get_property('lacp', LagLacp(self, 'lacp'))

    @property
    def static(self):
        # type: () -> LagStatic
        """Factory property that returns an instance of the LagStatic class

        TBD
        """
        return self._get_property('static', LagStatic(self, 'static'))

    @property
    def choice(self):
        # type: () -> Union[lacp, static, choice, choice, choice]
        """choice getter

        The type of lag protocol.

        Returns: Union[lacp, static, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of lag protocol.

        value: Union[lacp, static, choice, choice, choice]
        """
        self._set_property('choice', value)


class LagLacp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'actor_key': 'DevicePattern',
        'actor_port_number': 'DevicePattern',
        'actor_port_priority': 'DevicePattern',
        'actor_system_id': 'DevicePattern',
        'actor_system_priority': 'DevicePattern',
    }

    def __init__(self, parent=None, choice=None):
        super(LagLacp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def actor_key(self):
        # type: () -> DevicePattern
        """actor_key getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor key.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('actor_key', DevicePattern)

    @property
    def actor_port_number(self):
        # type: () -> DevicePattern
        """actor_port_number getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor port number.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('actor_port_number', DevicePattern)

    @property
    def actor_port_priority(self):
        # type: () -> DevicePattern
        """actor_port_priority getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor port priority.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('actor_port_priority', DevicePattern)

    @property
    def actor_system_id(self):
        # type: () -> DevicePattern
        """actor_system_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor system id.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('actor_system_id', DevicePattern)

    @property
    def actor_system_priority(self):
        # type: () -> DevicePattern
        """actor_system_priority getter

        A container for emulated device property patterns.A container for emulated device property patterns.The actor system priority.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('actor_system_priority', DevicePattern)


class DevicePattern(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'DeviceCounter',
        'decrement': 'DeviceCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None):
        super(DevicePattern, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def increment(self):
        # type: () -> DeviceCounter
        """Factory property that returns an instance of the DeviceCounter class

        An incrementing pattern.
        """
        return self._get_property('increment', DeviceCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> DeviceCounter
        """Factory property that returns an instance of the DeviceCounter class

        An incrementing pattern.
        """
        return self._get_property('decrement', DeviceCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')


class DeviceCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None):
        super(DeviceCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)

    @property
    def start(self):
        # type: () -> str
        """start getter

        TBD

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        TBD

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._set_property('step', value)


class LagStatic(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'lag_id': 'DevicePattern',
    }

    def __init__(self, parent=None, choice=None):
        super(LagStatic, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def lag_id(self):
        # type: () -> DevicePattern
        """lag_id getter

        A container for emulated device property patterns.A container for emulated device property patterns.The static lag id.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('lag_id', DevicePattern)


class DeviceEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'mac': 'DevicePattern',
        'mtu': 'DevicePattern',
        'vlans': 'DeviceVlanList',
        'ipv4': 'DeviceIpv4',
        'ipv6': 'DeviceIpv6',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceEthernet, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def mac(self):
        # type: () -> DevicePattern
        """mac getter

        A container for emulated device property patterns.Media access control address (MAC) is a 48bit identifier for use as a network address. The value can be an int or a hex string with or without spaces or colons separating each byte. The min value is 0 or '00:00:00:00:00:00'. The max value is 281474976710655 or 'FF:FF:FF:FF:FF:FF'.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('mac', DevicePattern)

    @property
    def mtu(self):
        # type: () -> DevicePattern
        """mtu getter

        A container for emulated device property patterns.Maximum transmission unit. default is 1500

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('mtu', DevicePattern)

    @property
    def vlans(self):
        # type: () -> DeviceVlanList
        """vlans getter

        List of vlans

        Returns: list[obj(snappi.DeviceVlan)]
        """
        return self._get_property('vlans', DeviceVlanList)

    @property
    def ipv4(self):
        # type: () -> DeviceIpv4
        """ipv4 getter

        Emulated ipv4 interface

        Returns: obj(snappi.DeviceIpv4)
        """
        return self._get_property('ipv4', DeviceIpv4)

    @property
    def ipv6(self):
        # type: () -> DeviceIpv6
        """ipv6 getter

        Emulated ipv6 protocol

        Returns: obj(snappi.DeviceIpv6)
        """
        return self._get_property('ipv6', DeviceIpv6)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'tpid': 'DevicePattern',
        'priority': 'DevicePattern',
        'id': 'DevicePattern',
    }

    TPID_8100 = '8100'
    TPID_88A8 = '88a8'
    TPID_9100 = '9100'
    TPID_9200 = '9200'
    TPID_9300 = '9300'

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceVlan, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def tpid(self):
        # type: () -> DevicePattern
        """tpid getter

        A container for emulated device property patterns.Vlan tag protocol identifier.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('tpid', DevicePattern)

    @property
    def priority(self):
        # type: () -> DevicePattern
        """priority getter

        A container for emulated device property patterns.Vlan priority.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('priority', DevicePattern)

    @property
    def id(self):
        # type: () -> DevicePattern
        """id getter

        A container for emulated device property patterns.Vlan id.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('id', DevicePattern)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceVlanList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceVlanList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceVlan]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceVlanList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceVlan
        return self._next()

    def next(self):
        # type: () -> DeviceVlan
        return self._next()

    def vlan(self, name=None):
        # type: () -> DeviceVlanList
        """Factory method that creates an instance of DeviceVlan class

        Emulated vlan protocol
        """
        item = DeviceVlan(name=name)
        self._add(item)
        return self


class DeviceIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'gateway': 'DevicePattern',
        'prefix': 'DevicePattern',
        'bgpv4': 'DeviceBgpv4',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceIpv4, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def gateway(self):
        # type: () -> DevicePattern
        """gateway getter

        A container for emulated device property patterns.The ipv4 address of the gateway.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('gateway', DevicePattern)

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.The prefix of the ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('prefix', DevicePattern)

    @property
    def bgpv4(self):
        # type: () -> DeviceBgpv4
        """bgpv4 getter

        Emulated BGPv4 routerThe bgpv4 device.

        Returns: obj(snappi.DeviceBgpv4)
        """
        return self._get_property('bgpv4', DeviceBgpv4)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'router_id': 'DevicePattern',
        'as_number': 'DevicePattern',
        'hold_time_interval': 'DevicePattern',
        'keep_alive_interval': 'DevicePattern',
        'dut_ipv4_address': 'DevicePattern',
        'dut_as_number': 'DevicePattern',
        'bgpv4_route_ranges': 'DeviceBgpv4RouteRangeList',
        'bgpv6_route_ranges': 'DeviceBgpv6RouteRangeList',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    def __init__(self, parent=None, choice=None, as_type=None, name=None):
        super(DeviceBgpv4, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('as_type', as_type)
        self._set_property('name', name)

    @property
    def router_id(self):
        # type: () -> DevicePattern
        """router_id getter

        A container for emulated device property patterns.The BGP router identifier. It must be the string representation of an IPv4 address 

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('router_id', DevicePattern)

    @property
    def as_number(self):
        # type: () -> DevicePattern
        """as_number getter

        A container for emulated device property patterns.Autonomous system (AS) number of 4 byte

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('as_number', DevicePattern)

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        Returns: Union[ibgp, ebgp]
        """
        return self._get_property('as_type')

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        value: Union[ibgp, ebgp]
        """
        self._set_property('as_type', value)

    @property
    def hold_time_interval(self):
        # type: () -> DevicePattern
        """hold_time_interval getter

        A container for emulated device property patterns.Number of seconds the sender proposes for the value of the Hold Timer

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('hold_time_interval', DevicePattern)

    @property
    def keep_alive_interval(self):
        # type: () -> DevicePattern
        """keep_alive_interval getter

        A container for emulated device property patterns.Number of seconds between transmissions of Keep Alive messages by router

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('keep_alive_interval', DevicePattern)

    @property
    def dut_ipv4_address(self):
        # type: () -> DevicePattern
        """dut_ipv4_address getter

        A container for emulated device property patterns.IPv4 address of the BGP peer for the session

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('dut_ipv4_address', DevicePattern)

    @property
    def dut_as_number(self):
        # type: () -> DevicePattern
        """dut_as_number getter

        A container for emulated device property patterns.Autonomous system (AS) number of the BGP peer router (DUT)

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('dut_as_number', DevicePattern)

    @property
    def bgpv4_route_ranges(self):
        # type: () -> DeviceBgpv4RouteRangeList
        """bgpv4_route_ranges getter

        Emulated bgpv4 route ranges

        Returns: list[obj(snappi.DeviceBgpv4RouteRange)]
        """
        return self._get_property('bgpv4_route_ranges', DeviceBgpv4RouteRangeList)

    @property
    def bgpv6_route_ranges(self):
        # type: () -> DeviceBgpv6RouteRangeList
        """bgpv6_route_ranges getter

        Emulated bgpv6 route ranges

        Returns: list[obj(snappi.DeviceBgpv6RouteRange)]
        """
        return self._get_property('bgpv6_route_ranges', DeviceBgpv6RouteRangeList)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv4RouteRange(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'address_step': 'DevicePattern',
        'prefix': 'DevicePattern',
        'next_hop_address': 'DevicePattern',
        'community': 'DeviceBgpCommunityList',
        'as_path': 'DeviceBgpAsPath',
    }

    def __init__(self, parent=None, choice=None, range_count=None, address_count=None, name=None):
        super(DeviceBgpv4RouteRange, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('range_count', range_count)
        self._set_property('address_count', address_count)
        self._set_property('name', name)

    @property
    def range_count(self):
        # type: () -> int
        """range_count getter

        The number of route ranges per parent bgpv4 device.. If creating sequential routes the range count should default to 1 and the address_count can be used to create a range of . If the parent device_count is 6 and the range_count is 2 that means there will be 2 route_range entries for every device for a total of 12 route ranges. Any child patterns will be applied across the total number of route ranges which implies a pattern count of 12.

        Returns: int
        """
        return self._get_property('range_count')

    @range_count.setter
    def range_count(self, value):
        """range_count setter

        The number of route ranges per parent bgpv4 device.. If creating sequential routes the range count should default to 1 and the address_count can be used to create a range of . If the parent device_count is 6 and the range_count is 2 that means there will be 2 route_range entries for every device for a total of 12 route ranges. Any child patterns will be applied across the total number of route ranges which implies a pattern count of 12.

        value: int
        """
        self._set_property('range_count', value)

    @property
    def address_count(self):
        # type: () -> int
        """address_count getter

        The number of ipv4 addresses in each route range.

        Returns: int
        """
        return self._get_property('address_count')

    @address_count.setter
    def address_count(self, value):
        """address_count setter

        The number of ipv4 addresses in each route range.

        value: int
        """
        self._set_property('address_count', value)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def address_step(self):
        # type: () -> DevicePattern
        """address_step getter

        A container for emulated device property patterns.The amount to increase each address by.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address_step', DevicePattern)

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.The network prefix to be applied to each address. 

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('prefix', DevicePattern)

    @property
    def next_hop_address(self):
        # type: () -> DevicePattern
        """next_hop_address getter

        A container for emulated device property patterns.IP Address of next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('next_hop_address', DevicePattern)

    @property
    def community(self):
        # type: () -> DeviceBgpCommunityList
        """community getter

        TBD

        Returns: list[obj(snappi.DeviceBgpCommunity)]
        """
        return self._get_property('community', DeviceBgpCommunityList)

    @property
    def as_path(self):
        # type: () -> DeviceBgpAsPath
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DeviceBgpAsPath)
        """
        return self._get_property('as_path', DeviceBgpAsPath)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpCommunity(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'as_number': 'DevicePattern',
        'as_custom': 'DevicePattern',
    }

    MANUAL_AS_NUMBER = 'manual_as_number'
    NO_EXPORT = 'no_export'
    NO_ADVERTISED = 'no_advertised'
    NO_EXPORT_SUBCONFED = 'no_export_subconfed'
    LLGR_STALE = 'llgr_stale'
    NO_LLGR = 'no_llgr'

    def __init__(self, parent=None, choice=None, community_type=None):
        super(DeviceBgpCommunity, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('community_type', community_type)

    @property
    def community_type(self):
        # type: () -> Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """community_type getter

        The type of community AS number.

        Returns: Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """
        return self._get_property('community_type')

    @community_type.setter
    def community_type(self, value):
        """community_type setter

        The type of community AS number.

        value: Union[manual_as_number, no_export, no_advertised, no_export_subconfed, llgr_stale, no_llgr]
        """
        self._set_property('community_type', value)

    @property
    def as_number(self):
        # type: () -> DevicePattern
        """as_number getter

        A container for emulated device property patterns.First two octets of 32 bit community AS number

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('as_number', DevicePattern)

    @property
    def as_custom(self):
        # type: () -> DevicePattern
        """as_custom getter

        A container for emulated device property patterns.Last two octets of the community AS number 

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('as_custom', DevicePattern)


class DeviceBgpCommunityList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpCommunityList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpCommunity]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpCommunityList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpCommunity
        return self._next()

    def next(self):
        # type: () -> DeviceBgpCommunity
        return self._next()

    def bgpcommunity(self, community_type=None):
        # type: () -> DeviceBgpCommunityList
        """Factory method that creates an instance of DeviceBgpCommunity class

        BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit AS number and a 16-bit custom value
        """
        item = DeviceBgpCommunity(community_type=community_type)
        self._add(item)
        return self


class DeviceBgpAsPath(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'override_peer_as_set_mode': 'DevicePattern',
        'as_path_segments': 'DeviceBgpAsPathSegmentList',
    }

    DO_NOT_INCLUDE_LOCAL_AS = 'do_not_include_local_as'
    INCLUDE_AS_SEQ = 'include_as_seq'
    INCLUDE_AS_SET = 'include_as_set'
    INCLUDE_AS_CONFED_SEQ = 'include_as_confed_seq'
    INCLUDE_AS_CONFED_SET = 'include_as_confed_set'
    PREPEND_TO_FIRST_SEGMENT = 'prepend_to_first_segment'

    def __init__(self, parent=None, choice=None, as_set_mode=None):
        super(DeviceBgpAsPath, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('as_set_mode', as_set_mode)

    @property
    def override_peer_as_set_mode(self):
        # type: () -> DevicePattern
        """override_peer_as_set_mode getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('override_peer_as_set_mode', DevicePattern)

    @property
    def as_set_mode(self):
        # type: () -> Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """as_set_mode getter

        TBD

        Returns: Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """
        return self._get_property('as_set_mode')

    @as_set_mode.setter
    def as_set_mode(self, value):
        """as_set_mode setter

        TBD

        value: Union[do_not_include_local_as, include_as_seq, include_as_set, include_as_confed_seq, include_as_confed_set, prepend_to_first_segment]
        """
        self._set_property('as_set_mode', value)

    @property
    def as_path_segments(self):
        # type: () -> DeviceBgpAsPathSegmentList
        """as_path_segments getter

        The AS path segments (non random) per route range

        Returns: list[obj(snappi.DeviceBgpAsPathSegment)]
        """
        return self._get_property('as_path_segments', DeviceBgpAsPathSegmentList)


class DeviceBgpAsPathSegment(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    AS_SEQ = 'as_seq'
    AS_SET = 'as_set'
    AS_CONFED_SEQ = 'as_confed_seq'
    AS_CONFED_SET = 'as_confed_set'

    def __init__(self, parent=None, choice=None, segment_type=None, as_numbers=None):
        super(DeviceBgpAsPathSegment, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('segment_type', segment_type)
        self._set_property('as_numbers', as_numbers)

    @property
    def segment_type(self):
        # type: () -> Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """segment_type getter

        as_seq is the most common type of AS_PATH PA, it contains the list of ASNs starting with the most recent ASN being added read from left to right.. The other three AS_PATH types are used for Confederations - AS_SET is the type of AS_PATH attribute that summarizes routes using using the aggregate-address command, allowing AS_PATHs to be summarized in the update as well. - AS_CONFED_SEQ gives the list of ASNs in the path starting with the most recent ASN to be added reading left to right - AS_CONFED_SET will allow summarization of multiple AS PATHs to be sent in BGP Updates.

        Returns: Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """
        return self._get_property('segment_type')

    @segment_type.setter
    def segment_type(self, value):
        """segment_type setter

        as_seq is the most common type of AS_PATH PA, it contains the list of ASNs starting with the most recent ASN being added read from left to right.. The other three AS_PATH types are used for Confederations - AS_SET is the type of AS_PATH attribute that summarizes routes using using the aggregate-address command, allowing AS_PATHs to be summarized in the update as well. - AS_CONFED_SEQ gives the list of ASNs in the path starting with the most recent ASN to be added reading left to right - AS_CONFED_SET will allow summarization of multiple AS PATHs to be sent in BGP Updates.

        value: Union[as_seq, as_set, as_confed_seq, as_confed_set]
        """
        self._set_property('segment_type', value)

    @property
    def as_numbers(self):
        # type: () -> list[int]
        """as_numbers getter

        The AS numbers in this AS path segment. The implementation must correctly assign delimeters between ASNs.

        Returns: list[int]
        """
        return self._get_property('as_numbers')

    @as_numbers.setter
    def as_numbers(self, value):
        """as_numbers setter

        The AS numbers in this AS path segment. The implementation must correctly assign delimeters between ASNs.

        value: list[int]
        """
        self._set_property('as_numbers', value)


class DeviceBgpAsPathSegmentList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpAsPathSegmentList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpAsPathSegment]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpAsPathSegmentList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpAsPathSegment
        return self._next()

    def next(self):
        # type: () -> DeviceBgpAsPathSegment
        return self._next()

    def bgpaspathsegment(self, segment_type='as_set', as_numbers=None):
        # type: () -> DeviceBgpAsPathSegmentList
        """Factory method that creates an instance of DeviceBgpAsPathSegment class

        TBD
        """
        item = DeviceBgpAsPathSegment(segment_type=segment_type, as_numbers=as_numbers)
        self._add(item)
        return self


class DeviceBgpv4RouteRangeList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv4RouteRangeList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv4RouteRange]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv4RouteRangeList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv4RouteRange
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv4RouteRange
        return self._next()

    def bgpv4routerange(self, range_count=1, address_count=1, name=None):
        # type: () -> DeviceBgpv4RouteRangeList
        """Factory method that creates an instance of DeviceBgpv4RouteRange class

        Emulated bgpv4 route ranges. Contains 1..n route ranges. A single route range takes shape as an address/prefix
        """
        item = DeviceBgpv4RouteRange(range_count=range_count, address_count=address_count, name=name)
        self._add(item)
        return self


class DeviceBgpv6RouteRange(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'address_step': 'DevicePattern',
        'prefix': 'DevicePattern',
        'next_hop_address': 'DevicePattern',
        'community': 'DeviceBgpCommunityList',
        'as_path': 'DeviceBgpAsPath',
    }

    def __init__(self, parent=None, choice=None, range_count=None, address_count=None, name=None):
        super(DeviceBgpv6RouteRange, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('range_count', range_count)
        self._set_property('address_count', address_count)
        self._set_property('name', name)

    @property
    def range_count(self):
        # type: () -> int
        """range_count getter

        The number of route ranges per parent bgpv4 device.. If creating sequential routes the range count should default to 1 and the address_count can be used to create a range of . If the parent device_count is 6 and the range_count is 2 that means there will be 2 route_range entries for every device for a total of 12 route ranges. Any child patterns will be applied across the total number of route ranges which implies a pattern count of 12.

        Returns: int
        """
        return self._get_property('range_count')

    @range_count.setter
    def range_count(self, value):
        """range_count setter

        The number of route ranges per parent bgpv4 device.. If creating sequential routes the range count should default to 1 and the address_count can be used to create a range of . If the parent device_count is 6 and the range_count is 2 that means there will be 2 route_range entries for every device for a total of 12 route ranges. Any child patterns will be applied across the total number of route ranges which implies a pattern count of 12.

        value: int
        """
        self._set_property('range_count', value)

    @property
    def address_count(self):
        # type: () -> int
        """address_count getter

        The number of ipv6 addresses in each route range.

        Returns: int
        """
        return self._get_property('address_count')

    @address_count.setter
    def address_count(self, value):
        """address_count setter

        The number of ipv6 addresses in each route range.

        value: int
        """
        self._set_property('address_count', value)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def address_step(self):
        # type: () -> DevicePattern
        """address_step getter

        A container for emulated device property patterns.The amount to increase each address by.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address_step', DevicePattern)

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.Ipv6 prefix length with minimum value is 0 to maximum value is 128

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('prefix', DevicePattern)

    @property
    def next_hop_address(self):
        # type: () -> DevicePattern
        """next_hop_address getter

        A container for emulated device property patterns.IP Address of the next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('next_hop_address', DevicePattern)

    @property
    def community(self):
        # type: () -> DeviceBgpCommunityList
        """community getter

        TBD

        Returns: list[obj(snappi.DeviceBgpCommunity)]
        """
        return self._get_property('community', DeviceBgpCommunityList)

    @property
    def as_path(self):
        # type: () -> DeviceBgpAsPath
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DeviceBgpAsPath)
        """
        return self._get_property('as_path', DeviceBgpAsPath)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv6RouteRangeList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceBgpv6RouteRangeList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[DeviceBgpv6RouteRange]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceBgpv6RouteRangeList
        return self._iter()

    def __next__(self):
        # type: () -> DeviceBgpv6RouteRange
        return self._next()

    def next(self):
        # type: () -> DeviceBgpv6RouteRange
        return self._next()

    def bgpv6routerange(self, range_count=1, address_count=1, name=None):
        # type: () -> DeviceBgpv6RouteRangeList
        """Factory method that creates an instance of DeviceBgpv6RouteRange class

        Emulated bgpv6 route range
        """
        item = DeviceBgpv6RouteRange(range_count=range_count, address_count=address_count, name=name)
        self._add(item)
        return self


class DeviceIpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'gateway': 'DevicePattern',
        'prefix': 'DevicePattern',
        'bgpv6': 'DeviceBgpv6',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceIpv6, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def gateway(self):
        # type: () -> DevicePattern
        """gateway getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('gateway', DevicePattern)

    @property
    def prefix(self):
        # type: () -> DevicePattern
        """prefix getter

        A container for emulated device property patterns.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('prefix', DevicePattern)

    @property
    def bgpv6(self):
        # type: () -> DeviceBgpv6
        """bgpv6 getter

        Emulated BGPv4 router and routes

        Returns: obj(snappi.DeviceBgpv6)
        """
        return self._get_property('bgpv6', DeviceBgpv6)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceBgpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'router_id': 'DevicePattern',
        'as_number': 'DevicePattern',
        'hold_time_interval': 'DevicePattern',
        'keep_alive_interval': 'DevicePattern',
        'dut_ipv6_address': 'DevicePattern',
        'dut_as_number': 'DevicePattern',
        'bgpv4_route_ranges': 'DeviceBgpv4RouteRangeList',
        'bgpv6_route_ranges': 'DeviceBgpv6RouteRangeList',
    }

    IBGP = 'ibgp'
    EBGP = 'ebgp'

    def __init__(self, parent=None, choice=None, as_type=None, name=None):
        super(DeviceBgpv6, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('as_type', as_type)
        self._set_property('name', name)

    @property
    def router_id(self):
        # type: () -> DevicePattern
        """router_id getter

        A container for emulated device property patterns.The BGP router identifier. It must be the string representation of an IPv4 address 

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('router_id', DevicePattern)

    @property
    def as_number(self):
        # type: () -> DevicePattern
        """as_number getter

        A container for emulated device property patterns.Autonomous system (AS) number of 4 byte

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('as_number', DevicePattern)

    @property
    def as_type(self):
        # type: () -> Union[ibgp, ebgp]
        """as_type getter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        Returns: Union[ibgp, ebgp]
        """
        return self._get_property('as_type')

    @as_type.setter
    def as_type(self, value):
        """as_type setter

        The type of BGP autonomous system. External BGP (EBGP) is used for BGP links between two or more autonomous systems. Internal BGP (IBGP) is used within a single autonomous system.

        value: Union[ibgp, ebgp]
        """
        self._set_property('as_type', value)

    @property
    def hold_time_interval(self):
        # type: () -> DevicePattern
        """hold_time_interval getter

        A container for emulated device property patterns.Number of seconds the sender proposes for the value of the Hold Timer

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('hold_time_interval', DevicePattern)

    @property
    def keep_alive_interval(self):
        # type: () -> DevicePattern
        """keep_alive_interval getter

        A container for emulated device property patterns.Number of seconds between transmissions of Keep Alive messages by router

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('keep_alive_interval', DevicePattern)

    @property
    def dut_ipv6_address(self):
        # type: () -> DevicePattern
        """dut_ipv6_address getter

        A container for emulated device property patterns.IPv4 address of the BGP peer for the session

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('dut_ipv6_address', DevicePattern)

    @property
    def dut_as_number(self):
        # type: () -> DevicePattern
        """dut_as_number getter

        A container for emulated device property patterns.Autonomous system (AS) number of the BGP peer router (DUT)

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('dut_as_number', DevicePattern)

    @property
    def bgpv4_route_ranges(self):
        # type: () -> DeviceBgpv4RouteRangeList
        """bgpv4_route_ranges getter

        Emulated bgpv4 route ranges

        Returns: list[obj(snappi.DeviceBgpv4RouteRange)]
        """
        return self._get_property('bgpv4_route_ranges', DeviceBgpv4RouteRangeList)

    @property
    def bgpv6_route_ranges(self):
        # type: () -> DeviceBgpv6RouteRangeList
        """bgpv6_route_ranges getter

        Emulated bgpv6 route ranges

        Returns: list[obj(snappi.DeviceBgpv6RouteRange)]
        """
        return self._get_property('bgpv6_route_ranges', DeviceBgpv6RouteRangeList)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class LagList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(LagList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Lag]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> LagList
        return self._iter()

    def __next__(self):
        # type: () -> Lag
        return self._next()

    def next(self):
        # type: () -> Lag
        return self._next()

    def lag(self, port_names=None, name=None):
        # type: () -> LagList
        """Factory method that creates an instance of Lag class

        A container for LAG settings.
        """
        item = Lag(port_names=port_names, name=name)
        self._add(item)
        return self


class Layer1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'auto_negotiation': 'Layer1AutoNegotiation',
        'flow_control': 'Layer1FlowControl',
    }

    SPEED_10_FD_MBPS = 'speed_10_fd_mbps'
    SPEED_10_HD_MBPS = 'speed_10_hd_mbps'
    SPEED_100_FD_MBPS = 'speed_100_fd_mbps'
    SPEED_100_HD_MBPS = 'speed_100_hd_mbps'
    SPEED_1_GBPS = 'speed_1_gbps'
    SPEED_10_GBPS = 'speed_10_gbps'
    SPEED_25_GBPS = 'speed_25_gbps'
    SPEED_40_GBPS = 'speed_40_gbps'
    SPEED_100_GBPS = 'speed_100_gbps'
    SPEED_200_GBPS = 'speed_200_gbps'
    SPEED_400_GBPS = 'speed_400_gbps'

    COPPER = 'copper'
    FIBER = 'fiber'
    SGMII = 'sgmii'

    def __init__(self, parent=None, choice=None, port_names=None, speed=None, media=None, promiscuous=None, mtu=None, ieee_media_defaults=None, auto_negotiate=None, name=None):
        super(Layer1, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('speed', speed)
        self._set_property('media', media)
        self._set_property('promiscuous', promiscuous)
        self._set_property('mtu', mtu)
        self._set_property('ieee_media_defaults', ieee_media_defaults)
        self._set_property('auto_negotiate', auto_negotiate)
        self._set_property('name', name)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        A list of unique names of port objects that will share the choice settings. 

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will share the choice settings. 

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def speed(self):
        # type: () -> Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """speed getter

        Set the speed if supported.

        Returns: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        return self._get_property('speed')

    @speed.setter
    def speed(self, value):
        """speed setter

        Set the speed if supported.

        value: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        self._set_property('speed', value)

    @property
    def media(self):
        # type: () -> Union[copper, fiber, sgmii]
        """media getter

        Set the type of media interface if supported.

        Returns: Union[copper, fiber, sgmii]
        """
        return self._get_property('media')

    @media.setter
    def media(self, value):
        """media setter

        Set the type of media interface if supported.

        value: Union[copper, fiber, sgmii]
        """
        self._set_property('media', value)

    @property
    def promiscuous(self):
        # type: () -> boolean
        """promiscuous getter

        Enable promiscuous mode if supported.

        Returns: boolean
        """
        return self._get_property('promiscuous')

    @promiscuous.setter
    def promiscuous(self, value):
        """promiscuous setter

        Enable promiscuous mode if supported.

        value: boolean
        """
        self._set_property('promiscuous', value)

    @property
    def mtu(self):
        # type: () -> int
        """mtu getter

        Set the maximum transmission unit size if supported.

        Returns: int
        """
        return self._get_property('mtu')

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Set the maximum transmission unit size if supported.

        value: int
        """
        self._set_property('mtu', value)

    @property
    def ieee_media_defaults(self):
        # type: () -> boolean
        """ieee_media_defaults getter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        Returns: boolean
        """
        return self._get_property('ieee_media_defaults')

    @ieee_media_defaults.setter
    def ieee_media_defaults(self, value):
        """ieee_media_defaults setter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        value: boolean
        """
        self._set_property('ieee_media_defaults', value)

    @property
    def auto_negotiate(self):
        # type: () -> boolean
        """auto_negotiate getter

        Enable/disable auto negotiation.

        Returns: boolean
        """
        return self._get_property('auto_negotiate')

    @auto_negotiate.setter
    def auto_negotiate(self, value):
        """auto_negotiate setter

        Enable/disable auto negotiation.

        value: boolean
        """
        self._set_property('auto_negotiate', value)

    @property
    def auto_negotiation(self):
        # type: () -> Layer1AutoNegotiation
        """auto_negotiation getter

        Container for auto negotiation settings

        Returns: obj(snappi.Layer1AutoNegotiation)
        """
        return self._get_property('auto_negotiation', Layer1AutoNegotiation)

    @property
    def flow_control(self):
        # type: () -> Layer1FlowControl
        """flow_control getter

        A container for layer1 receive flow control settings. To enable flow control settings on ports this object must be a valid object not a null value.

        Returns: obj(snappi.Layer1FlowControl)
        """
        return self._get_property('flow_control', Layer1FlowControl)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class Layer1AutoNegotiation(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, advertise_1000_mbps=None, advertise_100_fd_mbps=None, advertise_100_hd_mbps=None, advertise_10_fd_mbps=None, advertise_10_hd_mbps=None, link_training=None, rs_fec=None):
        super(Layer1AutoNegotiation, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('advertise_1000_mbps', advertise_1000_mbps)
        self._set_property('advertise_100_fd_mbps', advertise_100_fd_mbps)
        self._set_property('advertise_100_hd_mbps', advertise_100_hd_mbps)
        self._set_property('advertise_10_fd_mbps', advertise_10_fd_mbps)
        self._set_property('advertise_10_hd_mbps', advertise_10_hd_mbps)
        self._set_property('link_training', link_training)
        self._set_property('rs_fec', rs_fec)

    @property
    def advertise_1000_mbps(self):
        # type: () -> boolean
        """advertise_1000_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_1000_mbps')

    @advertise_1000_mbps.setter
    def advertise_1000_mbps(self, value):
        """advertise_1000_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_1000_mbps', value)

    @property
    def advertise_100_fd_mbps(self):
        # type: () -> boolean
        """advertise_100_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_100_fd_mbps')

    @advertise_100_fd_mbps.setter
    def advertise_100_fd_mbps(self, value):
        """advertise_100_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_100_fd_mbps', value)

    @property
    def advertise_100_hd_mbps(self):
        # type: () -> boolean
        """advertise_100_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_100_hd_mbps')

    @advertise_100_hd_mbps.setter
    def advertise_100_hd_mbps(self, value):
        """advertise_100_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_100_hd_mbps', value)

    @property
    def advertise_10_fd_mbps(self):
        # type: () -> boolean
        """advertise_10_fd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_10_fd_mbps')

    @advertise_10_fd_mbps.setter
    def advertise_10_fd_mbps(self, value):
        """advertise_10_fd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_10_fd_mbps', value)

    @property
    def advertise_10_hd_mbps(self):
        # type: () -> boolean
        """advertise_10_hd_mbps getter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        Returns: boolean
        """
        return self._get_property('advertise_10_hd_mbps')

    @advertise_10_hd_mbps.setter
    def advertise_10_hd_mbps(self, value):
        """advertise_10_hd_mbps setter

        If auto_negotiate is true and the interface supports this option then this speed will be advertised.

        value: boolean
        """
        self._set_property('advertise_10_hd_mbps', value)

    @property
    def link_training(self):
        # type: () -> boolean
        """link_training getter

        Enable/disable gigabit ethernet link training.

        Returns: boolean
        """
        return self._get_property('link_training')

    @link_training.setter
    def link_training(self, value):
        """link_training setter

        Enable/disable gigabit ethernet link training.

        value: boolean
        """
        self._set_property('link_training', value)

    @property
    def rs_fec(self):
        # type: () -> boolean
        """rs_fec getter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        Returns: boolean
        """
        return self._get_property('rs_fec')

    @rs_fec.setter
    def rs_fec(self, value):
        """rs_fec setter

        Enable/disable gigabit ethernet reed solomon forward error correction (RS FEC).

        value: boolean
        """
        self._set_property('rs_fec', value)


class Layer1FlowControl(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ieee_802_1qbb': 'Layer1Ieee8021qbb',
        'ieee_802_3x': 'Layer1Ieee8023x',
    }

    IEEE_802_1QBB = 'ieee_802_1qbb'
    IEEE_802_3X = 'ieee_802_3x'

    def __init__(self, parent=None, choice=None, directed_address=None):
        super(Layer1FlowControl, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('directed_address', directed_address)

    @property
    def ieee_802_1qbb(self):
        # type: () -> Layer1Ieee8021qbb
        """Factory property that returns an instance of the Layer1Ieee8021qbb class

        These settings enhance the existing 802.3x pause priority capabilities to enable flow control based on 802.1p priorities (classes of service). 
        """
        return self._get_property('ieee_802_1qbb', Layer1Ieee8021qbb(self, 'ieee_802_1qbb'))

    @property
    def ieee_802_3x(self):
        # type: () -> Layer1Ieee8023x
        """Factory property that returns an instance of the Layer1Ieee8023x class

        A container for ieee 802.3x rx pause settings
        """
        return self._get_property('ieee_802_3x', Layer1Ieee8023x(self, 'ieee_802_3x'))

    @property
    def directed_address(self):
        # type: () -> str
        """directed_address getter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        Returns: str
        """
        return self._get_property('directed_address')

    @directed_address.setter
    def directed_address(self, value):
        """directed_address setter

        The 48bit mac address that the layer1 port names will listen on for a directed pause. 

        value: str
        """
        self._set_property('directed_address', value)

    @property
    def choice(self):
        # type: () -> Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """choice getter

        The type of priority flow control.

        Returns: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of priority flow control.

        value: Union[ieee_802_1qbb, ieee_802_3x, choice, choice, choice]
        """
        self._set_property('choice', value)


class Layer1Ieee8021qbb(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, pfc_delay=None, pfc_class_0=None, pfc_class_1=None, pfc_class_2=None, pfc_class_3=None, pfc_class_4=None, pfc_class_5=None, pfc_class_6=None, pfc_class_7=None):
        super(Layer1Ieee8021qbb, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('pfc_delay', pfc_delay)
        self._set_property('pfc_class_0', pfc_class_0)
        self._set_property('pfc_class_1', pfc_class_1)
        self._set_property('pfc_class_2', pfc_class_2)
        self._set_property('pfc_class_3', pfc_class_3)
        self._set_property('pfc_class_4', pfc_class_4)
        self._set_property('pfc_class_5', pfc_class_5)
        self._set_property('pfc_class_6', pfc_class_6)
        self._set_property('pfc_class_7', pfc_class_7)

    @property
    def pfc_delay(self):
        # type: () -> int
        """pfc_delay getter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        Returns: int
        """
        return self._get_property('pfc_delay')

    @pfc_delay.setter
    def pfc_delay(self, value):
        """pfc_delay setter

        The upper limit on the transmit time of a queue after receiving a message to pause a specified priority. A value of 0 or null indicates that pfc delay will not be enabled. 

        value: int
        """
        self._set_property('pfc_delay', value)

    @property
    def pfc_class_0(self):
        # type: () -> int
        """pfc_class_0 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_0')

    @pfc_class_0.setter
    def pfc_class_0(self, value):
        """pfc_class_0 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_0', value)

    @property
    def pfc_class_1(self):
        # type: () -> int
        """pfc_class_1 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_1')

    @pfc_class_1.setter
    def pfc_class_1(self, value):
        """pfc_class_1 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_1', value)

    @property
    def pfc_class_2(self):
        # type: () -> int
        """pfc_class_2 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_2')

    @pfc_class_2.setter
    def pfc_class_2(self, value):
        """pfc_class_2 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_2', value)

    @property
    def pfc_class_3(self):
        # type: () -> int
        """pfc_class_3 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_3')

    @pfc_class_3.setter
    def pfc_class_3(self, value):
        """pfc_class_3 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_3', value)

    @property
    def pfc_class_4(self):
        # type: () -> int
        """pfc_class_4 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_4')

    @pfc_class_4.setter
    def pfc_class_4(self, value):
        """pfc_class_4 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_4', value)

    @property
    def pfc_class_5(self):
        # type: () -> int
        """pfc_class_5 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_5')

    @pfc_class_5.setter
    def pfc_class_5(self, value):
        """pfc_class_5 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_5', value)

    @property
    def pfc_class_6(self):
        # type: () -> int
        """pfc_class_6 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_6')

    @pfc_class_6.setter
    def pfc_class_6(self, value):
        """pfc_class_6 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_6', value)

    @property
    def pfc_class_7(self):
        # type: () -> int
        """pfc_class_7 getter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        Returns: int
        """
        return self._get_property('pfc_class_7')

    @pfc_class_7.setter
    def pfc_class_7(self, value):
        """pfc_class_7 setter

        The valid values are null, 0 - 7. A null value indicates there is no setting for this pfc class.

        value: int
        """
        self._set_property('pfc_class_7', value)


class Layer1Ieee8023x(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None):
        super(Layer1Ieee8023x, self).__init__()
        self._parent = parent
        self._choice = choice


class Layer1List(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(Layer1List, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Layer1]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Layer1List
        return self._iter()

    def __next__(self):
        # type: () -> Layer1
        return self._next()

    def next(self):
        # type: () -> Layer1
        return self._next()

    def layer1(self, port_names=None, speed='speed_10_gbps', media=None, promiscuous=False, mtu=1500, ieee_media_defaults=True, auto_negotiate=True, name=None):
        # type: () -> Layer1List
        """Factory method that creates an instance of Layer1 class

        A container for layer1 settings.
        """
        item = Layer1(port_names=port_names, speed=speed, media=media, promiscuous=promiscuous, mtu=mtu, ieee_media_defaults=ieee_media_defaults, auto_negotiate=auto_negotiate, name=name)
        self._add(item)
        return self


class Capture(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'filters': 'CaptureFilterList',
    }

    PCAP = 'pcap'
    PCAPNG = 'pcapng'

    def __init__(self, parent=None, choice=None, port_names=None, overwrite=None, packet_size=None, format=None, name=None):
        super(Capture, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('overwrite', overwrite)
        self._set_property('packet_size', packet_size)
        self._set_property('format', format)
        self._set_property('name', name)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The unique names of ports that the capture settings will apply to. Port_names cannot be duplicated between capture objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The unique names of ports that the capture settings will apply to. Port_names cannot be duplicated between capture objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def filters(self):
        # type: () -> CaptureFilterList
        """filters getter

        A list of filters to apply to the capturing ports. If no filters are specified then all packets will be captured. A capture can have multiple filters. The number of filters supported is determined by the implementation which can be retrieved using the capabilities API.. When multiple filters are specified the capture implementation must && (and) all the filters.

        Returns: list[obj(snappi.CaptureFilter)]
        """
        return self._get_property('filters', CaptureFilterList)

    @property
    def overwrite(self):
        # type: () -> boolean
        """overwrite getter

        Overwrite the capture buffer.

        Returns: boolean
        """
        return self._get_property('overwrite')

    @overwrite.setter
    def overwrite(self, value):
        """overwrite setter

        Overwrite the capture buffer.

        value: boolean
        """
        self._set_property('overwrite', value)

    @property
    def packet_size(self):
        # type: () -> int
        """packet_size getter

        The maximum size of each captured packet. If no value is specified or it is null then the entire packet will be captured.

        Returns: int
        """
        return self._get_property('packet_size')

    @packet_size.setter
    def packet_size(self, value):
        """packet_size setter

        The maximum size of each captured packet. If no value is specified or it is null then the entire packet will be captured.

        value: int
        """
        self._set_property('packet_size', value)

    @property
    def format(self):
        # type: () -> Union[pcap, pcapng]
        """format getter

        The format of the capture file.

        Returns: Union[pcap, pcapng]
        """
        return self._get_property('format')

    @format.setter
    def format(self, value):
        """format setter

        The format of the capture file.

        value: Union[pcap, pcapng]
        """
        self._set_property('format', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class CaptureFilter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'custom': 'CaptureCustom',
        'ethernet': 'CaptureEthernet',
        'vlan': 'CaptureVlan',
        'ipv4': 'CaptureIpv4',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    IPV4 = 'ipv4'

    def __init__(self, parent=None, choice=None):
        super(CaptureFilter, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def custom(self):
        # type: () -> CaptureCustom
        """Factory property that returns an instance of the CaptureCustom class

        TBD
        """
        return self._get_property('custom', CaptureCustom(self, 'custom'))

    @property
    def ethernet(self):
        # type: () -> CaptureEthernet
        """Factory property that returns an instance of the CaptureEthernet class

        TBD
        """
        return self._get_property('ethernet', CaptureEthernet(self, 'ethernet'))

    @property
    def vlan(self):
        # type: () -> CaptureVlan
        """Factory property that returns an instance of the CaptureVlan class

        TBD
        """
        return self._get_property('vlan', CaptureVlan(self, 'vlan'))

    @property
    def ipv4(self):
        # type: () -> CaptureIpv4
        """Factory property that returns an instance of the CaptureIpv4 class

        TBD
        """
        return self._get_property('ipv4', CaptureIpv4(self, 'ipv4'))

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, ipv4, choice, choice, choice]
        """
        self._set_property('choice', value)


class CaptureCustom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, offset=None, value=None, mask=None, negate=None):
        super(CaptureCustom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('offset', offset)
        self._set_property('value', value)
        self._set_property('mask', mask)
        self._set_property('negate', negate)

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        The byte offset to filter on

        Returns: int
        """
        return self._get_property('offset')

    @offset.setter
    def offset(self, value):
        """offset setter

        The byte offset to filter on

        value: int
        """
        self._set_property('offset', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value)

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        TBD

        Returns: str
        """
        return self._get_property('mask')

    @mask.setter
    def mask(self, value):
        """mask setter

        TBD

        value: str
        """
        self._set_property('mask', value)

    @property
    def negate(self):
        # type: () -> boolean
        """negate getter

        TBD

        Returns: boolean
        """
        return self._get_property('negate')

    @negate.setter
    def negate(self, value):
        """negate setter

        TBD

        value: boolean
        """
        self._set_property('negate', value)


class CaptureEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src': 'CaptureField',
        'dst': 'CaptureField',
        'ether_type': 'CaptureField',
        'pfc_queue': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureEthernet, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src(self):
        # type: () -> CaptureField
        """src getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('src', CaptureField)

    @property
    def dst(self):
        # type: () -> CaptureField
        """dst getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dst', CaptureField)

    @property
    def ether_type(self):
        # type: () -> CaptureField
        """ether_type getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('ether_type', CaptureField)

    @property
    def pfc_queue(self):
        # type: () -> CaptureField
        """pfc_queue getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('pfc_queue', CaptureField)


class CaptureField(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, value=None, mask=None, negate=None):
        super(CaptureField, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('value', value)
        self._set_property('mask', mask)
        self._set_property('negate', negate)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value)

    @property
    def mask(self):
        # type: () -> str
        """mask getter

        TBD

        Returns: str
        """
        return self._get_property('mask')

    @mask.setter
    def mask(self, value):
        """mask setter

        TBD

        value: str
        """
        self._set_property('mask', value)

    @property
    def negate(self):
        # type: () -> boolean
        """negate getter

        TBD

        Returns: boolean
        """
        return self._get_property('negate')

    @negate.setter
    def negate(self, value):
        """negate setter

        TBD

        value: boolean
        """
        self._set_property('negate', value)


class CaptureVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'priority': 'CaptureField',
        'cfi': 'CaptureField',
        'id': 'CaptureField',
        'protocol': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureVlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def priority(self):
        # type: () -> CaptureField
        """priority getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('priority', CaptureField)

    @property
    def cfi(self):
        # type: () -> CaptureField
        """cfi getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('cfi', CaptureField)

    @property
    def id(self):
        # type: () -> CaptureField
        """id getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('id', CaptureField)

    @property
    def protocol(self):
        # type: () -> CaptureField
        """protocol getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('protocol', CaptureField)


class CaptureIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'CaptureField',
        'headeer_length': 'CaptureField',
        'priority': 'CaptureField',
        'total_length': 'CaptureField',
        'identification': 'CaptureField',
        'reserved': 'CaptureField',
        'dont_fragment': 'CaptureField',
        'more_fragments': 'CaptureField',
        'fragment_offset': 'CaptureField',
        'time_to_live': 'CaptureField',
        'protocol': 'CaptureField',
        'header_checksum': 'CaptureField',
        'src': 'CaptureField',
        'dst': 'CaptureField',
    }

    def __init__(self, parent=None, choice=None):
        super(CaptureIpv4, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> CaptureField
        """version getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('version', CaptureField)

    @property
    def headeer_length(self):
        # type: () -> CaptureField
        """headeer_length getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('headeer_length', CaptureField)

    @property
    def priority(self):
        # type: () -> CaptureField
        """priority getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('priority', CaptureField)

    @property
    def total_length(self):
        # type: () -> CaptureField
        """total_length getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('total_length', CaptureField)

    @property
    def identification(self):
        # type: () -> CaptureField
        """identification getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('identification', CaptureField)

    @property
    def reserved(self):
        # type: () -> CaptureField
        """reserved getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('reserved', CaptureField)

    @property
    def dont_fragment(self):
        # type: () -> CaptureField
        """dont_fragment getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dont_fragment', CaptureField)

    @property
    def more_fragments(self):
        # type: () -> CaptureField
        """more_fragments getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('more_fragments', CaptureField)

    @property
    def fragment_offset(self):
        # type: () -> CaptureField
        """fragment_offset getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('fragment_offset', CaptureField)

    @property
    def time_to_live(self):
        # type: () -> CaptureField
        """time_to_live getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('time_to_live', CaptureField)

    @property
    def protocol(self):
        # type: () -> CaptureField
        """protocol getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('protocol', CaptureField)

    @property
    def header_checksum(self):
        # type: () -> CaptureField
        """header_checksum getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('header_checksum', CaptureField)

    @property
    def src(self):
        # type: () -> CaptureField
        """src getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('src', CaptureField)

    @property
    def dst(self):
        # type: () -> CaptureField
        """dst getter

        

        Returns: obj(snappi.CaptureField)
        """
        return self._get_property('dst', CaptureField)


class CaptureFilterList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(CaptureFilterList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[CaptureCustom, CaptureVlan, CaptureIpv4, CaptureEthernet, CaptureFilter]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureFilterList
        return self._iter()

    def __next__(self):
        # type: () -> CaptureFilter
        return self._next()

    def next(self):
        # type: () -> CaptureFilter
        return self._next()

    def filter(self):
        # type: () -> CaptureFilterList
        """Factory method that creates an instance of CaptureFilter class

        Container for capture filters
        """
        item = CaptureFilter()
        self._add(item)
        return self

    def custom(self, offset=None, value=None, mask=None, negate=False):
        # type: () -> CaptureFilterList
        """Factory method that creates an instance of CaptureCustom class

        TBD
        """
        item = CaptureFilter()
        item.custom
        item.choice = 'custom'
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> CaptureFilterList
        """Factory method that creates an instance of CaptureEthernet class

        TBD
        """
        item = CaptureFilter()
        item.ethernet
        item.choice = 'ethernet'
        self._add(item)
        return self

    def vlan(self):
        # type: () -> CaptureFilterList
        """Factory method that creates an instance of CaptureVlan class

        TBD
        """
        item = CaptureFilter()
        item.vlan
        item.choice = 'vlan'
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> CaptureFilterList
        """Factory method that creates an instance of CaptureIpv4 class

        TBD
        """
        item = CaptureFilter()
        item.ipv4
        item.choice = 'ipv4'
        self._add(item)
        return self


class CaptureList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(CaptureList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Capture]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> CaptureList
        return self._iter()

    def __next__(self):
        # type: () -> Capture
        return self._next()

    def next(self):
        # type: () -> Capture
        return self._next()

    def capture(self, port_names=None, overwrite=False, packet_size=None, format='pcap', name=None):
        # type: () -> CaptureList
        """Factory method that creates an instance of Capture class

        Container for capture settings.
        """
        item = Capture(port_names=port_names, overwrite=overwrite, packet_size=packet_size, format=format, name=name)
        self._add(item)
        return self


class Device(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'ethernet': 'DeviceEthernet',
        'ipv4_loopback': 'DeviceIpv4Loopback',
        'ipv6_loopback': 'DeviceIpv6Loopback',
    }

    def __init__(self, parent=None, choice=None, container_name=None, device_count=None, name=None):
        super(Device, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('container_name', container_name)
        self._set_property('device_count', device_count)
        self._set_property('name', name)

    @property
    def container_name(self):
        # type: () -> str
        """container_name getter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        Returns: str
        """
        return self._get_property('container_name')

    @container_name.setter
    def container_name(self, value):
        """container_name setter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        value: str
        """
        self._set_property('container_name', value)

    @property
    def device_count(self):
        # type: () -> int
        """device_count getter

        The number of emulated protocol devices or interfaces per port.. For example if the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        Returns: int
        """
        return self._get_property('device_count')

    @device_count.setter
    def device_count(self, value):
        """device_count setter

        The number of emulated protocol devices or interfaces per port.. For example if the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        value: int
        """
        self._set_property('device_count', value)

    @property
    def ethernet(self):
        # type: () -> DeviceEthernet
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.The ethernet stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        return self._get_property('ethernet', DeviceEthernet)

    @property
    def ipv4_loopback(self):
        # type: () -> DeviceIpv4Loopback
        """ipv4_loopback getter

        Emulated ipv4 loopback interfaceThe ipv4 loopback stack.

        Returns: obj(snappi.DeviceIpv4Loopback)
        """
        return self._get_property('ipv4_loopback', DeviceIpv4Loopback)

    @property
    def ipv6_loopback(self):
        # type: () -> DeviceIpv6Loopback
        """ipv6_loopback getter

        Emulated ipv6 loopback interfaceThe ipv4 loopback stack.

        Returns: obj(snappi.DeviceIpv6Loopback)
        """
        return self._get_property('ipv6_loopback', DeviceIpv6Loopback)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceIpv4Loopback(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'bgpv4': 'DeviceBgpv4',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceIpv4Loopback, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def bgpv4(self):
        # type: () -> DeviceBgpv4
        """bgpv4 getter

        Emulated BGPv4 routerThe bgpv4 device.

        Returns: obj(snappi.DeviceBgpv4)
        """
        return self._get_property('bgpv4', DeviceBgpv4)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceIpv6Loopback(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'DevicePattern',
        'bgpv6': 'DeviceBgpv6',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(DeviceIpv6Loopback, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def address(self):
        # type: () -> DevicePattern
        """address getter

        A container for emulated device property patterns.The ipv6 address.

        Returns: obj(snappi.DevicePattern)
        """
        return self._get_property('address', DevicePattern)

    @property
    def bgpv6(self):
        # type: () -> DeviceBgpv6
        """bgpv6 getter

        Emulated BGPv4 router and routesThe bgpv6 device.

        Returns: obj(snappi.DeviceBgpv6)
        """
        return self._get_property('bgpv6', DeviceBgpv6)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class DeviceList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(DeviceList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Device]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> DeviceList
        return self._iter()

    def __next__(self):
        # type: () -> Device
        return self._next()

    def next(self):
        # type: () -> Device
        return self._next()

    def device(self, container_name=None, device_count=1, name=None):
        # type: () -> DeviceList
        """Factory method that creates an instance of Device class

        A container for emulated protocol devices.
        """
        item = Device(container_name=container_name, device_count=device_count, name=name)
        self._add(item)
        return self


class Flow(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'tx_rx': 'FlowTxRx',
        'packet': 'FlowHeaderList',
        'size': 'FlowSize',
        'rate': 'FlowRate',
        'duration': 'FlowDuration',
    }

    def __init__(self, parent=None, choice=None, name=None):
        super(Flow, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)

    @property
    def tx_rx(self):
        # type: () -> FlowTxRx
        """tx_rx getter

        A container for different types of transmit and receive endpoint containers.The transmit and receive endpoints.

        Returns: obj(snappi.FlowTxRx)
        """
        return self._get_property('tx_rx', FlowTxRx)

    @property
    def packet(self):
        # type: () -> FlowHeaderList
        """packet getter

        The header is a list of traffic protocol headers. The order of traffic protocol headers assigned to the list is the order they will appear on the wire.

        Returns: list[obj(snappi.FlowHeader)]
        """
        return self._get_property('packet', FlowHeaderList)

    @property
    def size(self):
        # type: () -> FlowSize
        """size getter

        The frame size which overrides the total length of the packetThe size of the packets.

        Returns: obj(snappi.FlowSize)
        """
        return self._get_property('size', FlowSize)

    @property
    def rate(self):
        # type: () -> FlowRate
        """rate getter

        The rate of packet transmissionThe transmit rate of the packets.

        Returns: obj(snappi.FlowRate)
        """
        return self._get_property('rate', FlowRate)

    @property
    def duration(self):
        # type: () -> FlowDuration
        """duration getter

        A container for different transmit durations. The transmit duration of the packets.

        Returns: obj(snappi.FlowDuration)
        """
        return self._get_property('duration', FlowDuration)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._set_property('name', value)


class FlowTxRx(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port': 'FlowPort',
        'device': 'FlowDevice',
    }

    PORT = 'port'
    DEVICE = 'device'

    def __init__(self, parent=None, choice=None):
        super(FlowTxRx, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port(self):
        # type: () -> FlowPort
        """Factory property that returns an instance of the FlowPort class

        A container for a transmit port and 0..n intended receive ports. When assigning this container to a flow the flows's packet headers will not be populated with any address resolution information such as source and/or destination addresses. For example Flow.Ethernet dst mac address values will be defaulted to 0. For full control over the Flow.properties.packet header contents use this container. 
        """
        return self._get_property('port', FlowPort(self, 'port'))

    @property
    def device(self):
        # type: () -> FlowDevice
        """Factory property that returns an instance of the FlowDevice class

        A container for 1..n transmit devices and 1..n receive devices. Implemementations may use learned information from the devices to pre-populate Flow.properties.packet[Flow.Header fields].. For example an implementation may automatically start devices, get arp table information and pre-populate the Flow.Ethernet dst mac address values.. To discover what the implementation supports use the /results/capabilities API.
        """
        return self._get_property('device', FlowDevice(self, 'device'))

    @property
    def choice(self):
        # type: () -> Union[port, device, choice, choice, choice]
        """choice getter

        The type of transmit and receive container used by the flow.

        Returns: Union[port, device, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of transmit and receive container used by the flow.

        value: Union[port, device, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowPort(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, tx_name=None, rx_name=None):
        super(FlowPort, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('tx_name', tx_name)
        self._set_property('rx_name', rx_name)

    @property
    def tx_name(self):
        # type: () -> str
        """tx_name getter

        The unique name of a port that is the transmit port.

        Returns: str
        """
        return self._get_property('tx_name')

    @tx_name.setter
    def tx_name(self, value):
        """tx_name setter

        The unique name of a port that is the transmit port.

        value: str
        """
        self._set_property('tx_name', value)

    @property
    def rx_name(self):
        # type: () -> str
        """rx_name getter

        The unique name of a port that is the intended receive port.

        Returns: str
        """
        return self._get_property('rx_name')

    @rx_name.setter
    def rx_name(self, value):
        """rx_name setter

        The unique name of a port that is the intended receive port.

        value: str
        """
        self._set_property('rx_name', value)


class FlowDevice(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, tx_names=None, rx_names=None):
        super(FlowDevice, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('tx_names', tx_names)
        self._set_property('rx_names', rx_names)

    @property
    def tx_names(self):
        # type: () -> list[str]
        """tx_names getter

        The unique names of devices that will be transmitting.

        Returns: list[str]
        """
        return self._get_property('tx_names')

    @tx_names.setter
    def tx_names(self, value):
        """tx_names setter

        The unique names of devices that will be transmitting.

        value: list[str]
        """
        self._set_property('tx_names', value)

    @property
    def rx_names(self):
        # type: () -> list[str]
        """rx_names getter

        The unique names of emulated devices that will be receiving.

        Returns: list[str]
        """
        return self._get_property('rx_names')

    @rx_names.setter
    def rx_names(self, value):
        """rx_names setter

        The unique names of emulated devices that will be receiving.

        value: list[str]
        """
        self._set_property('rx_names', value)


class FlowHeader(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'custom': 'FlowCustom',
        'ethernet': 'FlowEthernet',
        'vlan': 'FlowVlan',
        'vxlan': 'FlowVxlan',
        'ipv4': 'FlowIpv4',
        'ipv6': 'FlowIpv6',
        'pfcpause': 'FlowPfcPause',
        'ethernetpause': 'FlowEthernetPause',
        'tcp': 'FlowTcp',
        'udp': 'FlowUdp',
        'gre': 'FlowGre',
        'gtpv1': 'FlowGtpv1',
        'gtpv2': 'FlowGtpv2',
        'arp': 'FlowArp',
        'ppp': 'FlowPpp',
        'igmpv1': 'FlowIgmpv1',
    }

    CUSTOM = 'custom'
    ETHERNET = 'ethernet'
    VLAN = 'vlan'
    VXLAN = 'vxlan'
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'
    PFCPAUSE = 'pfcpause'
    ETHERNETPAUSE = 'ethernetpause'
    TCP = 'tcp'
    UDP = 'udp'
    GRE = 'gre'
    GTPV1 = 'gtpv1'
    GTPV2 = 'gtpv2'
    ARP = 'arp'
    PPP = 'ppp'
    IGMPV1 = 'igmpv1'

    def __init__(self, parent=None, choice=None):
        super(FlowHeader, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def custom(self):
        # type: () -> FlowCustom
        """Factory property that returns an instance of the FlowCustom class

        Custom packet header
        """
        return self._get_property('custom', FlowCustom(self, 'custom'))

    @property
    def ethernet(self):
        # type: () -> FlowEthernet
        """Factory property that returns an instance of the FlowEthernet class

        Ethernet packet header
        """
        return self._get_property('ethernet', FlowEthernet(self, 'ethernet'))

    @property
    def vlan(self):
        # type: () -> FlowVlan
        """Factory property that returns an instance of the FlowVlan class

        VLAN packet header
        """
        return self._get_property('vlan', FlowVlan(self, 'vlan'))

    @property
    def vxlan(self):
        # type: () -> FlowVxlan
        """Factory property that returns an instance of the FlowVxlan class

        Vxlan packet header
        """
        return self._get_property('vxlan', FlowVxlan(self, 'vxlan'))

    @property
    def ipv4(self):
        # type: () -> FlowIpv4
        """Factory property that returns an instance of the FlowIpv4 class

        IPv4 packet header
        """
        return self._get_property('ipv4', FlowIpv4(self, 'ipv4'))

    @property
    def ipv6(self):
        # type: () -> FlowIpv6
        """Factory property that returns an instance of the FlowIpv6 class

        IPv6 packet header
        """
        return self._get_property('ipv6', FlowIpv6(self, 'ipv6'))

    @property
    def pfcpause(self):
        # type: () -> FlowPfcPause
        """Factory property that returns an instance of the FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        return self._get_property('pfcpause', FlowPfcPause(self, 'pfcpause'))

    @property
    def ethernetpause(self):
        # type: () -> FlowEthernetPause
        """Factory property that returns an instance of the FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        return self._get_property('ethernetpause', FlowEthernetPause(self, 'ethernetpause'))

    @property
    def tcp(self):
        # type: () -> FlowTcp
        """Factory property that returns an instance of the FlowTcp class

        TCP packet header
        """
        return self._get_property('tcp', FlowTcp(self, 'tcp'))

    @property
    def udp(self):
        # type: () -> FlowUdp
        """Factory property that returns an instance of the FlowUdp class

        UDP packet header
        """
        return self._get_property('udp', FlowUdp(self, 'udp'))

    @property
    def gre(self):
        # type: () -> FlowGre
        """Factory property that returns an instance of the FlowGre class

        GRE packet header
        """
        return self._get_property('gre', FlowGre(self, 'gre'))

    @property
    def gtpv1(self):
        # type: () -> FlowGtpv1
        """Factory property that returns an instance of the FlowGtpv1 class

        GTPv1 packet header
        """
        return self._get_property('gtpv1', FlowGtpv1(self, 'gtpv1'))

    @property
    def gtpv2(self):
        # type: () -> FlowGtpv2
        """Factory property that returns an instance of the FlowGtpv2 class

        GTPv2 packet header
        """
        return self._get_property('gtpv2', FlowGtpv2(self, 'gtpv2'))

    @property
    def arp(self):
        # type: () -> FlowArp
        """Factory property that returns an instance of the FlowArp class

        ARP packet header
        """
        return self._get_property('arp', FlowArp(self, 'arp'))

    @property
    def ppp(self):
        # type: () -> FlowPpp
        """Factory property that returns an instance of the FlowPpp class

        PPP packet header
        """
        return self._get_property('ppp', FlowPpp(self, 'ppp'))

    @property
    def igmpv1(self):
        # type: () -> FlowIgmpv1
        """Factory property that returns an instance of the FlowIgmpv1 class

        IGMPv1 packet header
        """
        return self._get_property('igmpv1', FlowIgmpv1(self, 'igmpv1'))

    @property
    def choice(self):
        # type: () -> Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, ppp, igmpv1, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, ppp, igmpv1, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, arp, ppp, igmpv1, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowCustom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'patterns': 'FlowBitPatternList',
    }

    def __init__(self, parent=None, choice=None, bytes=None):
        super(FlowCustom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('bytes', bytes)

    @property
    def bytes(self):
        # type: () -> str
        """bytes getter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        Returns: str
        """
        return self._get_property('bytes')

    @bytes.setter
    def bytes(self, value):
        """bytes setter

        A custom packet header defined as a string of hex bytes. The string MUST contain valid hex characters. Spaces or colons can be part of the bytes but will be discarded This can be used to create a custom protocol from other inputs such as scapy, wireshark, pcap etc.. An example of ethernet/ipv4: '00000000000200000000000108004500001400010000400066e70a0000010a000002'

        value: str
        """
        self._set_property('bytes', value)

    @property
    def patterns(self):
        # type: () -> FlowBitPatternList
        """patterns getter

        Modify the bytes with bit based patterns

        Returns: list[obj(snappi.FlowBitPattern)]
        """
        return self._get_property('patterns', FlowBitPatternList)


class FlowBitPattern(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'bitlist': 'FlowBitList',
        'bitcounter': 'FlowBitCounter',
    }

    BITLIST = 'bitlist'
    BITCOUNTER = 'bitcounter'

    def __init__(self, parent=None, choice=None):
        super(FlowBitPattern, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def bitlist(self):
        # type: () -> FlowBitList
        """Factory property that returns an instance of the FlowBitList class

        A pattern which is a list of values.
        """
        return self._get_property('bitlist', FlowBitList(self, 'bitlist'))

    @property
    def bitcounter(self):
        # type: () -> FlowBitCounter
        """Factory property that returns an instance of the FlowBitCounter class

        An incrementing pattern
        """
        return self._get_property('bitcounter', FlowBitCounter(self, 'bitcounter'))

    @property
    def choice(self):
        # type: () -> Union[bitlist, bitcounter, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[bitlist, bitcounter, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[bitlist, bitcounter, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowBitList(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, offset=None, length=None, count=None, values=None):
        super(FlowBitList, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('offset', offset)
        self._set_property('length', length)
        self._set_property('count', count)
        self._set_property('values', values)

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        Bit offset in the packet at which the pattern will be applied

        Returns: int
        """
        return self._get_property('offset')

    @offset.setter
    def offset(self, value):
        """offset setter

        Bit offset in the packet at which the pattern will be applied

        value: int
        """
        self._set_property('offset', value)

    @property
    def length(self):
        # type: () -> int
        """length getter

        The number of bits in the packet that the pattern will span

        Returns: int
        """
        return self._get_property('length')

    @length.setter
    def length(self, value):
        """length setter

        The number of bits in the packet that the pattern will span

        value: int
        """
        self._set_property('length', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of values to generate before repeating

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The number of values to generate before repeating

        value: int
        """
        self._set_property('count', value)

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value)


class FlowBitCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, offset=None, length=None, count=None, start=None, step=None):
        super(FlowBitCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('offset', offset)
        self._set_property('length', length)
        self._set_property('count', count)
        self._set_property('start', start)
        self._set_property('step', step)

    @property
    def offset(self):
        # type: () -> int
        """offset getter

        Bit offset in the packet at which the pattern will be applied

        Returns: int
        """
        return self._get_property('offset')

    @offset.setter
    def offset(self, value):
        """offset setter

        Bit offset in the packet at which the pattern will be applied

        value: int
        """
        self._set_property('offset', value)

    @property
    def length(self):
        # type: () -> int
        """length getter

        The number of bits in the packet that the pattern will span

        Returns: int
        """
        return self._get_property('length')

    @length.setter
    def length(self, value):
        """length setter

        The number of bits in the packet that the pattern will span

        value: int
        """
        self._set_property('length', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of values to generate before repeating A value of 0 means the pattern will count continuously

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The number of values to generate before repeating A value of 0 means the pattern will count continuously

        value: int
        """
        self._set_property('count', value)

    @property
    def start(self):
        # type: () -> str
        """start getter

        The starting value of the pattern. If the value is greater than the length it will be truncated.

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        The starting value of the pattern. If the value is greater than the length it will be truncated.

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        The amount the start value will be incremented by If the value is greater than the length it will be truncated.

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        The amount the start value will be incremented by If the value is greater than the length it will be truncated.

        value: str
        """
        self._set_property('step', value)


class FlowBitPatternList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowBitPatternList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowBitPattern, FlowBitCounter, FlowBitList]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowBitPatternList
        return self._iter()

    def __next__(self):
        # type: () -> FlowBitPattern
        return self._next()

    def next(self):
        # type: () -> FlowBitPattern
        return self._next()

    def bitpattern(self):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitPattern class

        Container for a bit pattern
        """
        item = FlowBitPattern()
        self._add(item)
        return self

    def bitlist(self, offset=1, length=1, count=1, values=None):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitList class

        A pattern which is a list of values.
        """
        item = FlowBitPattern()
        item.bitlist
        item.choice = 'bitlist'
        self._add(item)
        return self

    def bitcounter(self, offset=0, length=32, count=1, start=0, step=0):
        # type: () -> FlowBitPatternList
        """Factory method that creates an instance of FlowBitCounter class

        An incrementing pattern
        """
        item = FlowBitPattern()
        item.bitcounter
        item.choice = 'bitcounter'
        self._add(item)
        return self


class FlowEthernet(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'pfc_queue': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowEthernet, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst', FlowPattern)

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src', FlowPattern)

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ether_type', FlowPattern)

    @property
    def pfc_queue(self):
        # type: () -> FlowPattern
        """pfc_queue getter

        A container for packet header field patterns.A container for packet header field patterns.Optional field of 3 bits

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pfc_queue', FlowPattern)


class FlowPattern(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'FlowCounter',
        'decrement': 'FlowCounter',
    }

    VALUE = 'value'
    VALUES = 'values'
    INCREMENT = 'increment'
    DECREMENT = 'decrement'

    def __init__(self, parent=None, choice=None, metric_group=None):
        super(FlowPattern, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('metric_group', metric_group)

    @property
    def increment(self):
        # type: () -> FlowCounter
        """Factory property that returns an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        return self._get_property('increment', FlowCounter(self, 'increment'))

    @property
    def decrement(self):
        # type: () -> FlowCounter
        """Factory property that returns an instance of the FlowCounter class

        A counter pattern that can increment or decrement.
        """
        return self._get_property('decrement', FlowCounter(self, 'decrement'))

    @property
    def choice(self):
        # type: () -> Union[value, values, increment, decrement, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[value, values, increment, decrement, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[value, values, increment, decrement, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def value(self):
        # type: () -> str
        """value getter

        TBD

        Returns: str
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        TBD

        value: str
        """
        self._set_property('value', value, 'value')

    @property
    def values(self):
        # type: () -> list[str]
        """values getter

        TBD

        Returns: list[str]
        """
        return self._get_property('values')

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._set_property('values', value, 'values')

    @property
    def metric_group(self):
        # type: () -> str
        """metric_group getter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        Returns: str
        """
        return self._get_property('metric_group')

    @metric_group.setter
    def metric_group(self, value):
        """metric_group setter

        A unique name is used to indicate to the system that the field may extend the metric row key and create an aggregate metric row for every unique value. To have metric group columns appear in the flow metric rows the flow metric request allows for the metric_group value to be specified as part of the request.

        value: str
        """
        self._set_property('metric_group', value)


class FlowCounter(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, step=None, count=None):
        super(FlowCounter, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('step', step)
        self._set_property('count', count)

    @property
    def start(self):
        # type: () -> str
        """start getter

        The value at which the pattern will start.

        Returns: str
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        The value at which the pattern will start.

        value: str
        """
        self._set_property('start', value)

    @property
    def step(self):
        # type: () -> str
        """step getter

        The value at which the pattern will increment or decrement by.

        Returns: str
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        The value at which the pattern will increment or decrement by.

        value: str
        """
        self._set_property('step', value)

    @property
    def count(self):
        # type: () -> int
        """count getter

        The number of values in the pattern.

        Returns: int
        """
        return self._get_property('count')

    @count.setter
    def count(self, value):
        """count setter

        The number of values in the pattern.

        value: int
        """
        self._set_property('count', value)


class FlowVlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'priority': 'FlowPattern',
        'cfi': 'FlowPattern',
        'id': 'FlowPattern',
        'protocol': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowVlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def priority(self):
        # type: () -> FlowPattern
        """priority getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('priority', FlowPattern)

    @property
    def cfi(self):
        # type: () -> FlowPattern
        """cfi getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('cfi', FlowPattern)

    @property
    def id(self):
        # type: () -> FlowPattern
        """id getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('id', FlowPattern)

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol', FlowPattern)


class FlowVxlan(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'flags': 'FlowPattern',
        'reserved0': 'FlowPattern',
        'vni': 'FlowPattern',
        'reserved1': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowVxlan, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def flags(self):
        # type: () -> FlowPattern
        """flags getter

        A container for packet header field patterns.A container for packet header field patterns.RRRRIRRR Where the I flag MUST be set to 1 for a valid vxlan network id (VNI). The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('flags', FlowPattern)

    @property
    def reserved0(self):
        # type: () -> FlowPattern
        """reserved0 getter

        A container for packet header field patterns.A container for packet header field patterns.Set to 0. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved0', FlowPattern)

    @property
    def vni(self):
        # type: () -> FlowPattern
        """vni getter

        A container for packet header field patterns.A container for packet header field patterns.Vxlan network id. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('vni', FlowPattern)

    @property
    def reserved1(self):
        # type: () -> FlowPattern
        """reserved1 getter

        A container for packet header field patterns.A container for packet header field patterns.Set to 0. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved1', FlowPattern)


class FlowIpv4(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'FlowPattern',
        'header_length': 'FlowPattern',
        'priority': 'FlowIpv4Priority',
        'total_length': 'FlowPattern',
        'identification': 'FlowPattern',
        'reserved': 'FlowPattern',
        'dont_fragment': 'FlowPattern',
        'more_fragments': 'FlowPattern',
        'fragment_offset': 'FlowPattern',
        'time_to_live': 'FlowPattern',
        'protocol': 'FlowPattern',
        'header_checksum': 'FlowPattern',
        'src': 'FlowPattern',
        'dst': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def header_length(self):
        # type: () -> FlowPattern
        """header_length getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('header_length', FlowPattern)

    @property
    def priority(self):
        # type: () -> FlowIpv4Priority
        """priority getter

        A container for ipv4 raw, tos, dscp ip priorities.A container for ipv4 raw, tos, dscp ip priorities.

        Returns: obj(snappi.FlowIpv4Priority)
        """
        return self._get_property('priority', FlowIpv4Priority)

    @property
    def total_length(self):
        # type: () -> FlowPattern
        """total_length getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('total_length', FlowPattern)

    @property
    def identification(self):
        # type: () -> FlowPattern
        """identification getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('identification', FlowPattern)

    @property
    def reserved(self):
        # type: () -> FlowPattern
        """reserved getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved', FlowPattern)

    @property
    def dont_fragment(self):
        # type: () -> FlowPattern
        """dont_fragment getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dont_fragment', FlowPattern)

    @property
    def more_fragments(self):
        # type: () -> FlowPattern
        """more_fragments getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('more_fragments', FlowPattern)

    @property
    def fragment_offset(self):
        # type: () -> FlowPattern
        """fragment_offset getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('fragment_offset', FlowPattern)

    @property
    def time_to_live(self):
        # type: () -> FlowPattern
        """time_to_live getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('time_to_live', FlowPattern)

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol', FlowPattern)

    @property
    def header_checksum(self):
        # type: () -> FlowPattern
        """header_checksum getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('header_checksum', FlowPattern)

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src', FlowPattern)

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst', FlowPattern)


class FlowIpv4Priority(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'raw': 'FlowPattern',
        'tos': 'FlowIpv4Tos',
        'dscp': 'FlowIpv4Dscp',
    }

    PRIORITY_RAW = '0'

    RAW = 'raw'
    TOS = 'tos'
    DSCP = 'dscp'

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Priority, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def raw(self):
        # type: () -> FlowPattern
        """Factory property that returns an instance of the FlowPattern class

        A container for packet header field patterns.
        """
        return self._get_property('raw', FlowPattern(self, 'raw'))

    @property
    def tos(self):
        # type: () -> FlowIpv4Tos
        """Factory property that returns an instance of the FlowIpv4Tos class

        Type of service (TOS) packet field.
        """
        return self._get_property('tos', FlowIpv4Tos(self, 'tos'))

    @property
    def dscp(self):
        # type: () -> FlowIpv4Dscp
        """Factory property that returns an instance of the FlowIpv4Dscp class

        Differentiated services code point (DSCP) packet field.
        """
        return self._get_property('dscp', FlowIpv4Dscp(self, 'dscp'))

    @property
    def choice(self):
        # type: () -> Union[raw, tos, dscp, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[raw, tos, dscp, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[raw, tos, dscp, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowIpv4Tos(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'precedence': 'FlowPattern',
        'delay': 'FlowPattern',
        'throughput': 'FlowPattern',
        'reliability': 'FlowPattern',
        'monetary': 'FlowPattern',
        'unused': 'FlowPattern',
    }

    PRE_ROUTINE = '0'
    PRE_PRIORITY = '1'
    PRE_IMMEDIATE = '2'
    PRE_FLASH = '3'
    PRE_FLASH_OVERRIDE = '4'
    PRE_CRITIC_ECP = '5'
    PRE_INTERNETWORK_CONTROL = '6'
    PRE_NETWORK_CONTROL = '7'
    NORMAL = '0'
    LOW = '1'

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Tos, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def precedence(self):
        # type: () -> FlowPattern
        """precedence getter

        A container for packet header field patterns.A container for packet header field patterns.Precedence value is 3 bits: >=0 precedence <=3

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('precedence', FlowPattern)

    @property
    def delay(self):
        # type: () -> FlowPattern
        """delay getter

        A container for packet header field patterns.A container for packet header field patterns.Delay value is 1 bit: >=0 delay <=1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('delay', FlowPattern)

    @property
    def throughput(self):
        # type: () -> FlowPattern
        """throughput getter

        A container for packet header field patterns.A container for packet header field patterns.Throughput value is 1 bit: >=0 throughput <=3

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('throughput', FlowPattern)

    @property
    def reliability(self):
        # type: () -> FlowPattern
        """reliability getter

        A container for packet header field patterns.A container for packet header field patterns.Reliability value is 1 bit: >=0 reliability <=1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reliability', FlowPattern)

    @property
    def monetary(self):
        # type: () -> FlowPattern
        """monetary getter

        A container for packet header field patterns.A container for packet header field patterns.Monetary value is 1 bit: >=0 monetary <=1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('monetary', FlowPattern)

    @property
    def unused(self):
        # type: () -> FlowPattern
        """unused getter

        A container for packet header field patterns.A container for packet header field patterns.Unused value is 1 bit: >=0 unused <=1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('unused', FlowPattern)


class FlowIpv4Dscp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'phb': 'FlowPattern',
        'ecn': 'FlowPattern',
    }

    PHB_DEFAULT = '0'
    PHB_CS1 = '8'
    PHB_CS2 = '16'
    PHB_CS3 = '24'
    PHB_CS4 = '32'
    PHB_CS5 = '40'
    PHB_CS6 = '48'
    PHB_CS7 = '56'
    PHB_AF11 = '10'
    PHB_AF12 = '12'
    PHB_AF13 = '14'
    PHB_AF21 = '18'
    PHB_AF22 = '20'
    PHB_AF23 = '22'
    PHB_AF31 = '26'
    PHB_AF32 = '28'
    PHB_AF33 = '30'
    PHB_AF41 = '34'
    PHB_AF42 = '36'
    PHB_AF43 = '38'
    PHB_EF46 = '46'
    ECN_NON_CAPABLE = '0'
    ECN_CAPABLE_TRANSPORT_0 = '1'
    ECN_CAPABLE_TRANSPORT_1 = '2'
    ECN_CONGESTION_ENCOUNTERED = '3'

    def __init__(self, parent=None, choice=None):
        super(FlowIpv4Dscp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def phb(self):
        # type: () -> FlowPattern
        """phb getter

        A container for packet header field patterns.A container for packet header field patterns.phb (per-hop-behavior) value is 6 bits: >=0 PHB <=63.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('phb', FlowPattern)

    @property
    def ecn(self):
        # type: () -> FlowPattern
        """ecn getter

        A container for packet header field patterns.A container for packet header field patterns.ecn (explicit-congestion-notification) value is 2 bits: >=0 ecn <=3

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ecn', FlowPattern)


class FlowIpv6(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'FlowPattern',
        'traffic_class': 'FlowPattern',
        'flow_label': 'FlowPattern',
        'payload_length': 'FlowPattern',
        'next_header': 'FlowPattern',
        'hop_limit': 'FlowPattern',
        'src': 'FlowPattern',
        'dst': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIpv6, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.Default version number is 6 (bit sequence 0110) 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def traffic_class(self):
        # type: () -> FlowPattern
        """traffic_class getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('traffic_class', FlowPattern)

    @property
    def flow_label(self):
        # type: () -> FlowPattern
        """flow_label getter

        A container for packet header field patterns.A container for packet header field patterns.20 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('flow_label', FlowPattern)

    @property
    def payload_length(self):
        # type: () -> FlowPattern
        """payload_length getter

        A container for packet header field patterns.A container for packet header field patterns.16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('payload_length', FlowPattern)

    @property
    def next_header(self):
        # type: () -> FlowPattern
        """next_header getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('next_header', FlowPattern)

    @property
    def hop_limit(self):
        # type: () -> FlowPattern
        """hop_limit getter

        A container for packet header field patterns.A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('hop_limit', FlowPattern)

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.128 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src', FlowPattern)

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.128 bits

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst', FlowPattern)


class FlowPfcPause(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'control_op_code': 'FlowPattern',
        'class_enable_vector': 'FlowPattern',
        'pause_class_0': 'FlowPattern',
        'pause_class_1': 'FlowPattern',
        'pause_class_2': 'FlowPattern',
        'pause_class_3': 'FlowPattern',
        'pause_class_4': 'FlowPattern',
        'pause_class_5': 'FlowPattern',
        'pause_class_6': 'FlowPattern',
        'pause_class_7': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowPfcPause, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst', FlowPattern)

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src', FlowPattern)

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ether_type', FlowPattern)

    @property
    def control_op_code(self):
        # type: () -> FlowPattern
        """control_op_code getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('control_op_code', FlowPattern)

    @property
    def class_enable_vector(self):
        # type: () -> FlowPattern
        """class_enable_vector getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('class_enable_vector', FlowPattern)

    @property
    def pause_class_0(self):
        # type: () -> FlowPattern
        """pause_class_0 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_0', FlowPattern)

    @property
    def pause_class_1(self):
        # type: () -> FlowPattern
        """pause_class_1 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_1', FlowPattern)

    @property
    def pause_class_2(self):
        # type: () -> FlowPattern
        """pause_class_2 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_2', FlowPattern)

    @property
    def pause_class_3(self):
        # type: () -> FlowPattern
        """pause_class_3 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_3', FlowPattern)

    @property
    def pause_class_4(self):
        # type: () -> FlowPattern
        """pause_class_4 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_4', FlowPattern)

    @property
    def pause_class_5(self):
        # type: () -> FlowPattern
        """pause_class_5 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_5', FlowPattern)

    @property
    def pause_class_6(self):
        # type: () -> FlowPattern
        """pause_class_6 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_6', FlowPattern)

    @property
    def pause_class_7(self):
        # type: () -> FlowPattern
        """pause_class_7 getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pause_class_7', FlowPattern)


class FlowEthernetPause(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'dst': 'FlowPattern',
        'src': 'FlowPattern',
        'ether_type': 'FlowPattern',
        'control_op_code': 'FlowPattern',
        'time': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowEthernetPause, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def dst(self):
        # type: () -> FlowPattern
        """dst getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst', FlowPattern)

    @property
    def src(self):
        # type: () -> FlowPattern
        """src getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src', FlowPattern)

    @property
    def ether_type(self):
        # type: () -> FlowPattern
        """ether_type getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ether_type', FlowPattern)

    @property
    def control_op_code(self):
        # type: () -> FlowPattern
        """control_op_code getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('control_op_code', FlowPattern)

    @property
    def time(self):
        # type: () -> FlowPattern
        """time getter

        A container for packet header field patterns.A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('time', FlowPattern)


class FlowTcp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src_port': 'FlowPattern',
        'dst_port': 'FlowPattern',
        'seq_num': 'FlowPattern',
        'ack_num': 'FlowPattern',
        'data_offset': 'FlowPattern',
        'ecn_ns': 'FlowPattern',
        'ecn_cwr': 'FlowPattern',
        'ecn_echo': 'FlowPattern',
        'ctl_urg': 'FlowPattern',
        'ctl_ack': 'FlowPattern',
        'ctl_psh': 'FlowPattern',
        'ctl_rst': 'FlowPattern',
        'ctl_syn': 'FlowPattern',
        'ctl_fin': 'FlowPattern',
        'window': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowTcp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src_port(self):
        # type: () -> FlowPattern
        """src_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp source port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src_port', FlowPattern)

    @property
    def dst_port(self):
        # type: () -> FlowPattern
        """dst_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp destination port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst_port', FlowPattern)

    @property
    def seq_num(self):
        # type: () -> FlowPattern
        """seq_num getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp Sequence Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('seq_num', FlowPattern)

    @property
    def ack_num(self):
        # type: () -> FlowPattern
        """ack_num getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp Acknowledgement Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ack_num', FlowPattern)

    @property
    def data_offset(self):
        # type: () -> FlowPattern
        """data_offset getter

        A container for packet header field patterns.A container for packet header field patterns.The number of 32 bit words in the TCP header. This indicates where the data begins. Max length is 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('data_offset', FlowPattern)

    @property
    def ecn_ns(self):
        # type: () -> FlowPattern
        """ecn_ns getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, concealment protection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ecn_ns', FlowPattern)

    @property
    def ecn_cwr(self):
        # type: () -> FlowPattern
        """ecn_cwr getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, congestion window reduced. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ecn_cwr', FlowPattern)

    @property
    def ecn_echo(self):
        # type: () -> FlowPattern
        """ecn_echo getter

        A container for packet header field patterns.A container for packet header field patterns.Explicit congestion notification, echo. 1 indicates the peer is ecn capable. 0 indicates that a packet with ipv4.ecn = 11 in the ip header was received during normal transmission. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ecn_echo', FlowPattern)

    @property
    def ctl_urg(self):
        # type: () -> FlowPattern
        """ctl_urg getter

        A container for packet header field patterns.A container for packet header field patterns.A value of 1 indicates that the urgent pointer field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_urg', FlowPattern)

    @property
    def ctl_ack(self):
        # type: () -> FlowPattern
        """ctl_ack getter

        A container for packet header field patterns.A container for packet header field patterns.A value of 1 indicates that the ackknowledgment field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_ack', FlowPattern)

    @property
    def ctl_psh(self):
        # type: () -> FlowPattern
        """ctl_psh getter

        A container for packet header field patterns.A container for packet header field patterns.Asks to push the buffered data to the receiving application. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_psh', FlowPattern)

    @property
    def ctl_rst(self):
        # type: () -> FlowPattern
        """ctl_rst getter

        A container for packet header field patterns.A container for packet header field patterns.Reset the connection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_rst', FlowPattern)

    @property
    def ctl_syn(self):
        # type: () -> FlowPattern
        """ctl_syn getter

        A container for packet header field patterns.A container for packet header field patterns.Synchronize sequenece numbers. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_syn', FlowPattern)

    @property
    def ctl_fin(self):
        # type: () -> FlowPattern
        """ctl_fin getter

        A container for packet header field patterns.A container for packet header field patterns.Last packet from the sender. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('ctl_fin', FlowPattern)

    @property
    def window(self):
        # type: () -> FlowPattern
        """window getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp connection window. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('window', FlowPattern)


class FlowUdp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'src_port': 'FlowPattern',
        'dst_port': 'FlowPattern',
        'length': 'FlowPattern',
        'checksum': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowUdp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def src_port(self):
        # type: () -> FlowPattern
        """src_port getter

        A container for packet header field patterns.A container for packet header field patterns.Udp source port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('src_port', FlowPattern)

    @property
    def dst_port(self):
        # type: () -> FlowPattern
        """dst_port getter

        A container for packet header field patterns.A container for packet header field patterns.Tcp destination port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('dst_port', FlowPattern)

    @property
    def length(self):
        # type: () -> FlowPattern
        """length getter

        A container for packet header field patterns.A container for packet header field patterns.Length in bytes of the udp header and yudp data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('length', FlowPattern)

    @property
    def checksum(self):
        # type: () -> FlowPattern
        """checksum getter

        A container for packet header field patterns.A container for packet header field patterns.Checksum field used for error checking of header and data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('checksum', FlowPattern)


class FlowGre(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'checksum_present': 'FlowPattern',
        'key_present': 'FlowPattern',
        'seq_number_present': 'FlowPattern',
        'reserved0': 'FlowPattern',
        'version': 'FlowPattern',
        'protocol': 'FlowPattern',
        'checksum': 'FlowPattern',
        'reserved1': 'FlowPattern',
        'key': 'FlowPattern',
        'sequence_number': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGre, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def checksum_present(self):
        # type: () -> FlowPattern
        """checksum_present getter

        A container for packet header field patterns.A container for packet header field patterns.Checksum bit. Set to 1 if a checksum is present.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('checksum_present', FlowPattern)

    @property
    def key_present(self):
        # type: () -> FlowPattern
        """key_present getter

        A container for packet header field patterns.A container for packet header field patterns.Key bit. Set to 1 if a key is present.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('key_present', FlowPattern)

    @property
    def seq_number_present(self):
        # type: () -> FlowPattern
        """seq_number_present getter

        A container for packet header field patterns.A container for packet header field patterns.Sequence number bit. Set to 1 if a sequence number is present.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('seq_number_present', FlowPattern)

    @property
    def reserved0(self):
        # type: () -> FlowPattern
        """reserved0 getter

        A container for packet header field patterns.A container for packet header field patterns.Reserved bits. Set to 0. 9 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved0', FlowPattern)

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.Gre version number. Set to 0. 3 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def protocol(self):
        # type: () -> FlowPattern
        """protocol getter

        A container for packet header field patterns.A container for packet header field patterns.Indicates the ether protocol type of the encapsulated payload. - 0x0800 ipv4 - 0x86DD ipv6

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol', FlowPattern)

    @property
    def checksum(self):
        # type: () -> FlowPattern
        """checksum getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the checksum_present bit is set. Contains the checksum for the gre header and payload. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('checksum', FlowPattern)

    @property
    def reserved1(self):
        # type: () -> FlowPattern
        """reserved1 getter

        A container for packet header field patterns.A container for packet header field patterns.Reserved bits. Set to 0. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved1', FlowPattern)

    @property
    def key(self):
        # type: () -> FlowPattern
        """key getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the key_present bit is set. Contains an application specific key value. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('key', FlowPattern)

    @property
    def sequence_number(self):
        # type: () -> FlowPattern
        """sequence_number getter

        A container for packet header field patterns.A container for packet header field patterns.Present if the seq_number_present bit is set. Contains a sequence number for the gre packet. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('sequence_number', FlowPattern)


class FlowGtpv1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'FlowPattern',
        'protocol_type': 'FlowPattern',
        'reserved': 'FlowPattern',
        'e_flag': 'FlowPattern',
        's_flag': 'FlowPattern',
        'pn_flag': 'FlowPattern',
        'message_type': 'FlowPattern',
        'message_length': 'FlowPattern',
        'teid': 'FlowPattern',
        'squence_number': 'FlowPattern',
        'n_pdu_number': 'FlowPattern',
        'next_extension_header_type': 'FlowPattern',
        'extension_headers': 'FlowGtpExtensionList',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpv1, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.It is a 3-bit field. For GTPv1, this has a value of 1.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def protocol_type(self):
        # type: () -> FlowPattern
        """protocol_type getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that differentiates GTP (value 1) from GTP' (value 0).

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol_type', FlowPattern)

    @property
    def reserved(self):
        # type: () -> FlowPattern
        """reserved getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('reserved', FlowPattern)

    @property
    def e_flag(self):
        # type: () -> FlowPattern
        """e_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is an extension header optional field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('e_flag', FlowPattern)

    @property
    def s_flag(self):
        # type: () -> FlowPattern
        """s_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is a Sequence Number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('s_flag', FlowPattern)

    @property
    def pn_flag(self):
        # type: () -> FlowPattern
        """pn_flag getter

        A container for packet header field patterns.A container for packet header field patterns.A 1-bit value that states whether there is a N-PDU number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('pn_flag', FlowPattern)

    @property
    def message_type(self):
        # type: () -> FlowPattern
        """message_type getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('message_type', FlowPattern)

    @property
    def message_length(self):
        # type: () -> FlowPattern
        """message_length getter

        A container for packet header field patterns.A container for packet header field patterns.A 16-bit field that indicates the length of the payload in bytes (rest of the packet following the mandatory 8-byte GTP header). Includes the optional fields.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('message_length', FlowPattern)

    @property
    def teid(self):
        # type: () -> FlowPattern
        """teid getter

        A container for packet header field patterns.A container for packet header field patterns.Tunnel endpoint identifier. A 32-bit(4-octet) field used to multiplex different connections in the same GTP tunnel.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('teid', FlowPattern)

    @property
    def squence_number(self):
        # type: () -> FlowPattern
        """squence_number getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 16-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the s_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('squence_number', FlowPattern)

    @property
    def n_pdu_number(self):
        # type: () -> FlowPattern
        """n_pdu_number getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the pn_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('n_pdu_number', FlowPattern)

    @property
    def next_extension_header_type(self):
        # type: () -> FlowPattern
        """next_extension_header_type getter

        A container for packet header field patterns.A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the e_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('next_extension_header_type', FlowPattern)

    @property
    def extension_headers(self):
        # type: () -> FlowGtpExtensionList
        """extension_headers getter

        A list of optional extension headers.

        Returns: list[obj(snappi.FlowGtpExtension)]
        """
        return self._get_property('extension_headers', FlowGtpExtensionList)


class FlowGtpExtension(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'extension_length': 'FlowPattern',
        'contents': 'FlowPattern',
        'next_extension_header': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpExtension, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def extension_length(self):
        # type: () -> FlowPattern
        """extension_length getter

        A container for packet header field patterns.An 8-bit field. This field states the length of this extension header, including the length, the contents, and the next extension header field, in 4-octet units, so the length of the extension must always be a multiple of 4.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('extension_length', FlowPattern)

    @property
    def contents(self):
        # type: () -> FlowPattern
        """contents getter

        A container for packet header field patterns.The extension header contents.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('contents', FlowPattern)

    @property
    def next_extension_header(self):
        # type: () -> FlowPattern
        """next_extension_header getter

        A container for packet header field patterns.An 8-bit field. It states the type of the next extension, or 0 if no next extension exists. This permits chaining several next extension headers.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('next_extension_header', FlowPattern)


class FlowGtpExtensionList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowGtpExtensionList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowGtpExtension]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowGtpExtensionList
        return self._iter()

    def __next__(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def next(self):
        # type: () -> FlowGtpExtension
        return self._next()

    def gtpextension(self):
        # type: () -> FlowGtpExtensionList
        """Factory method that creates an instance of FlowGtpExtension class

        TBD
        """
        item = FlowGtpExtension()
        self._add(item)
        return self


class FlowGtpv2(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'FlowPattern',
        'piggybacking_flag': 'FlowPattern',
        'teid_flag': 'FlowPattern',
        'spare1': 'FlowPattern',
        'message_type': 'FlowPattern',
        'message_length': 'FlowPattern',
        'teid': 'FlowPattern',
        'sequence_number': 'FlowPattern',
        'spare2': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowGtpv2, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.It is a 3-bit field. For GTPv2, this has a value of 2.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def piggybacking_flag(self):
        # type: () -> FlowPattern
        """piggybacking_flag getter

        A container for packet header field patterns.A container for packet header field patterns.If this bit is set to 1 then another GTP-C message with its own header shall be present at the end of the current message.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('piggybacking_flag', FlowPattern)

    @property
    def teid_flag(self):
        # type: () -> FlowPattern
        """teid_flag getter

        A container for packet header field patterns.A container for packet header field patterns.If this bit is set to 1 then the TEID field will be present between the message length and the sequence number. All messages except Echo and Echo reply require TEID to be present.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('teid_flag', FlowPattern)

    @property
    def spare1(self):
        # type: () -> FlowPattern
        """spare1 getter

        A container for packet header field patterns.A container for packet header field patterns.A 3-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('spare1', FlowPattern)

    @property
    def message_type(self):
        # type: () -> FlowPattern
        """message_type getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('message_type', FlowPattern)

    @property
    def message_length(self):
        # type: () -> FlowPattern
        """message_length getter

        A container for packet header field patterns.A container for packet header field patterns.A 16-bit field that indicates the length of the payload in bytes (excluding the mandatory GTP-c header (first 4 bytes). Includes the TEID and sequence_number if they are present.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('message_length', FlowPattern)

    @property
    def teid(self):
        # type: () -> FlowPattern
        """teid getter

        A container for packet header field patterns.A container for packet header field patterns.Tunnel endpoint identifier. A 32-bit (4-octet) field used to multiplex different connections in the same GTP tunnel. Is present only if the teid_flag is set.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('teid', FlowPattern)

    @property
    def sequence_number(self):
        # type: () -> FlowPattern
        """sequence_number getter

        A container for packet header field patterns.A container for packet header field patterns.A 24-bit field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('sequence_number', FlowPattern)

    @property
    def spare2(self):
        # type: () -> FlowPattern
        """spare2 getter

        A container for packet header field patterns.A container for packet header field patterns.An 8-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('spare2', FlowPattern)


class FlowArp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'hardware_type': 'FlowPattern',
        'protocol_type': 'FlowPattern',
        'hardware_length': 'FlowPattern',
        'protocol_length': 'FlowPattern',
        'operation': 'FlowPattern',
        'sender_hardware_addr': 'FlowPattern',
        'sender_protocol_addr': 'FlowPattern',
        'target_hardware_addr': 'FlowPattern',
        'target_protocol_addr': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowArp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def hardware_type(self):
        # type: () -> FlowPattern
        """hardware_type getter

        A container for packet header field patterns.A container for packet header field patterns.Network link protocol type. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('hardware_type', FlowPattern)

    @property
    def protocol_type(self):
        # type: () -> FlowPattern
        """protocol_type getter

        A container for packet header field patterns.A container for packet header field patterns.The internetwork protocol for which the ARP request is intended. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol_type', FlowPattern)

    @property
    def hardware_length(self):
        # type: () -> FlowPattern
        """hardware_length getter

        A container for packet header field patterns.A container for packet header field patterns.Length (in octets) of a hardware address. Max length is 1 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('hardware_length', FlowPattern)

    @property
    def protocol_length(self):
        # type: () -> FlowPattern
        """protocol_length getter

        A container for packet header field patterns.A container for packet header field patterns.Length (in octets) of internetwork addresses. Max length is 1 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol_length', FlowPattern)

    @property
    def operation(self):
        # type: () -> FlowPattern
        """operation getter

        A container for packet header field patterns.A container for packet header field patterns.The operation that the sender is performing: 1 for request, 2 for reply. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('operation', FlowPattern)

    @property
    def sender_hardware_addr(self):
        # type: () -> FlowPattern
        """sender_hardware_addr getter

        A container for packet header field patterns.A container for packet header field patterns.Media address of the sender. Max length is 6 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('sender_hardware_addr', FlowPattern)

    @property
    def sender_protocol_addr(self):
        # type: () -> FlowPattern
        """sender_protocol_addr getter

        A container for packet header field patterns.A container for packet header field patterns.Internetwork address of the sender. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('sender_protocol_addr', FlowPattern)

    @property
    def target_hardware_addr(self):
        # type: () -> FlowPattern
        """target_hardware_addr getter

        A container for packet header field patterns.A container for packet header field patterns.Media address of the target. Max length is 6 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('target_hardware_addr', FlowPattern)

    @property
    def target_protocol_addr(self):
        # type: () -> FlowPattern
        """target_protocol_addr getter

        A container for packet header field patterns.A container for packet header field patterns.Internetwork address of the target. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('target_protocol_addr', FlowPattern)


class FlowPpp(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'address': 'FlowPattern',
        'control': 'FlowPattern',
        'protocol_type': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowPpp, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def address(self):
        # type: () -> FlowPattern
        """address getter

        A container for packet header field patterns.A container for packet header field patterns.PPP address field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('address', FlowPattern)

    @property
    def control(self):
        # type: () -> FlowPattern
        """control getter

        A container for packet header field patterns.A container for packet header field patterns.PPP control field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('control', FlowPattern)

    @property
    def protocol_type(self):
        # type: () -> FlowPattern
        """protocol_type getter

        A container for packet header field patterns.A container for packet header field patterns.PPP protocol field. Indicates the protocol type of the encapsulated payload.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('protocol_type', FlowPattern)


class FlowIgmpv1(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'version': 'FlowPattern',
        'type': 'FlowPattern',
        'unused': 'FlowPattern',
        'checksum': 'FlowPattern',
        'group_address': 'FlowPattern',
    }

    def __init__(self, parent=None, choice=None):
        super(FlowIgmpv1, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def version(self):
        # type: () -> FlowPattern
        """version getter

        A container for packet header field patterns.A container for packet header field patterns.IGMP version field.

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('version', FlowPattern)

    @property
    def type(self):
        # type: () -> FlowPattern
        """type getter

        A container for packet header field patterns.A container for packet header field patterns.Type of IGMP message, either a Host Membership Query or a Host Membership Report

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('type', FlowPattern)

    @property
    def unused(self):
        # type: () -> FlowPattern
        """unused getter

        A container for packet header field patterns.A container for packet header field patterns.Unused field in IGMPv1

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('unused', FlowPattern)

    @property
    def checksum(self):
        # type: () -> FlowPattern
        """checksum getter

        A container for packet header field patterns.A container for packet header field patterns.Checksum of the IGMP message

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('checksum', FlowPattern)

    @property
    def group_address(self):
        # type: () -> FlowPattern
        """group_address getter

        A container for packet header field patterns.A container for packet header field patterns.Group Address field

        Returns: obj(snappi.FlowPattern)
        """
        return self._get_property('group_address', FlowPattern)


class FlowHeaderList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowHeaderList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowTcp, FlowGtpv2, FlowIgmpv1, FlowPpp, FlowGre, FlowUdp, FlowPfcPause, FlowCustom, FlowEthernetPause, FlowVlan, FlowHeader, FlowVxlan, FlowIpv6, FlowArp, FlowEthernet, FlowGtpv1, FlowIpv4]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowHeaderList
        return self._iter()

    def __next__(self):
        # type: () -> FlowHeader
        return self._next()

    def next(self):
        # type: () -> FlowHeader
        return self._next()

    def header(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowHeader class

        Container for all traffic packet headers
        """
        item = FlowHeader()
        self._add(item)
        return self

    def custom(self, bytes=None):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowCustom class

        Custom packet header
        """
        item = FlowHeader()
        item.custom
        item.choice = 'custom'
        self._add(item)
        return self

    def ethernet(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowEthernet class

        Ethernet packet header
        """
        item = FlowHeader()
        item.ethernet
        item.choice = 'ethernet'
        self._add(item)
        return self

    def vlan(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowVlan class

        VLAN packet header
        """
        item = FlowHeader()
        item.vlan
        item.choice = 'vlan'
        self._add(item)
        return self

    def vxlan(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowVxlan class

        Vxlan packet header
        """
        item = FlowHeader()
        item.vxlan
        item.choice = 'vxlan'
        self._add(item)
        return self

    def ipv4(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowIpv4 class

        IPv4 packet header
        """
        item = FlowHeader()
        item.ipv4
        item.choice = 'ipv4'
        self._add(item)
        return self

    def ipv6(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowIpv6 class

        IPv6 packet header
        """
        item = FlowHeader()
        item.ipv6
        item.choice = 'ipv6'
        self._add(item)
        return self

    def pfcpause(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowPfcPause class

        IEEE 802.1Qbb PFC Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0101 16bits - class_enable_vector: 16bits - pause_class_0: 0x0000 16bits - pause_class_1: 0x0000 16bits - pause_class_2: 0x0000 16bits - pause_class_3: 0x0000 16bits - pause_class_4: 0x0000 16bits - pause_class_5: 0x0000 16bits - pause_class_6: 0x0000 16bits - pause_class_7: 0x0000 16bits
        """
        item = FlowHeader()
        item.pfcpause
        item.choice = 'pfcpause'
        self._add(item)
        return self

    def ethernetpause(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowEthernetPause class

        IEEE 802.3x Ethernet Pause packet header. - dst: 01:80:C2:00:00:01 48bits - src: 48bits - ether_type: 0x8808 16bits - control_op_code: 0x0001 16bits - time: 0x0000 16bits
        """
        item = FlowHeader()
        item.ethernetpause
        item.choice = 'ethernetpause'
        self._add(item)
        return self

    def tcp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowTcp class

        TCP packet header
        """
        item = FlowHeader()
        item.tcp
        item.choice = 'tcp'
        self._add(item)
        return self

    def udp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowUdp class

        UDP packet header
        """
        item = FlowHeader()
        item.udp
        item.choice = 'udp'
        self._add(item)
        return self

    def gre(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGre class

        GRE packet header
        """
        item = FlowHeader()
        item.gre
        item.choice = 'gre'
        self._add(item)
        return self

    def gtpv1(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGtpv1 class

        GTPv1 packet header
        """
        item = FlowHeader()
        item.gtpv1
        item.choice = 'gtpv1'
        self._add(item)
        return self

    def gtpv2(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowGtpv2 class

        GTPv2 packet header
        """
        item = FlowHeader()
        item.gtpv2
        item.choice = 'gtpv2'
        self._add(item)
        return self

    def arp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowArp class

        ARP packet header
        """
        item = FlowHeader()
        item.arp
        item.choice = 'arp'
        self._add(item)
        return self

    def ppp(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowPpp class

        PPP packet header
        """
        item = FlowHeader()
        item.ppp
        item.choice = 'ppp'
        self._add(item)
        return self

    def igmpv1(self):
        # type: () -> FlowHeaderList
        """Factory method that creates an instance of FlowIgmpv1 class

        IGMPv1 packet header
        """
        item = FlowHeader()
        item.igmpv1
        item.choice = 'igmpv1'
        self._add(item)
        return self


class FlowSize(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'increment': 'FlowSizeIncrement',
        'random': 'FlowSizeRandom',
    }

    FIXED = 'fixed'
    INCREMENT = 'increment'
    RANDOM = 'random'

    def __init__(self, parent=None, choice=None):
        super(FlowSize, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def increment(self):
        # type: () -> FlowSizeIncrement
        """Factory property that returns an instance of the FlowSizeIncrement class

        Frame size that increments from a starting size to an ending size incrementing by a step size.
        """
        return self._get_property('increment', FlowSizeIncrement(self, 'increment'))

    @property
    def random(self):
        # type: () -> FlowSizeRandom
        """Factory property that returns an instance of the FlowSizeRandom class

        Random frame size from a min value to a max value.
        """
        return self._get_property('random', FlowSizeRandom(self, 'random'))

    @property
    def choice(self):
        # type: () -> Union[fixed, increment, random, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed, increment, random, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed, increment, random, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def fixed(self):
        # type: () -> int
        """fixed getter

        TBD

        Returns: int
        """
        return self._get_property('fixed')

    @fixed.setter
    def fixed(self, value):
        """fixed setter

        TBD

        value: int
        """
        self._set_property('fixed', value, 'fixed')


class FlowSizeIncrement(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, start=None, end=None, step=None):
        super(FlowSizeIncrement, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('start', start)
        self._set_property('end', end)
        self._set_property('step', step)

    @property
    def start(self):
        # type: () -> int
        """start getter

        Starting frame size in bytes

        Returns: int
        """
        return self._get_property('start')

    @start.setter
    def start(self, value):
        """start setter

        Starting frame size in bytes

        value: int
        """
        self._set_property('start', value)

    @property
    def end(self):
        # type: () -> int
        """end getter

        Ending frame size in bytes

        Returns: int
        """
        return self._get_property('end')

    @end.setter
    def end(self, value):
        """end setter

        Ending frame size in bytes

        value: int
        """
        self._set_property('end', value)

    @property
    def step(self):
        # type: () -> int
        """step getter

        Step frame size in bytes

        Returns: int
        """
        return self._get_property('step')

    @step.setter
    def step(self, value):
        """step setter

        Step frame size in bytes

        value: int
        """
        self._set_property('step', value)


class FlowSizeRandom(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, min=None, max=None):
        super(FlowSizeRandom, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('min', min)
        self._set_property('max', max)

    @property
    def min(self):
        # type: () -> int
        """min getter

        TBD

        Returns: int
        """
        return self._get_property('min')

    @min.setter
    def min(self, value):
        """min setter

        TBD

        value: int
        """
        self._set_property('min', value)

    @property
    def max(self):
        # type: () -> int
        """max getter

        TBD

        Returns: int
        """
        return self._get_property('max')

    @max.setter
    def max(self, value):
        """max setter

        TBD

        value: int
        """
        self._set_property('max', value)


class FlowRate(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    PPS = 'pps'
    BPS = 'bps'
    KBPS = 'kbps'
    MBPS = 'mbps'
    GBPS = 'gbps'
    PERCENTAGE = 'percentage'

    def __init__(self, parent=None, choice=None):
        super(FlowRate, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def pps(self):
        # type: () -> int
        """pps getter

        Packets per second.

        Returns: int
        """
        return self._get_property('pps')

    @pps.setter
    def pps(self, value):
        """pps setter

        Packets per second.

        value: int
        """
        self._set_property('pps', value, 'pps')

    @property
    def bps(self):
        # type: () -> int
        """bps getter

        Bits per second.

        Returns: int
        """
        return self._get_property('bps')

    @bps.setter
    def bps(self, value):
        """bps setter

        Bits per second.

        value: int
        """
        self._set_property('bps', value, 'bps')

    @property
    def kbps(self):
        # type: () -> int
        """kbps getter

        Kilobits per second.

        Returns: int
        """
        return self._get_property('kbps')

    @kbps.setter
    def kbps(self, value):
        """kbps setter

        Kilobits per second.

        value: int
        """
        self._set_property('kbps', value, 'kbps')

    @property
    def mbps(self):
        # type: () -> int
        """mbps getter

        Megabits per second.

        Returns: int
        """
        return self._get_property('mbps')

    @mbps.setter
    def mbps(self, value):
        """mbps setter

        Megabits per second.

        value: int
        """
        self._set_property('mbps', value, 'mbps')

    @property
    def gbps(self):
        # type: () -> int
        """gbps getter

        Gigabits per second.

        Returns: int
        """
        return self._get_property('gbps')

    @gbps.setter
    def gbps(self, value):
        """gbps setter

        Gigabits per second.

        value: int
        """
        self._set_property('gbps', value, 'gbps')

    @property
    def percentage(self):
        # type: () -> float
        """percentage getter

        The percentage of a port location's available bandwidth.

        Returns: float
        """
        return self._get_property('percentage')

    @percentage.setter
    def percentage(self, value):
        """percentage setter

        The percentage of a port location's available bandwidth.

        value: float
        """
        self._set_property('percentage', value, 'percentage')


class FlowDuration(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'fixed_packets': 'FlowFixedPackets',
        'fixed_seconds': 'FlowFixedSeconds',
        'burst': 'FlowBurst',
        'continuous': 'FlowContinuous',
    }

    FIXED_PACKETS = 'fixed_packets'
    FIXED_SECONDS = 'fixed_seconds'
    BURST = 'burst'
    CONTINUOUS = 'continuous'

    def __init__(self, parent=None, choice=None):
        super(FlowDuration, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def fixed_packets(self):
        # type: () -> FlowFixedPackets
        """Factory property that returns an instance of the FlowFixedPackets class

        Transmit a fixed number of packets after which the flow will stop.
        """
        return self._get_property('fixed_packets', FlowFixedPackets(self, 'fixed_packets'))

    @property
    def fixed_seconds(self):
        # type: () -> FlowFixedSeconds
        """Factory property that returns an instance of the FlowFixedSeconds class

        Transmit for a fixed number of seconds after which the flow will stop.
        """
        return self._get_property('fixed_seconds', FlowFixedSeconds(self, 'fixed_seconds'))

    @property
    def burst(self):
        # type: () -> FlowBurst
        """Factory property that returns an instance of the FlowBurst class

        Transmits continuous or fixed burst of packets. For continuous burst of packets, it will not automatically stop. For fixed burst of packets, it will stop after transmitting fixed number of bursts. 
        """
        return self._get_property('burst', FlowBurst(self, 'burst'))

    @property
    def continuous(self):
        # type: () -> FlowContinuous
        """Factory property that returns an instance of the FlowContinuous class

        Transmit will be continuous and will not stop automatically. 
        """
        return self._get_property('continuous', FlowContinuous(self, 'continuous'))

    @property
    def choice(self):
        # type: () -> Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        self._set_property('choice', value)


class FlowFixedPackets(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, packets=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedPackets, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('packets', packets)
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        Stop transmit of the flow after this number of packets.

        Returns: int
        """
        return self._get_property('packets')

    @packets.setter
    def packets(self, value):
        """packets setter

        Stop transmit of the flow after this number of packets.

        value: int
        """
        self._set_property('packets', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowFixedSeconds(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, seconds=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedSeconds, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('seconds', seconds)
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def seconds(self):
        # type: () -> float
        """seconds getter

        Stop transmit of the flow after this number of seconds.

        Returns: float
        """
        return self._get_property('seconds')

    @seconds.setter
    def seconds(self, value):
        """seconds setter

        Stop transmit of the flow after this number of seconds.

        value: float
        """
        self._set_property('seconds', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowBurst(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, bursts=None, packets=None, gap=None, inter_burst_gap=None, inter_burst_gap_unit=None):
        super(FlowBurst, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('bursts', bursts)
        self._set_property('packets', packets)
        self._set_property('gap', gap)
        self._set_property('inter_burst_gap', inter_burst_gap)
        self._set_property('inter_burst_gap_unit', inter_burst_gap_unit)

    @property
    def bursts(self):
        # type: () -> int
        """bursts getter

        The number of packet bursts transmitted per flow. A value of 0 implies continuous burst of packets.

        Returns: int
        """
        return self._get_property('bursts')

    @bursts.setter
    def bursts(self, value):
        """bursts setter

        The number of packet bursts transmitted per flow. A value of 0 implies continuous burst of packets.

        value: int
        """
        self._set_property('bursts', value)

    @property
    def packets(self):
        # type: () -> int
        """packets getter

        The number of packets transmitted per burst.

        Returns: int
        """
        return self._get_property('packets')

    @packets.setter
    def packets(self, value):
        """packets setter

        The number of packets transmitted per burst.

        value: int
        """
        self._set_property('packets', value)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def inter_burst_gap(self):
        # type: () -> int
        """inter_burst_gap getter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        Returns: int
        """
        return self._get_property('inter_burst_gap')

    @inter_burst_gap.setter
    def inter_burst_gap(self, value):
        """inter_burst_gap setter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        value: int
        """
        self._set_property('inter_burst_gap', value)

    @property
    def inter_burst_gap_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """inter_burst_gap_unit getter

        The inter burst gap expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('inter_burst_gap_unit')

    @inter_burst_gap_unit.setter
    def inter_burst_gap_unit(self, value):
        """inter_burst_gap_unit setter

        The inter burst gap expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('inter_burst_gap_unit', value)


class FlowContinuous(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    BYTES = 'bytes'
    NANOSECONDS = 'nanoseconds'

    def __init__(self, parent=None, choice=None, gap=None, delay=None, delay_unit=None):
        super(FlowContinuous, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('gap', gap)
        self._set_property('delay', delay)
        self._set_property('delay_unit', delay_unit)

    @property
    def gap(self):
        # type: () -> int
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._get_property('gap')

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._set_property('gap', value)

    @property
    def delay(self):
        # type: () -> int
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._get_property('delay')

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._set_property('delay', value)

    @property
    def delay_unit(self):
        # type: () -> Union[bytes, nanoseconds]
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._get_property('delay_unit')

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._set_property('delay_unit', value)


class FlowList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Flow]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowList
        return self._iter()

    def __next__(self):
        # type: () -> Flow
        return self._next()

    def next(self):
        # type: () -> Flow
        return self._next()

    def flow(self, name=None):
        # type: () -> FlowList
        """Factory method that creates an instance of Flow class

        A high level data plane traffic flow. Acts as a container for endpoints, packet headers, packet size, transmit rate and transmit duration.
        """
        item = Flow(name=name)
        self._add(item)
        return self


class ConfigOptions(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_options': 'PortOptions',
    }

    def __init__(self, parent=None, choice=None):
        super(ConfigOptions, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port_options(self):
        # type: () -> PortOptions
        """port_options getter

        Common port options that apply to all configured Port objects. 

        Returns: obj(snappi.PortOptions)
        """
        return self._get_property('port_options', PortOptions)


class PortOptions(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, location_preemption=None):
        super(PortOptions, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('location_preemption', location_preemption)

    @property
    def location_preemption(self):
        # type: () -> boolean
        """location_preemption getter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        Returns: boolean
        """
        return self._get_property('location_preemption')

    @location_preemption.setter
    def location_preemption(self, value):
        """location_preemption setter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        value: boolean
        """
        self._set_property('location_preemption', value)


class Details(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, errors=None, warnings=None):
        super(Details, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('errors', errors)
        self._set_property('warnings', warnings)

    @property
    def errors(self):
        # type: () -> list[str]
        """errors getter

        A list of any errors that may have occurred while executing the request.

        Returns: list[str]
        """
        return self._get_property('errors')

    @errors.setter
    def errors(self, value):
        """errors setter

        A list of any errors that may have occurred while executing the request.

        value: list[str]
        """
        self._set_property('errors', value)

    @property
    def warnings(self):
        # type: () -> list[str]
        """warnings getter

        A list of any warnings generated while executing the request.

        Returns: list[str]
        """
        return self._get_property('warnings')

    @warnings.setter
    def warnings(self, value):
        """warnings setter

        A list of any warnings generated while executing the request.

        value: list[str]
        """
        self._set_property('warnings', value)


class TransmitState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    START = 'start'
    STOP = 'stop'
    PAUSE = 'pause'

    def __init__(self, parent=None, choice=None, flow_names=None, state=None):
        super(TransmitState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('flow_names', flow_names)
        self._set_property('state', state)

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flows to which the transmit state will be applied to. If the list of flow_names is empty or null the state will be applied to all configured flows.

        Returns: list[str]
        """
        return self._get_property('flow_names')

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flows to which the transmit state will be applied to. If the list of flow_names is empty or null the state will be applied to all configured flows.

        value: list[str]
        """
        self._set_property('flow_names', value)

    @property
    def state(self):
        # type: () -> Union[start, stop, pause]
        """state getter

        The transmit state.

        Returns: Union[start, stop, pause]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The transmit state.

        value: Union[start, stop, pause]
        """
        self._set_property('state', value)


class LinkState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    def __init__(self, parent=None, choice=None, port_names=None, state=None):
        super(LinkState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('state', state)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of port objects to. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of port objects to. An empty or null list will control all port objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def state(self):
        # type: () -> Union[up, down]
        """state getter

        The link state.

        Returns: Union[up, down]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The link state.

        value: Union[up, down]
        """
        self._set_property('state', value)


class CaptureState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    START = 'start'
    STOP = 'stop'

    def __init__(self, parent=None, choice=None, port_names=None, state=None):
        super(CaptureState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('state', state)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def state(self):
        # type: () -> Union[start, stop]
        """state getter

        The capture state.

        Returns: Union[start, stop]
        """
        return self._get_property('state')

    @state.setter
    def state(self, value):
        """state setter

        The capture state.

        value: Union[start, stop]
        """
        self._set_property('state', value)


class MetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port': 'PortMetricsRequest',
        'flow': 'FlowMetricsRequest',
        'bgpv4': 'Bgpv4MetricsRequest',
    }

    PORT = 'port'
    FLOW = 'flow'
    BGPV4 = 'bgpv4'

    def __init__(self, parent=None, choice=None):
        super(MetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port(self):
        # type: () -> PortMetricsRequest
        """Factory property that returns an instance of the PortMetricsRequest class

        The port result request to the traffic generator
        """
        return self._get_property('port', PortMetricsRequest(self, 'port'))

    @property
    def flow(self):
        # type: () -> FlowMetricsRequest
        """Factory property that returns an instance of the FlowMetricsRequest class

        The request to the traffic generator for flow results.
        """
        return self._get_property('flow', FlowMetricsRequest(self, 'flow'))

    @property
    def bgpv4(self):
        # type: () -> Bgpv4MetricsRequest
        """Factory property that returns an instance of the Bgpv4MetricsRequest class

        The request to retrieve BGPv4 Router statistics and learned routing information
        """
        return self._get_property('bgpv4', Bgpv4MetricsRequest(self, 'bgpv4'))

    @property
    def choice(self):
        # type: () -> Union[port, flow, bgpv4, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[port, flow, bgpv4, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[port, flow, bgpv4, choice, choice, choice]
        """
        self._set_property('choice', value)


class PortMetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    TRANSMIT = 'transmit'
    LOCATION = 'location'
    LINK = 'link'
    CAPTURE = 'capture'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    BYTES_TX_RATE = 'bytes_tx_rate'
    BYTES_RX_RATE = 'bytes_rx_rate'

    def __init__(self, parent=None, choice=None, port_names=None, column_names=None):
        super(PortMetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_names', port_names)
        self._set_property('column_names', column_names)

    @property
    def port_names(self):
        # type: () -> list[str]
        """port_names getter

        The names of objects to return results for. An empty list will return all port row results.

        Returns: list[str]
        """
        return self._get_property('port_names')

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The names of objects to return results for. An empty list will return all port row results.

        value: list[str]
        """
        self._set_property('port_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        Returns: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned. The name of the port cannot be excluded.

        value: list[Union[transmit, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate]]
        """
        self._set_property('column_names', value)


class FlowMetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    TRANSMIT = 'transmit'
    PORT_TX = 'port_tx'
    PORT_RX = 'port_rx'
    FRAMES_TX = 'frames_tx'
    FRAMES_RX = 'frames_rx'
    BYTES_TX = 'bytes_tx'
    BYTES_RX = 'bytes_rx'
    FRAMES_TX_RATE = 'frames_tx_rate'
    FRAMES_RX_RATE = 'frames_rx_rate'
    LOSS = 'loss'

    def __init__(self, parent=None, choice=None, flow_names=None, column_names=None, metric_group_names=None):
        super(FlowMetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('flow_names', flow_names)
        self._set_property('column_names', column_names)
        self._set_property('metric_group_names', metric_group_names)

    @property
    def flow_names(self):
        # type: () -> list[str]
        """flow_names getter

        The names of flow objects to return results for. An empty list will return results for all flows.

        Returns: list[str]
        """
        return self._get_property('flow_names')

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flow objects to return results for. An empty list will return results for all flows.

        value: list[str]
        """
        self._set_property('flow_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        Returns: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        value: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        self._set_property('column_names', value)

    @property
    def metric_group_names(self):
        # type: () -> list[str]
        """metric_group_names getter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        Returns: list[str]
        """
        return self._get_property('metric_group_names')

    @metric_group_names.setter
    def metric_group_names(self, value):
        """metric_group_names setter

        Extend the details of flow metrics by specifying any configured flow packet header field metric_group names.

        value: list[str]
        """
        self._set_property('metric_group_names', value)


class Bgpv4MetricsRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    SESSIONS_TOTAL = 'sessions_total'
    SESSIONS_UP = 'sessions_up'
    SESSIONS_DOWN = 'sessions_down'
    SESSIONS_NOT_STARTED = 'sessions_not_started'
    ROUTES_ADVERTISED = 'routes_advertised'
    ROUTES_WITHDRAWN = 'routes_withdrawn'

    def __init__(self, parent=None, choice=None, device_names=None, column_names=None):
        super(Bgpv4MetricsRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('device_names', device_names)
        self._set_property('column_names', column_names)

    @property
    def device_names(self):
        # type: () -> list[str]
        """device_names getter

        The names of BGPv4 device to return results for. An empty list will return results for all BGPv4 devices.

        Returns: list[str]
        """
        return self._get_property('device_names')

    @device_names.setter
    def device_names(self, value):
        """device_names setter

        The names of BGPv4 device to return results for. An empty list will return results for all BGPv4 devices.

        value: list[str]
        """
        self._set_property('device_names', value)

    @property
    def column_names(self):
        # type: () -> list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv4 device cannot be excluded.

        Returns: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        return self._get_property('column_names')

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the BGPv4 device cannot be excluded.

        value: list[Union[sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn]]
        """
        self._set_property('column_names', value)


class MetricsResponse(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_metrics': 'PortMetricList',
        'flow_metrics': 'FlowMetricList',
        'bgpv4_metrics': 'Bgpv4MetricList',
    }

    PORT_METRICS = 'port_metrics'
    FLOW_METRICS = 'flow_metrics'
    BGPV4_METRICS = 'bgpv4_metrics'

    def __init__(self, parent=None, choice=None):
        super(MetricsResponse, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def choice(self):
        # type: () -> Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """choice getter

        TBD

        Returns: Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """
        return self._get_property('choice')

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[port_metrics, flow_metrics, bgpv4_metrics, choice, choice, choice]
        """
        self._set_property('choice', value)

    @property
    def port_metrics(self):
        # type: () -> PortMetricList
        """port_metrics getter

        TBD

        Returns: list[obj(snappi.PortMetric)]
        """
        return self._get_property('port_metrics', PortMetricList)

    @property
    def flow_metrics(self):
        # type: () -> FlowMetricList
        """flow_metrics getter

        TBD

        Returns: list[obj(snappi.FlowMetric)]
        """
        return self._get_property('flow_metrics', FlowMetricList)

    @property
    def bgpv4_metrics(self):
        # type: () -> Bgpv4MetricList
        """bgpv4_metrics getter

        TBD

        Returns: list[obj(snappi.Bgpv4Metric)]
        """
        return self._get_property('bgpv4_metrics', Bgpv4MetricList)


class PortMetric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, parent=None, choice=None, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        super(PortMetric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('location', location)
        self._set_property('link', link)
        self._set_property('capture', capture)
        self._set_property('frames_tx', frames_tx)
        self._set_property('frames_rx', frames_rx)
        self._set_property('bytes_tx', bytes_tx)
        self._set_property('bytes_rx', bytes_rx)
        self._set_property('frames_tx_rate', frames_tx_rate)
        self._set_property('frames_rx_rate', frames_rx_rate)
        self._set_property('bytes_tx_rate', bytes_tx_rate)
        self._set_property('bytes_rx_rate', bytes_rx_rate)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured port

        value: str
        """
        self._set_property('name', value)

    @property
    def location(self):
        # type: () -> str
        """location getter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        Returns: str
        """
        return self._get_property('location')

    @location.setter
    def location(self, value):
        """location setter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        value: str
        """
        self._set_property('location', value)

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        The state of the test port link The string can be up, down or a custom error message.

        Returns: Union[up, down]
        """
        return self._get_property('link')

    @link.setter
    def link(self, value):
        """link setter

        The state of the test port link The string can be up, down or a custom error message.

        value: Union[up, down]
        """
        self._set_property('link', value)

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        Returns: Union[started, stopped]
        """
        return self._get_property('capture')

    @capture.setter
    def capture(self, value):
        """capture setter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        value: Union[started, stopped]
        """
        self._set_property('capture', value)

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._get_property('frames_tx')

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._set_property('frames_tx', value)

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._get_property('frames_rx')

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._set_property('frames_rx', value)

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._get_property('bytes_tx')

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._set_property('bytes_tx', value)

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of valid bytes received

        Returns: int
        """
        return self._get_property('bytes_rx')

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of valid bytes received

        value: int
        """
        self._set_property('bytes_rx', value)

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._get_property('frames_tx_rate')

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._set_property('frames_tx_rate', value)

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._get_property('frames_rx_rate')

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._set_property('frames_rx_rate', value)

    @property
    def bytes_tx_rate(self):
        # type: () -> float
        """bytes_tx_rate getter

        The current rate of bytes transmitted

        Returns: float
        """
        return self._get_property('bytes_tx_rate')

    @bytes_tx_rate.setter
    def bytes_tx_rate(self, value):
        """bytes_tx_rate setter

        The current rate of bytes transmitted

        value: float
        """
        self._set_property('bytes_tx_rate', value)

    @property
    def bytes_rx_rate(self):
        # type: () -> float
        """bytes_rx_rate getter

        The current rate of bytes received

        Returns: float
        """
        return self._get_property('bytes_rx_rate')

    @bytes_rx_rate.setter
    def bytes_rx_rate(self, value):
        """bytes_rx_rate setter

        The current rate of bytes received

        value: float
        """
        self._set_property('bytes_rx_rate', value)


class PortMetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortMetricList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[PortMetric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortMetricList
        return self._iter()

    def __next__(self):
        # type: () -> PortMetric
        return self._next()

    def next(self):
        # type: () -> PortMetric
        return self._next()

    def metric(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        # type: () -> PortMetricList
        """Factory method that creates an instance of PortMetric class

        TBD
        """
        item = PortMetric(name=name, location=location, link=link, capture=capture, frames_tx=frames_tx, frames_rx=frames_rx, bytes_tx=bytes_tx, bytes_rx=bytes_rx, frames_tx_rate=frames_tx_rate, frames_rx_rate=frames_rx_rate, bytes_tx_rate=bytes_tx_rate, bytes_rx_rate=bytes_rx_rate)
        self._add(item)
        return self


class FlowMetric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'metric_groups': 'FlowMetricGroupList',
    }

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, parent=None, choice=None, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None):
        super(FlowMetric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('transmit', transmit)
        self._set_property('port_tx', port_tx)
        self._set_property('port_rx', port_rx)
        self._set_property('frames_tx', frames_tx)
        self._set_property('frames_rx', frames_rx)
        self._set_property('bytes_tx', bytes_tx)
        self._set_property('bytes_rx', bytes_rx)
        self._set_property('frames_tx_rate', frames_tx_rate)
        self._set_property('frames_rx_rate', frames_rx_rate)
        self._set_property('loss', loss)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured flow.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured flow.

        value: str
        """
        self._set_property('name', value)

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        The transmit state of the flow.

        Returns: Union[started, stopped, paused]
        """
        return self._get_property('transmit')

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        The transmit state of the flow.

        value: Union[started, stopped, paused]
        """
        self._set_property('transmit', value)

    @property
    def port_tx(self):
        # type: () -> str
        """port_tx getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('port_tx')

    @port_tx.setter
    def port_tx(self, value):
        """port_tx setter

        The name of a configured port

        value: str
        """
        self._set_property('port_tx', value)

    @property
    def port_rx(self):
        # type: () -> str
        """port_rx getter

        The name of a configured port

        Returns: str
        """
        return self._get_property('port_rx')

    @port_rx.setter
    def port_rx(self, value):
        """port_rx setter

        The name of a configured port

        value: str
        """
        self._set_property('port_rx', value)

    @property
    def frames_tx(self):
        # type: () -> int
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._get_property('frames_tx')

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._set_property('frames_tx', value)

    @property
    def frames_rx(self):
        # type: () -> int
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._get_property('frames_rx')

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._set_property('frames_rx', value)

    @property
    def bytes_tx(self):
        # type: () -> int
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._get_property('bytes_tx')

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._set_property('bytes_tx', value)

    @property
    def bytes_rx(self):
        # type: () -> int
        """bytes_rx getter

        The current total number of bytes received

        Returns: int
        """
        return self._get_property('bytes_rx')

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of bytes received

        value: int
        """
        self._set_property('bytes_rx', value)

    @property
    def frames_tx_rate(self):
        # type: () -> float
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._get_property('frames_tx_rate')

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._set_property('frames_tx_rate', value)

    @property
    def frames_rx_rate(self):
        # type: () -> float
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._get_property('frames_rx_rate')

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._set_property('frames_rx_rate', value)

    @property
    def loss(self):
        # type: () -> float
        """loss getter

        The percentage of lost frames

        Returns: float
        """
        return self._get_property('loss')

    @loss.setter
    def loss(self, value):
        """loss setter

        The percentage of lost frames

        value: float
        """
        self._set_property('loss', value)

    @property
    def metric_groups(self):
        # type: () -> FlowMetricGroupList
        """metric_groups getter

        Any configured flow packet header field metric_group names will appear as additional name/value pairs.

        Returns: list[obj(snappi.FlowMetricGroup)]
        """
        return self._get_property('metric_groups', FlowMetricGroupList)


class FlowMetricGroup(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, name=None, value=None):
        super(FlowMetricGroup, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('value', value)

    @property
    def name(self):
        # type: () -> str
        """name getter

        Name provided as part of a flow packet header field metric group

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        Name provided as part of a flow packet header field metric group

        value: str
        """
        self._set_property('name', value)

    @property
    def value(self):
        # type: () -> float
        """value getter

        The value of the flow packet header field

        Returns: float
        """
        return self._get_property('value')

    @value.setter
    def value(self, value):
        """value setter

        The value of the flow packet header field

        value: float
        """
        self._set_property('value', value)


class FlowMetricGroupList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricGroupList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowMetricGroup]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricGroupList
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def next(self):
        # type: () -> FlowMetricGroup
        return self._next()

    def metricgroup(self, name=None, value=None):
        # type: () -> FlowMetricGroupList
        """Factory method that creates an instance of FlowMetricGroup class

        A metric group
        """
        item = FlowMetricGroup(name=name, value=value)
        self._add(item)
        return self


class FlowMetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowMetricList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowMetric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowMetricList
        return self._iter()

    def __next__(self):
        # type: () -> FlowMetric
        return self._next()

    def next(self):
        # type: () -> FlowMetric
        return self._next()

    def metric(self, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None):
        # type: () -> FlowMetricList
        """Factory method that creates an instance of FlowMetric class

        TBD
        """
        item = FlowMetric(name=name, transmit=transmit, port_tx=port_tx, port_rx=port_rx, frames_tx=frames_tx, frames_rx=frames_rx, bytes_tx=bytes_tx, bytes_rx=bytes_rx, frames_tx_rate=frames_tx_rate, frames_rx_rate=frames_rx_rate, loss=loss)
        self._add(item)
        return self


class Bgpv4Metric(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        super(Bgpv4Metric, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('sessions_total', sessions_total)
        self._set_property('sessions_up', sessions_up)
        self._set_property('sessions_down', sessions_down)
        self._set_property('sessions_not_started', sessions_not_started)
        self._set_property('routes_advertised', routes_advertised)
        self._set_property('routes_withdrawn', routes_withdrawn)

    @property
    def name(self):
        # type: () -> str
        """name getter

        The name of a configured BGPv4 device.

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured BGPv4 device.

        value: str
        """
        self._set_property('name', value)

    @property
    def sessions_total(self):
        # type: () -> int
        """sessions_total getter

        Total number of session

        Returns: int
        """
        return self._get_property('sessions_total')

    @sessions_total.setter
    def sessions_total(self, value):
        """sessions_total setter

        Total number of session

        value: int
        """
        self._set_property('sessions_total', value)

    @property
    def sessions_up(self):
        # type: () -> int
        """sessions_up getter

        Sessions are in active state

        Returns: int
        """
        return self._get_property('sessions_up')

    @sessions_up.setter
    def sessions_up(self, value):
        """sessions_up setter

        Sessions are in active state

        value: int
        """
        self._set_property('sessions_up', value)

    @property
    def sessions_down(self):
        # type: () -> int
        """sessions_down getter

        Sessions are not active state

        Returns: int
        """
        return self._get_property('sessions_down')

    @sessions_down.setter
    def sessions_down(self, value):
        """sessions_down setter

        Sessions are not active state

        value: int
        """
        self._set_property('sessions_down', value)

    @property
    def sessions_not_started(self):
        # type: () -> int
        """sessions_not_started getter

        Sessions not able to start due to some internal issue

        Returns: int
        """
        return self._get_property('sessions_not_started')

    @sessions_not_started.setter
    def sessions_not_started(self, value):
        """sessions_not_started setter

        Sessions not able to start due to some internal issue

        value: int
        """
        self._set_property('sessions_not_started', value)

    @property
    def routes_advertised(self):
        # type: () -> int
        """routes_advertised getter

        Number of advertised routes sent

        Returns: int
        """
        return self._get_property('routes_advertised')

    @routes_advertised.setter
    def routes_advertised(self, value):
        """routes_advertised setter

        Number of advertised routes sent

        value: int
        """
        self._set_property('routes_advertised', value)

    @property
    def routes_withdrawn(self):
        # type: () -> int
        """routes_withdrawn getter

        Number of routes withdrawn

        Returns: int
        """
        return self._get_property('routes_withdrawn')

    @routes_withdrawn.setter
    def routes_withdrawn(self, value):
        """routes_withdrawn setter

        Number of routes withdrawn

        value: int
        """
        self._set_property('routes_withdrawn', value)


class Bgpv4MetricList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(Bgpv4MetricList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[Bgpv4Metric]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> Bgpv4MetricList
        return self._iter()

    def __next__(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def next(self):
        # type: () -> Bgpv4Metric
        return self._next()

    def metric(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        # type: () -> Bgpv4MetricList
        """Factory method that creates an instance of Bgpv4Metric class

        BGPv4 Router statistics and learned routing information
        """
        item = Bgpv4Metric(name=name, sessions_total=sessions_total, sessions_up=sessions_up, sessions_down=sessions_down, sessions_not_started=sessions_not_started, routes_advertised=routes_advertised, routes_withdrawn=routes_withdrawn)
        self._add(item)
        return self


class StateMetrics(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {
        'port_state': 'PortStateList',
        'flow_state': 'FlowStateList',
    }

    def __init__(self, parent=None, choice=None):
        super(StateMetrics, self).__init__()
        self._parent = parent
        self._choice = choice

    @property
    def port_state(self):
        # type: () -> PortStateList
        """port_state getter

        TBD

        Returns: list[obj(snappi.PortState)]
        """
        return self._get_property('port_state', PortStateList)

    @property
    def flow_state(self):
        # type: () -> FlowStateList
        """flow_state getter

        TBD

        Returns: list[obj(snappi.FlowState)]
        """
        return self._get_property('flow_state', FlowStateList)


class PortState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    UP = 'up'
    DOWN = 'down'

    STARTED = 'started'
    STOPPED = 'stopped'

    def __init__(self, parent=None, choice=None, name=None, link=None, capture=None):
        super(PortState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('link', link)
        self._set_property('capture', capture)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def link(self):
        # type: () -> Union[up, down]
        """link getter

        TBD

        Returns: Union[up, down]
        """
        return self._get_property('link')

    @link.setter
    def link(self, value):
        """link setter

        TBD

        value: Union[up, down]
        """
        self._set_property('link', value)

    @property
    def capture(self):
        # type: () -> Union[started, stopped]
        """capture getter

        TBD

        Returns: Union[started, stopped]
        """
        return self._get_property('capture')

    @capture.setter
    def capture(self, value):
        """capture setter

        TBD

        value: Union[started, stopped]
        """
        self._set_property('capture', value)


class PortStateList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(PortStateList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[PortState]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> PortStateList
        return self._iter()

    def __next__(self):
        # type: () -> PortState
        return self._next()

    def next(self):
        # type: () -> PortState
        return self._next()

    def state(self, name=None, link=None, capture=None):
        # type: () -> PortStateList
        """Factory method that creates an instance of PortState class

        TBD
        """
        item = PortState(name=name, link=link, capture=capture)
        self._add(item)
        return self


class FlowState(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    STARTED = 'started'
    STOPPED = 'stopped'
    PAUSED = 'paused'

    def __init__(self, parent=None, choice=None, name=None, transmit=None):
        super(FlowState, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('name', name)
        self._set_property('transmit', transmit)

    @property
    def name(self):
        # type: () -> str
        """name getter

        TBD

        Returns: str
        """
        return self._get_property('name')

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._set_property('name', value)

    @property
    def transmit(self):
        # type: () -> Union[started, stopped, paused]
        """transmit getter

        TBD

        Returns: Union[started, stopped, paused]
        """
        return self._get_property('transmit')

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        TBD

        value: Union[started, stopped, paused]
        """
        self._set_property('transmit', value)


class FlowStateList(SnappiList):
    __slots__ = ()

    def __init__(self):
        super(FlowStateList, self).__init__()

    def __getitem__(self, key):
        # type: () -> Union[FlowState]
        return self._getitem(key)

    def __iter__(self):
        # type: () -> FlowStateList
        return self._iter()

    def __next__(self):
        # type: () -> FlowState
        return self._next()

    def next(self):
        # type: () -> FlowState
        return self._next()

    def state(self, name=None, transmit=None):
        # type: () -> FlowStateList
        """Factory method that creates an instance of FlowState class

        TBD
        """
        item = FlowState(name=name, transmit=transmit)
        self._add(item)
        return self


class Capabilities(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, unsupported=None, formats=None):
        super(Capabilities, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('unsupported', unsupported)
        self._set_property('formats', formats)

    @property
    def unsupported(self):
        # type: () -> list[str]
        """unsupported getter

        A list of /components/schemas/... paths that are not supported.

        Returns: list[str]
        """
        return self._get_property('unsupported')

    @unsupported.setter
    def unsupported(self, value):
        """unsupported setter

        A list of /components/schemas/... paths that are not supported.

        value: list[str]
        """
        self._set_property('unsupported', value)

    @property
    def formats(self):
        # type: () -> list[str]
        """formats getter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        Returns: list[str]
        """
        return self._get_property('formats')

    @formats.setter
    def formats(self, value):
        """formats setter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        value: list[str]
        """
        self._set_property('formats', value)


class CaptureRequest(SnappiObject):
    __slots__ = ('_parent', '_choice')

    _TYPES = {}

    def __init__(self, parent=None, choice=None, port_name=None):
        super(CaptureRequest, self).__init__()
        self._parent = parent
        self._choice = choice
        self._set_property('port_name', port_name)

    @property
    def port_name(self):
        # type: () -> str
        """port_name getter

        The name of a port a capture is started on.

        Returns: str
        """
        return self._get_property('port_name')

    @port_name.setter
    def port_name(self, value):
        """port_name setter

        The name of a port a capture is started on.

        value: str
        """
        self._set_property('port_name', value)


class Api(object):
    """Snappi Abstract API
    """

    def __init__(self, host=None):
        self.host = host if host else "https://localhost"

    def set_config(self, payload):
        """POST /config

        Sets configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_config")

    def update_config(self, payload):
        """PATCH /config

        Updates configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("update_config")

    def get_config(self):
        """GET /config

        TBD

        Return: config
        """
        raise NotImplementedError("get_config")

    def set_transmit_state(self, payload):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_transmit_state")

    def set_link_state(self, payload):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_link_state")

    def set_capture_state(self, payload):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        raise NotImplementedError("set_capture_state")

    def get_metrics(self, payload):
        """POST /results/metrics

        TBD

        Return: metrics_response
        """
        raise NotImplementedError("get_metrics")

    def get_state_metrics(self):
        """POST /results/state

        TBD

        Return: state_metrics
        """
        raise NotImplementedError("get_state_metrics")

    def get_capabilities(self):
        """POST /results/capabilities

        TBD

        Return: capabilities
        """
        raise NotImplementedError("get_capabilities")

    def get_capture(self, payload):
        """POST /results/capture

        TBD

        Return: None
        """
        raise NotImplementedError("get_capture")

    def config(self):
        """Factory method that creates an instance of Config

        Return: Config
        """
        return Config()

    def details(self):
        """Factory method that creates an instance of Details

        Return: Details
        """
        return Details()

    def transmit_state(self):
        """Factory method that creates an instance of TransmitState

        Return: TransmitState
        """
        return TransmitState()

    def link_state(self):
        """Factory method that creates an instance of LinkState

        Return: LinkState
        """
        return LinkState()

    def capture_state(self):
        """Factory method that creates an instance of CaptureState

        Return: CaptureState
        """
        return CaptureState()

    def metrics_request(self):
        """Factory method that creates an instance of MetricsRequest

        Return: MetricsRequest
        """
        return MetricsRequest()

    def metrics_response(self):
        """Factory method that creates an instance of MetricsResponse

        Return: MetricsResponse
        """
        return MetricsResponse()

    def state_metrics(self):
        """Factory method that creates an instance of StateMetrics

        Return: StateMetrics
        """
        return StateMetrics()

    def capabilities(self):
        """Factory method that creates an instance of Capabilities

        Return: Capabilities
        """
        return Capabilities()

    def capture_request(self):
        """Factory method that creates an instance of CaptureRequest

        Return: CaptureRequest
        """
        return CaptureRequest()


class HttpApi(Api):
    """Snappi HTTP API
    """
    def __init__(self, host=None):
        super(HttpApi, self).__init__(host=host)
        self._transport = SnappiHttpTransport(host=self.host)

    def set_config(self, payload):
        """POST /config

        Sets configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/config",
            payload=payload,
            return_object=self.details(),
        )

    def update_config(self, payload):
        """PATCH /config

        Updates configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "patch",
            "/config",
            payload=payload,
            return_object=self.details(),
        )

    def get_config(self):
        """GET /config

        TBD

        Return: config
        """
        return self._transport.send_recv(
            "get",
            "/config",
            payload=None,
            return_object=self.config(),
        )

    def set_transmit_state(self, payload):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/transmit",
            payload=payload,
            return_object=self.details(),
        )

    def set_link_state(self, payload):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/link",
            payload=payload,
            return_object=self.details(),
        )

    def set_capture_state(self, payload):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.

        Return: details
        """
        return self._transport.send_recv(
            "post",
            "/control/capture",
            payload=payload,
            return_object=self.details(),
        )

    def get_metrics(self, payload):
        """POST /results/metrics

        TBD

        Return: metrics_response
        """
        return self._transport.send_recv(
            "post",
            "/results/metrics",
            payload=payload,
            return_object=self.metrics_response(),
        )

    def get_state_metrics(self):
        """POST /results/state

        TBD

        Return: state_metrics
        """
        return self._transport.send_recv(
            "post",
            "/results/state",
            payload=None,
            return_object=self.state_metrics(),
        )

    def get_capabilities(self):
        """POST /results/capabilities

        TBD

        Return: capabilities
        """
        return self._transport.send_recv(
            "post",
            "/results/capabilities",
            payload=None,
            return_object=self.capabilities(),
        )

    def get_capture(self, payload):
        """POST /results/capture

        TBD

        Return: None
        """
        return self._transport.send_recv(
            "post",
            "/results/capture",
            payload=payload,
            return_object=None,
        )


def api(host=None, ext=None):
    if ext is None:
        return HttpApi(host=host)

    try:
        lib = importlib.import_module("snappi_%s" % ext)
        return lib.Api(host=host)
    except ImportError as err:
        msg = "Snappi extension %s is not installed or invalid: %s"
        raise Exception(msg % (ext, err))
