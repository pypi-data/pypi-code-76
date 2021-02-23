from dfx_utils.helper import json_friendly_dumps
from typing import Dict
import time


class SuperDict:
    """
    data = SuperDict()
    data['a.b'] = 1 => {'a': {'b': 1}}
    """

    def __init__(self, _dict: dict = None, _sep='.'):
        self._sep = _sep
        self._dict = _dict or {}

    def __getitem__(self, item):
        tmp_data = None
        if self._sep in item:
            tmp_dict = self._dict
            for key in item.split(self._sep):
                tmp_data = tmp_dict.get(key)
                if tmp_data is not None:
                    if tmp_data and isinstance(tmp_data, dict):
                        tmp_dict = tmp_data
        else:
            tmp_data = self._dict.get(item)
        return SuperDict(tmp_data) if isinstance(tmp_data, dict) else tmp_data

    def __setitem__(self, key, value):
        if self._sep in key:
            tmp_dict = self._dict
            keys = key.split(self._sep)
            for idx, item in enumerate(keys):
                if idx == len(keys) - 1:
                    tmp_dict[item] = value
                else:
                    tmp_dict[item] = tmp_dict.get(item, {})
                    tmp_dict = tmp_dict[item]
        else:
            self._dict[key] = value

    def __getattribute__(self, item):
        """ 当调用的函数不存在时，去self._dict里面找 """
        try:
            return super(SuperDict, self).__getattribute__(item)
        except AttributeError:
            return self._dict.__getattribute__(item)

    def __str__(self):
        return json_friendly_dumps(self._dict)

    def clear(self):
        self._dict = {}

    def get(self, item, default=None):
        ret_data = self.__getitem__(item)
        return ret_data if ret_data is not None else default


class BaseData(object):
    def __init__(self, **kwargs):
        self += kwargs
        # 记录实例化时间，用于排序
        self._created_at = time.time()

    def __add__(self, other: Dict):
        """ 使用加法的形式添加数据
        tmp = BaseData()
        tmp += {'a': 1}
        """
        if not isinstance(other, Dict):
            raise Exception('BaseData need dict')
        for key, val in other.items():
            self[key] = val
        return self

    def __lt__(self, other):
        """ 根据时间排序，默认升序排列 """
        return self._created_at < other._created_at

    def __getattribute__(self, item):
        """ 当访问的属性不存在时，返回 None """
        try:
            return super().__getattribute__(item)
        except Exception:
            return None

    def __getitem__(self, item):
        """ 该函数使实例可以像字典一样为属性赋值 """
        return getattr(self, item)

    def __setitem__(self, key, value):
        """ 该函数使实例可以像字典一样获取属性值 """
        setattr(self, key, value)

    def __delitem__(self, key):
        """ 该函数使实例可以像字典一样删除属性 """
        delattr(self, key)

    def __call__(self):
        """ 使实例可执行，返回一个属性字典 """
        ret = dict()
        for item in dir(self):
            if not item.startswith('_'):
                ret[item] = getattr(self, item)
        return ret

    def __str__(self):
        """ 序列化实例字典 """
        return json_friendly_dumps(self())


class SuperData(BaseData):
    def __setitem__(self, key, value):
        setattr(self, key, SuperData(**value) \
            if isinstance(value, Dict) else value)

    def __call__(self):
        ret = dict()
        for item in dir(self):
            if item.startswith('_'): continue
            value = getattr(self, item)
            ret[item] = value() \
                if isinstance(value, SuperData) else value
        return ret
