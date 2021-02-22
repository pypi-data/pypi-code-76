# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:    singleton.py
   Description:  单例模式
   Author:       Caturbhuja
   date:         2020/8/31
   WeChat:       chending2012
-------------------------------------------------
   Change Activity:
       2020/8/31:   DB工厂类创建

-------------------------------------------------
"""
__author__ = 'Caturbhuja'


class Singleton(type):
    """
    Singleton Metaclass
    """
    _inst = dict()

    def __call__(cls, *args, **kwargs):
        db_type = kwargs.get("db_type", "mysql")
        singleton_switch = kwargs.get("singleton_switch", False)
        singleton_num = str(kwargs.get("singleton_num", '0'))
        singleton_sign = "{}_{}".format(db_type, singleton_num)
        if singleton_switch:
            if singleton_sign not in cls._inst:
                kwargs["singleton_sign"] = singleton_sign
                cls._inst[singleton_sign] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._inst[singleton_sign]
        else:
            kwargs["singleton_sign"] = "{}_singleton_off".format(singleton_sign)
            return super(Singleton, cls).__call__(*args, **kwargs)
