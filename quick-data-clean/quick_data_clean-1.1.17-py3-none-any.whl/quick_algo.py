# -*- coding: utf-8 -*-

import binascii
import base64

from quick_data_clean.quick_common import Common
from PySmartCard.CpuCard import SmartCardAlgo


class DataAlgo(object):

    algo_obj = None

    @classmethod
    def base64_encode(cls, source_in, encoding="ansi"):
        return base64.b64encode(source_in.encode(encoding)).decode(encoding)

    @classmethod
    def base64_decode(cls, source_in, encoding="ansi"):
        return base64.b64decode(source_in).decode(encoding)

    @classmethod
    def get_sub_bytes(cls, source_byte, begin_index, length):
        return source_byte[begin_index:begin_index + length:1]

    @classmethod
    def xor(cls, source_1, source_2):

        Common.check_assign_type(source_1, Common.type_byte,
                                 "the first parameter of xor")

        Common.check_assign_type(source_2, Common.type_byte,
                                 "the second parameter of xor")

        result = bytearray([])
        if len(source_1) < len(source_2):
            for byte_index, byte_data in enumerate(source_1):
                result.append(byte_data ^ source_2[byte_index])
        else:
            for byte_index, byte_data in enumerate(source_2):
                result[byte_index] = byte_data ^ source_1[byte_index]

        return result

    def fenge(str1):
        alist = []
        for i in range(0, len(str1), 2):
            alist.append(str1[i:i + 2])
        return alist

    @classmethod
    def xor_single_bytes(cls, source_1):

        Common.check_assign_type(source_1, Common.type_byte,
                                 "the first parameter of xor")

        for index, byte_data in enumerate(source_1):
            if index == 0:
                byte_result = byte_data
            else:
                byte_result = byte_result ^ byte_data

        return bytes([byte_result])

    # '1234' -> b'\x12\x34'
    @classmethod
    def pack(cls, str_input):
        return binascii.a2b_hex(str_input)

    # b'\x12\x34'->'1234'
    @classmethod
    def un_pack(cls, byte_input):
        return binascii.b2a_hex(byte_input).decode()

    @classmethod
    def load_algo(cls):
        if cls.algo_obj is None:
            cls.algo_obj = SmartCardAlgo()

    @classmethod
    def des3_ecb(cls, data, key, type):
        cls.load_algo()
        return cls.algo_obj.des3_ecb(data, key, type)

    @classmethod
    def des3_cbc(cls, data, key, type, initial_vector="0000000000000000"):
        cls.load_algo()
        return cls.algo_obj.des3_cbc(data, key, type, initial_vector)

    @classmethod
    def des_ecb(cls, data, key, type):
        cls.load_algo()
        return cls.algo_obj.des_ecb(data, key, type)

    @classmethod
    def sm4_ecb(cls, data, key, type):
        cls.load_algo()
        return cls.algo_obj.sm4_ecb(data, key, type)

    @classmethod
    def sm4_cbc(cls, data, key, type,
                initial_vector="00000000000000000000000000000000"):
        cls.load_algo()
        return cls.algo_obj.sm4_cbc(data, key, type, initial_vector)

    @classmethod
    def mac_3des(cls, data, key, random=""):
        cls.load_algo()
        return cls.algo_obj.get_mac(data, key, random)

    @classmethod
    def mac_sm4(cls, data, key, random=""):
        cls.load_algo()
        return cls.algo_obj.get_mac_sm4(data, key, random)

