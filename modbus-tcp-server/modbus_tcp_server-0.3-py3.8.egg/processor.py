from .bits import BitStream, BitConsumer
from modbus_tcp_server.data_source import BaseDataSource
from modbus_tcp_server.datagrams import MODBUSTCPMessage
from satella.coding import rethrow_as

from .exceptions import IllegalAddress, IllegalValue, InvalidFrame, \
    GatewayTargetDeviceFailedToRespond, GatewayPathUnavailable, CustomMODBUSError
import weakref
import struct


STRUCT_HH = struct.Struct('>HH')
STRUCT_HHB = struct.Struct('>HHB')


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
    return STRUCT_HH.pack(address, value)


def write_single_register(db: BaseDataSource, unit_id: int, address: int, value: int) -> bytes:
    db.set_holding_register(unit_id, address, value)
    return STRUCT_HH.pack(address, value)


def write_multiple_registers(db: BaseDataSource, unit_id: int, msg: MODBUSTCPMessage) -> bytes:
    address, amount, databytes, reg_data = STRUCT_HHB.unpack(msg.data[1:6]), msg.data[6:]
    if databytes != 2*amount:
        raise InvalidFrame('Mismatch between writing amount and no of bytes')

    with rethrow_as(struct.error, InvalidFrame):
        for address, value in zip(range(address, address+amount),
                                  struct.unpack('>'+('H'*amount), reg_data)):
            db.set_holding_register(unit_id, address, value)
    return STRUCT_HH.pack(address, amount)


def write_multiple_coils(db: BaseDataSource, unit_id: int, msg: MODBUSTCPMessage) -> bytes:
    address, amount, databytes = STRUCT_HHB.unpack(msg.data[1:6])
    target_db = amount // 8
    if amount % 8:
        target_db += 1
    if target_db != databytes:
        raise InvalidFrame('Mismatch between writing amount and no of bytes')
    stream = BitConsumer(msg.data[6:])
    for address, value in zip(range(address, address+amount), stream):
        db.set_coil(unit_id, address, value)
    return STRUCT_HH.pack(address, amount)


TRANSLATION_TABLE = {
    0x03: (read_holding_registers, STRUCT_HH),
    0x04: (read_analog_inputs, STRUCT_HH),
    0x01: (read_coil, STRUCT_HH),
    0x02: (read_discrete_input, STRUCT_HH),
    0x05: (write_single_coil, STRUCT_HH),
    0x06: (write_single_register, STRUCT_HH),
    0x10: (write_multiple_registers, None),
    0x0F: (write_multiple_coils, None)
}


class ModbusProcessor:
    __slots__ = ('server', 'struct_cache')

    def __init__(self, server):
        self.server = weakref.proxy(server)

    def process(self, msg: MODBUSTCPMessage) -> MODBUSTCPMessage:
        """
        :raises InvalidFrame: invalid data frame
        """
        try:
            proc_fun, struct_inst = TRANSLATION_TABLE[msg.data[0]]
            if struct_inst is not None:
                args = struct_inst.unpack(msg.data[1:])
                return msg.respond(proc_fun(self.server.data_source, msg.unit_id, *args))
            else:
                return msg.respond(proc_fun(self.server.data_source, msg.unit_id, msg))
        except KeyError:
            return msg.respond(b'\x01', True)
        except CustomMODBUSError as e:
            return msg.respond(bytes([e.error_code]), True)
