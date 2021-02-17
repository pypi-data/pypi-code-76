from modbus_tcp_server.bits import BitStream
from modbus_tcp_server.data_source import BaseDataSource
from modbus_tcp_server.datagrams import MODBUSTCPMessage
import weakref
import struct


STRUCT_H = struct.Struct('>H')


def read_holding_registers(db: BaseDataSource, unit_id: int, address_start: int, amount: int):
    output = []
    for address in range(address_start, address_start + amount):
        output.append(db.get_holding_register(unit_id, address))
    output_len = len(output)
    return struct.pack('>H'+('H'*output_len), output_len*2, *output)


def read_analog_inputs(db: BaseDataSource, unit_id: int, address_start: int, amount: int):
    output = []
    for address in range(address_start, address_start + amount):
        output.append(db.get_analog_input(unit_id, address))
    output_len = len(output)
    return struct.pack('>H'+('H'*output_len), output_len*2, *output)


def read_coil(db: BaseDataSource, unit_id: int, address_start: int, amount: int):
    bs = BitStream()
    for address in range(address_start, address_start + amount):
        bs.add(db.get_coil(unit_id, address))
    return bytes([len(bs)]) + bytes(bs)


def read_discrete_input(db: BaseDataSource, unit_id: int, address_start: int, amount: int):
    bs = BitStream()
    for address in range(address_start, address_start + amount):
        bs.add(db.get_discrete_input(unit_id, address))
    return bytes([len(bs)]) + bytes(bs)


def write_single_coil(db: BaseDataSource, unit_id: int, address: int, value: int) -> bytes:
    db.set_coil(unit_id, address, value == 0xFF00)
    return struct.pack('>HH', address, value)


def write_single_register(db: BaseDataSource, unit_id: int, address: int, value: int) -> bytes:
    db.set_holding_register(unit_id, address, value)
    return struct.pack('>HH', address, value)


TRANSLATION_TABLE = {
    0x03: (read_holding_registers, '>HH'),
    0x04: (read_analog_inputs, '>HH'),
    0x01: (read_coil, '>HH'),
    0x02: (read_discrete_input, '>HH'),
    0x05: (write_single_coil, '>HH'),
    0x06: (write_single_register, '>HH'),
}


class ModbusProcessor:
    __slots__ = ('server', 'struct_cache')

    def __init__(self, server):
        self.server = weakref.proxy(server)
        self.struct_cache = {}

    def get_struct(self, str_: str) -> struct.Struct:
        if str_ not in self.struct_cache:
            self.struct_cache[str_] = struct.Struct(str_)
        return self.struct_cache[str_]

    def process(self, msg: MODBUSTCPMessage) -> MODBUSTCPMessage:
        try:
            proc_fun, str_ = TRANSLATION_TABLE[msg.data[0]]
            st = self.get_struct(str_)
            args = st.unpack(msg.data[1:])
            return msg.respond(proc_fun(self.server.data_source, msg.unit_id, *args))
        except KeyError:
            return msg.respond(b'\x01', True)
