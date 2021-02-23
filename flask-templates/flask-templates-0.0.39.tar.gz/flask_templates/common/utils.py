# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              __init__.py
    Description
    Author:                 develop
    date:                   4/3/2019
----------------------------------------------------
"""
__author__ = 'develop'

import functools
import requests
import hashlib
import os
import yaml
import sys
import math
import datetime
import pytz
import base64
import re
import simplejson as json
from decimal import Context, ROUND_HALF_UP
from itertools import chain
from itertools import groupby
from collections import OrderedDict

PRIVATE_KEY = "MjIxLDM1"


class BaseError(Exception):
    base_msg = 'base error'

    def __init__(self, msg):
        self.msg = self.base_msg + ":" + msg

    def __str__(self):
        return repr(self.msg)


def window_func(func, seq, window_size):
    return list(chain(*map(func, window(seq, window_size))))


def window(seq, window_size):
    """
    :param seq:
    :param window_size:
    :return:
    """
    st = 0
    while st < len(seq):
        yield seq[st:st + window_size]
        st += window_size


def get_platform():
    if "win" in sys.platform.lower():
        return "windows"
    elif "linux" in sys.platform.lower():
        return "linux"


def base64_encode_str(string):
    return base64.encodebytes(string.encode('utf-8')).decode('utf-8').strip()


def base64_decode_str(string):
    return base64.decodebytes(string.encode('utf-8')).decode('utf-8')


def module_import(module_name, sdk_name=None, version=None):
    try:
        __import__(module_name)
    except ImportError:
        os.system(
            'pip install {}'.format(sdk_name if sdk_name else module_name + ("" if not version else "==" + version)))
        __import__(module_name)


def encrypt(string, e_type='base64'):
    if e_type is None:
        return string
    elif e_type == 'base64':
        return base64_encode_str(string)
    else:
        raise Exception('e_type error!')


def decrypt(string, e_type='special'):
    if e_type is None or not string:
        return string
    elif e_type == 'base64':
        return base64_decode_str(string)
    elif e_type == 'special':
        if string.startswith('__c__'):
            return string[5:]
        return SpecialDecrypt.decrypt(string)
    else:
        raise Exception('e_type error!')


class SpecialDecrypt:
    base64str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    @staticmethod
    def cipher_to_dec_array(cipher):
        arr = []
        base64_index_map = {}
        for i in range(len(SpecialDecrypt.base64str)):
            base64_index_map[SpecialDecrypt.base64str[i]] = i
        for c in cipher:
            arr.append(base64_index_map[c])
        return arr

    @staticmethod
    def dec_array_to_bin_string(arr):
        s = ''
        for i in arr:
            s += bin(i).replace('b', '').zfill(6)[-6:]
        return s

    @staticmethod
    def dealBinStringToBinArray(s):
        count = int(len(s) / 8)
        strArr = []
        for i in range(count):
            substr = s[:8]
            s = s[8:]
            strArr.append(substr)
        return strArr

    @staticmethod
    def binArrayToDecArray(binArray):
        decArray = []
        for b in binArray:
            decArray.append(int(b, 2))
        return decArray

    @staticmethod
    def rsaDecryt(cryptASCII, pow, divisor):
        return (int(cryptASCII) ** pow) % divisor

    @staticmethod
    def rsaArray(arr, privateKey):
        s = str(base64.decodebytes(privateKey.encode(encoding='utf-8')), 'utf-8')
        sps = s.split(',')
        for i in range(len(arr)):
            arr[i] = SpecialDecrypt.rsaDecryt(arr[i], int(sps[1]), int(sps[0]))
        return arr

    @staticmethod
    def decrypt(cipher, privateKey=PRIVATE_KEY):
        arr = SpecialDecrypt.cipher_to_dec_array(cipher)
        binaryString = SpecialDecrypt.dec_array_to_bin_string(arr)
        binArray = SpecialDecrypt.dealBinStringToBinArray(binaryString)
        enDecArray = SpecialDecrypt.binArrayToDecArray(binArray)
        rsaArr = SpecialDecrypt.rsaArray(enDecArray, privateKey)
        return ''.join(map(chr, rsaArr))


def read_parm(request):
    res = dict()
    res.update(request.args)
    res.update(request.form)

    if request.is_json:
        res.update(request.json)
    elif request.data != b'':
        res.update(json.loads(request.data.decode()))
    header_json = request.headers.get('json')
    if header_json:
        res.update(json.loads(header_json))
    return res


def construct_result(code=0, message="success", data=None, **kwargs):
    """
    构造结果
    :return: 
    """
    res = {"code": code, "msg": message, "data": data}

    for one in kwargs:
        if one not in res:
            res[one] = kwargs[one]
    return json.dumps(res, ensure_ascii=False), {"Content-type": "application/json"}


def post_req(url, **kwargs):
    error_message = ""
    count = 0
    while count < 3:
        try:
            r = requests.post(url, **kwargs)
            if r.status_code == 200:
                return True, r.json()
            else:
                error_message = "post_req {} error ,status_code:{},params:{}".format(url, r.status_code, kwargs)
                count += 1
        except Exception as e:
            error_message = "post_req {} error {},params:{}".format(url, e, kwargs)
            count += 1
        print(error_message)
    return False, error_message


def get_md5(file_name=None, bytes=None):
    every_catch_num = 32000
    if file_name:
        if not os.path.exists(file_name):
            raise Exception("文件不存在")
        m = hashlib.md5()
        with open(file_name, "rb") as fd:
            while True:
                x = fd.read(every_catch_num)
                if not x:
                    break
                m.update(x)
        return m.hexdigest()
    elif bytes:
        m = hashlib.md5()
        length = len(bytes)
        cur_pos = 0
        for one in range(int(length / every_catch_num)):
            x = bytes[cur_pos:cur_pos + every_catch_num]
            m.update(x)
            cur_pos += every_catch_num
        m.update(bytes[cur_pos:])
        return m.hexdigest()
    else:
        raise ValueError("没有获取md5的对象")


def read_yaml(yaml_file, encoding="utf-8"):
    config = dict()
    if not yaml_file:
        return config
    with open(yaml_file, encoding=encoding) as fd:
        config = yaml.safe_load(fd)
    return config


def get_roud_num(num, sep=2):
    # 导进来的这个包在对于大于1的数进行四舍五入的时候是没有问题的，但在小于1的数的时候就会出问题
    num = str(num)
    if sep < 0:
        return int(float(num))
    if float(num) >= 1:
        if sep != 0:
            a = ("%.{}f".format(sep)) % float(num)
        else:
            a = "%d." % int(float(num))
        c = Context(prec=(len(a) - 1), rounding=ROUND_HALF_UP).create_decimal(num)
        res = float(str(c))
    else:
        d = float(num) * math.pow(10, sep)
        print(d)
        if d - int(d) < 0.5:
            res = float(int(d) / math.pow(10, sep))
        else:
            i = (int(d) + 1) / math.pow(10, sep)
            res = float(i)
    if sep == 0:
        return int(res)
    return res


def mix_change(src_iterator, desc_iterator):
    """
    复合替换dict
    :param src_iterator:
    :param desc_iterator:
    :return:
    """
    if type(src_iterator) == dict:
        all_dict = dict(src_iterator, **desc_iterator)
        for key in all_dict.keys():
            if key not in src_iterator:
                src_iterator[key] = all_dict[key]
                continue
            value = src_iterator[key]
            if type(value) == dict:
                mix_change(value, desc_iterator.get(key, {}))
            elif type(value) == list:
                mix_change(value, desc_iterator.get(key, None))
            else:
                value = desc_iterator.get(key, value)
                src_iterator[key] = value
    elif type(src_iterator) == list:
        # 列表暂时也用替换
        if desc_iterator is not None:
            src_iterator.clear()
            src_iterator.extend(desc_iterator)
    else:
        raise Exception('config_iter invalid')


def replace_variables_collection(src, **variables_dict):
    if type(src) == list:
        for index, item in enumerate(src):
            if type(item) == list or type(item) == dict:
                replace_variables_collection(item, **variables_dict)
            else:
                src[index] = replace_variables(item, **variables_dict)
    elif type(src) == dict:
        for key, value in src.items():
            if type(value) == list or type(value) == dict:
                replace_variables_collection(value, **variables_dict)
            else:
                src[key] = replace_variables(value, **variables_dict)


def replace_variables(src, key, push_set=None, **variables_dict):
    """
    if src like 'something ${a:c} nothing!',return 'something {} nothing!'.format(variables_dict.get('a',c)
    :param src:
    :param variables_dict:
    :return:
    """
    if type(src) != str:
        return src
    if not push_set:
        push_set = set()
    re_compile = re.compile(r'(\$[{](.*?)[}])')  # 最小匹配
    match_obj = re.findall(re_compile, src)
    for replace_item, piece in match_obj:
        pieces = piece.split(":")
        replaced_key = pieces[0]
        if replaced_key == key:
            raise Exception("replaced_key {} cycle!!".format(replaced_key))
        # if replaced_key in push_set:
        #     raise Exception("replaced_key {} cycle!!".format(replaced_key))
        value = variables_dict.get(replaced_key)
        if not value:  # 没有找到对应
            if len(pieces) > 1:  # 没有找到对应，有默认值
                value = pieces[1]
            else:
                raise Exception("replaced_key {} can't be found!!".format(replaced_key))
        else:  # 找到对应
            match_obj = re.findall(re_compile, value)
            if match_obj:  # 嵌套参数替换
                push_set.add(key)
                value = replace_variables(value, replaced_key, push_set, **variables_dict)
        src = src.replace(replace_item, value)
        # push_set.s
    return src


def iter_change(src_iterator, name_dict, name_list=None, sep='_'):
    """
    扁平化替换
    Parameters
    ----------
    src_iterator
    name_dict
    name_list
    sep

    Returns
    -------

    """
    if name_list is None:
        name_list = []
    if type(src_iterator) == dict:
        for key, value in src_iterator.items():
            name_list.append(key)
            if type(value) == dict or type(value) == list:
                iter_change(value, name_dict, name_list, sep=sep)
            else:
                env_key = sep.join(name_list)
                src_iterator[key] = name_dict.get(env_key, value)
            name_list.pop(-1)
    elif type(src_iterator) == list:
        index = 0
        for one in src_iterator:
            name_list.append(str(index))
            if type(one) == dict or type(one) == list:
                iter_change(one, name_dict, name_list, sep=sep)
            else:
                env_key = sep.join(name_list)
                src_iterator[index] = name_dict.get(env_key, one)
            index += 1
            name_list.pop(-1)
    else:
        raise Exception('config_iter invalid')


temp = {
    "x": "xxxxxxxx",
    "y": "yyyyyyyyyy${x}",
    "z": "zzzzzz${a}zzzz${y}",
    "a": "aaaaaa${b}aaaaa${x}",
    "b": "bbbbbb${c}",
    "c": "ccccccc${d.0.f}${y}",
    "d": [
        {
            "e": "eeeeee${a},${b}",
            "f": "ffffff",
            "g": "gggggg",
        }
    ]
}

re_compile = re.compile(r'(\$[{](.*?)[}])')


def config_pre_deal(value, key):
    if type(value) != str:
        result = {"value": value, "relative_map": dict()}
    else:
        match_obj = re.findall(re_compile, value)
        if match_obj:
            # 嵌套
            replace_set = set()
            relative_map = dict()
            for replace_item, piece in match_obj:
                pieces = piece.split(":")
                replaced_key = pieces[0]
                if replaced_key == key:
                    raise Exception("replaced_key {} cycle!!".format(replaced_key))
                relative_map.setdefault(replaced_key, set()).add(replace_item)

            result = {"value": value, "relative_map": relative_map}
        else:
            result = {"value": value, "relative_map": dict()}
    return result


def flat_collect(config, pre="", flat_dict=None):
    if flat_dict is None:
        flat_dict = dict()
    if type(config) == dict:
        for key, value in config.items():
            if type(value) == dict or type(value) == list:
                flat_collect(value, pre=pre + key + ".", flat_dict=flat_dict)
            else:
                flat_dict[pre + key] = config_pre_deal(value, pre + key)

    elif type(config) == list:
        for index, item in enumerate(config):
            if type(item) == dict or type(item) == list:
                flat_collect(item, pre=pre + str(index) + ".", flat_dict=flat_dict)
            else:
                flat_dict[pre + str(index)] = config_pre_deal(item, pre + str(index))
    else:
        pass


def replace_flat_dict(key, value, relative_map, variables_dict, stack=None):
    if stack is None:
        stack = OrderedDict()
    if key in stack:
        raise Exception("replaced_key {} cycle!!".format(key))
    stack[key] = 1
    for replaced_key in relative_map:
        if replaced_key not in variables_dict:  # 該替換項目不存在
            for replace_item in relative_map[replaced_key]:
                if replace_item == "${" + replaced_key + "}":
                    raise Exception("replaced_key {} can't be found!!".format(replaced_key))
                elif replaced_key + ":" in replace_item:
                    value = value.replace(replace_item, replace_item[2:-1].split(":")[-1])
        else:
            for replace_item in relative_map[replaced_key]:
                value = value.replace(replace_item,
                                      str(replace_flat_dict(replaced_key, variables_dict[replaced_key]['value'],
                                                            variables_dict[replaced_key]['relative_map'],
                                                            variables_dict, stack)))
    variables_dict[key] = {
        "value": value,
        "relative_map": {}
    }
    stack.pop(key)
    return value


def get_filter_dic(dic, filter_keys=None, require_all=False):
    """

    :param dic:
    :param filter_keys:
    :param require_all:
    :return:
    字典按key过滤
    """
    if not filter_keys:
        return {}
    if not require_all:
        return {k: dic[k] for k in filter_keys if k in dic}
    else:
        return {k: dic[k] for k in filter_keys}


def get_changed_value(src, change_dict=None, not_exist_exception=None, callback=None):
    result = src
    if callback:
        result = callback(src)
    if change_dict:
        if result not in change_dict:
            if not_exist_exception:
                raise not_exist_exception
        result = change_dict.get(result, result)
    return result


def align_list(src_list, another_list, according_name):
    temp_dict = dict()
    for another_dict in another_list:
        temp_dict[another_dict[according_name]] = another_dict
    result_list = list()
    for src_dict in src_list:
        key = src_dict[according_name]
        if key not in temp_dict:
            # 没有找到对应的
            pass
        else:
            temp_list = [src_dict, temp_dict[key]]
            result_list.append(temp_list)
    return result_list


def align_list_union(src_list, another_list, according_name):
    temp_dict = dict()
    for another_dict in another_list:
        temp_dict[another_dict[according_name]] = another_dict
    temp_dict2 = dict()
    for src_dict in src_list:
        temp_dict2[src_dict[according_name]] = src_dict
    result_list = list()
    for src_dict in src_list:
        key = src_dict[according_name]
        if key not in temp_dict:
            # 没有找到对应的
            temp_list = [src_dict, dict.fromkeys(src_dict)]
            result_list.append(temp_list)
        else:
            temp_list = [src_dict, temp_dict[key]]
            result_list.append(temp_list)
    for ana_dict in another_list:
        key = ana_dict[according_name]
        if key not in temp_dict2:
            # 没有找到对应的
            temp_list = [dict.fromkeys(ana_dict), ana_dict]
            result_list.append(temp_list)
        # else:
        #     pass
        # temp_list = [ana_dict, temp_dict2[key]]
        # result_list.append(temp_list)
    return result_list


def dict_list_sum(dict_list, group_field, sum_field):
    """
    字典列表聚合求和
    按照group_field分组， 对sum_field求和
    :param dict_list: eg: [{'a': 1, 'b':3}, {'a': 1, 'b':2}, {'a': 2, 'b':2}, {'a': 2, 'b':10}]
    :param group_field: eg 'a'
    :param sum_field: eg 'b'
    :return: eg: {1: 5, 2: 12}
    """
    dic = {}
    for item in dict_list:
        group_value = item[group_field]
        if group_value not in dic:
            dic[group_value] = 0
        dic[group_value] += item[sum_field]
    return dic


def update_many_sql(data_list, mysql_table, merge_keys=None):
    query = ""
    if not merge_keys:
        merge_keys = []
    for data_dict in data_list:
        if not query:
            columns = ', '.join('`{0}`'.format(k) for k in data_dict)
            duplicates = ', '.join(
                '{0}=VALUES({0})'.format(k) if k not in merge_keys else '{0}={0}+VALUES({0})'.format(k) for k in
                data_dict)

            place_holders = ', '.join(':{}'.format(k) for k in data_dict)
            query = "INSERT INTO {0} ({1}) VALUES ({2})".format(mysql_table, columns, place_holders)
            query = "{0} ON DUPLICATE KEY UPDATE {1}".format(query, duplicates)
    return query


def update_many_sql_diff(data_list, mysql_table, diff_keys=None):
    query = ""
    if not diff_keys:
        diff_keys = []
    for data_dict in data_list:
        if not query:
            columns = ', '.join('`{0}`'.format(k) for k in data_dict)
            duplicates = ', '.join(
                '{0}=VALUES({0})'.format(k) if k not in diff_keys else '{0}=VALUES({0})-{0}'.format(k) for k in
                data_dict)

            place_holders = ', '.join(':{}'.format(k) for k in data_dict)
            query = "INSERT INTO {0} ({1}) VALUES ({2})".format(mysql_table, columns, place_holders)
            query = "{0} ON DUPLICATE KEY UPDATE {1}".format(query, duplicates)
    return query


def get_res(key, item_list):
    """

    :param key: 输入
    :param item_list: 匹配的对象
    :return:
    """
    index_res = set()
    for item in item_list:
        for i in range(len(item)):
            if key.upper() in item[i]:
                index_res.add(i)
                if len(index_res) == 10:
                    break
        if len(index_res) == 10:
            break
            # if item[i].strip().startswith(key):
            #     index_res.add(i)
            #     if len(index_res) == 5:
            #         break

    res = [[item_list[0][i], item_list[1][i], item_list[2][i]] for i in index_res]
    return res


def set_dict_list_values(dict_seq, key, value, **kwargs):
    from copy import deepcopy
    for dic in deepcopy(dict_seq):
        flag = True
        for k, v in kwargs.items():
            if dic[k] != v:
                flag = False
                break
        if flag:
            dic[key] = value
    return dict_seq


def dict_to_key(dic):
    key = ''
    for k, v in sorted(dic.items()):
        v = round(v, 4)
        key += "{}_{};".format(k, v)
    return key


def timestamp_2_date(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone('Asia/Shanghai')).strftime(fmt)


def date_range(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    for n in range(int((end_date - start_date).days) + 1):
        yield str((start_date + datetime.timedelta(n)).date())


def get_format_yield_list(org_date_list, org_yield_list, format_list):
    """

    :param org_date_list: 交易日日期列表
    :param org_yield_list: 交易日持仓金额列表
    :param format_list: 自然日日日期列表
    :return: 自然日持仓金额列表
    第一天已对齐；自然日日日期列表 包含 交易日日期列表
    """
    # 二分法
    # seq_dict = {}
    # diff_list = sorted(set(format_list) - set(org_date_list))
    # for date in diff_list:
    #     seq = bisect_left(org_date_list, date)
    #     seq_dict[seq] = 1 + seq_dict.setdefault(seq, 0)

    # 需要插入的位置字典
    seq_dict = {}
    i = 0
    for j in range(len(format_list)):
        if i < len(org_date_list) and format_list[j] == org_date_list[i]:
            i += 1
        else:
            seq_dict[i] = 1 + seq_dict.setdefault(i, 0)
    format_yield_list = []
    pre_seq = 0
    for seq in sorted(seq_dict.keys()):
        format_yield_list += org_yield_list[pre_seq:seq] + seq_dict[seq] * [org_yield_list[seq - 1]]
        pre_seq = seq
    format_yield_list += org_yield_list[pre_seq:]
    return format_yield_list


def doublewrap(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    '''

    @functools.wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


# def chain(*args):
#     s = True
#     for e in args:
#         if s:
#             a = e
#             s = False
#         else:
#             a += e
#     return a

def get_sum_line(*args):
    dict_list = [{'date': k, 'value': v} for k, v in
                 chain(*[zip(el[0], el[1]) for el in args])]
    dict_list = sorted(dict_list, key=lambda x: x['date'])
    sum_list = [{'date': key, 'value': sum(d['value'] for d in group)} for key, group in
                groupby(dict_list, key=lambda d: d['date'])]
    date_list = [item['date'] for item in sum_list]
    amount_list = [item['value'] for item in sum_list]
    return date_list, amount_list


if __name__ == "__main__":
    pass

    print(chain((1, 3), (3, 2)))
    print(*chain({1: 3}, {3: 2}))
    # print({**{1:3,3:1},**{3:2}})
    # def a(*, b=1, c=3):
    #     print(b + c)
    print((1, 3) + (3, 2))

    # from collections import Iterator,Iterable
    # print(decrypt('QXBwXzQ5MTIwODgw'))
    # print(encrypt('sd61131707'))
    # print(update_many_sql([{'code':1}],'table1'))
    # print(list(date_range('2019-09-11','2019-9-29')))

    # print(set_dict_list_values(
    #     [{'asset_id': 3, 'holding_amount': 3000, 'holding_share': 8000, 'sub_asset_id': 6, 'security_id': '000003.MF'},
    #      {'asset_id': 2, 'holding_amount': 3000, 'holding_share': 8000, 'sub_asset_id': 6, 'security_id': '000003.MF'}],
    #     'holding_share', 0, asset_id=3))
    # print(get_platform())
    # print(get_roud_num(3.15, 1))
    #
    #
    # def my_round(t, n):
    #     i = abs(round(t * (10 ** (n + 1))))
    #     j = i % 10
    #     if j >= 5:
    #         m = (int(i / 10) + 1) * 10
    #     else:
    #         m = int(i / 10) * 10
    #     ret = m / (10 ** (n + 1))
    #     return ret if i >= 0 else -ret
    #
    #
    # print(my_round(-1.09, 1))
    # print(get_changed_value('hh', {'h': 2}, callback=lambda x: x[0]))
    # from decimal import Decimal
