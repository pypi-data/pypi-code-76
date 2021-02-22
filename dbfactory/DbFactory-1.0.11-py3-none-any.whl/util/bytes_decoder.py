# -*- coding=utf8 -*-
# author caturbhuja
# date   2019/11/27 11:06
# wechat chending2012


def decoder(args, decode_type='utf8'):
    """
    这个方法，把输入的数据内部所有数据，解码成 decode_type 类型的数据，一个不漏
    :param args: python8种基础数据结构
    :param decode_type: 解码类型
    :return: 解码结果
    """
    if isinstance(args, dict):
        args = decode_dict(args, decode_type)
    elif isinstance(args, list):
        args = decode_list(args, decode_type)
    elif isinstance(args, tuple):
        args = decode_tuple(args, decode_type)
    elif isinstance(args, set):
        args = decode_set(args, decode_type)
    elif isinstance(args, bytes):
        args = args.decode(decode_type)
    elif isinstance(args, bool):
        pass
    else:
        print('args type maybe not support, args:{}, type:{}'.format(args, type(args)))
    return args


def decode_dict(_dict, decode_type='utf8'):
    """传入字典内数据解码"""
    _new_dict = dict()
    for keys, value in _dict.items():
        if isinstance(keys, bytes):
            keys = keys.decode(decode_type)
        if isinstance(value, bytes):
            value = value.decode(decode_type)
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, set):
            value.add(decode_set(value))
        elif isinstance(value, dict):
            value = decode_dict(value)
        _new_dict[keys] = value
    return _new_dict


def decode_list(_list, decode_type='utf8'):
    _new_list = list()
    for each in _list:
        if isinstance(each, dict):
            _new_list.append(decode_dict(each))
        elif isinstance(each, (list, tuple)):
            _new_list.append(decode_list(each))
        elif isinstance(each, set):
            _new_list.append(decode_set(each))
        elif isinstance(each, bytes):
            _new_list.append(each.decode(decode_type))
        elif isinstance(each, bool):
            _new_list.append(each)
        else:
            _new_list.append(each)
    return _new_list


def decode_tuple(_tuple, decode_type='utf8'):
    return tuple(decode_list(_tuple, decode_type))


def decode_set(_set, decode_type='utf8'):
    _new_set = set()
    for each in _set:
        if isinstance(each, bytes):
            _new_set.add(each.decode(decode_type))
        elif isinstance(each, tuple):
            _new_set.add(decode_tuple(each, decode_type))
        else:
            _new_set.add(each)
    return _new_set
