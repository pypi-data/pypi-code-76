from .bits import BitStream, BitConsumer
from modbus_tcp_server.data_source import BaseDataSource
from modbus_tcp_server.datagrams import MODBUSTCPMessage
from satella.coding import rethrow_as

from .exceptions import IllegalAddress, IllegalValue, InvalidFrame, \
    GatewayTargetDeviceFailedToRespond, GatewayPathUnavailable
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


def write_multiple_registers(db: BaseDataSource, unit_id: int, msg: MODBUSTCPMessage) -> bytes:
    address, amount, databytes, reg_data = struct.unpack('>HHB', msg.data[1:6]), msg.data[6:]
    if databytes != 2*amount:
        raise InvalidFrame('Mismatch between writing amount and no of bytes')

    with rethrow_as(struct.error, InvalidFrame):
        for address, value in zip(range(address, address+amount),
                                  struct.unpack('>'+('H'*amount), reg_data)):
            db.set_holding_register(unit_id, address, value)
    return struct.pack('>HH', address, amount)


def write_multiple_coils(db: BaseDataSource, unit_id: int, msg: MODBUSTCPMessage) -> bytes:
    address, amount, databytes = struct.unpack('>HHB', msg.data[1:6])
    target_db = amount // 8
    if amount % 8:
        target_db += 1
    if target_db != databytes:
        raise InvalidFrame('Mismatch between writing amount and no of bytes')
    stream = BitConsumer(msg.data[6:])
    for address, value in zip(range(address, address+amount), stream):
        db.set_coil(unit_id, address, value)
    return struct.pack('>HH', address, amount)


TRANSLATION_TABLE = {
    0x03: (read_holding_registers, '>HH'),
    0x04: (read_analog_inputs, '>HH'),
    0x01: (read_coil, '>HH'),
    0x02: (read_discrete_input, '>HH'),
    0x05: (write_single_coil, '>HH'),
    0x06: (write_single_register, '>HH'),
    0x10: (write_multiple_registers, None),
    0x0F: (write_multiple_coils, None)
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
        """
        :raises InvalidFrame: invalid data frame
        """
        try:
            proc_fun, str_ = TRANSLATION_TABLE[msg.data[0]]
            if str_ is not None:
                st = self.get_struct(str_)
                args = st.unpack(msg.data[1:])
                return msg.respond(proc_fun(self.server.data_source, msg.unit_id, *args))
            else:
                return msg.respond(proc_fun(self.server.data_source, msg.unit_id, msg))
        except KeyError:
            return msg.respond(b'\x01', True)
        except IllegalAddress:
            return msg.respond(b'\x02', True)
        except IllegalValue:
            return msg.respond(b'\x03', True)
        except GatewayTargetDeviceFailedToRespond:
            return msg.respond(b'\x0B', True)
        except GatewayPathUnavailable:
            return msg.respond(b'\x0A', True)
