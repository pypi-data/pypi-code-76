#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@corp.ovh.com>


"""
from collections import OrderedDict
from typing import Type, List

from cdumay_error import Error


class Registry(object):
    """Error registry"""
    __errors = OrderedDict()

    @classmethod
    def register(cls, clazz: Type[Error]) -> Type[Error]:
        """Register a new error type"""
        if clazz.MSGID not in cls.__errors:
            cls.__errors[clazz.MSGID] = clazz
        return clazz

    @classmethod
    def filter_by_status(cls, code: str) -> List[Type[Error]]:
        """Filter error by code"""
        return [x for x in cls.__errors.values() if x.CODE == code]

    @staticmethod
    def error_to_dict(clazz: Type[Error]) -> dict:
        """Serialize an Error Class to dict"""
        return dict(
            code=clazz.CODE, description=clazz.__doc__, msgid=clazz.MSGID,
            name=clazz.__name__
        )

    @classmethod
    def to_list(cls) -> List[dict]:
        """List all errors"""
        return [cls.error_to_dict(x) for x in cls.__errors.values()]

    @classmethod
    def to_dict(cls) -> OrderedDict:
        """Return all registered errors"""
        return cls.__errors

    @classmethod
    def craft_error(cls, msgid: str, **kwargs) -> Error:
        """Try to initialize error from dict"""
        data = dict(msgid=msgid, **kwargs)
        if msgid in cls.__errors.keys():
            return cls.__errors[msgid](**data)
        else:
            return Error(**data)
