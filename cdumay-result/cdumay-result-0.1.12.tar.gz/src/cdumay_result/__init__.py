#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
from typing import Optional, Any
from uuid import uuid4

import jsonpath_rw_ext
from cdumay_error import from_exc, Error
from cdumay_error.types import ValidationError
from marshmallow import Schema, fields, EXCLUDE


def random_uuid() -> str:
    """description of random_uuid"""
    return str(uuid4())


class ResultSchema(Schema):
    """Result (de)serializer"""

    class Meta:
        """Marshamllow field management"""
        unknown = EXCLUDE

    uuid = fields.String()
    retcode = fields.Integer(default=0)
    stdout = fields.String(default="")
    stderr = fields.String(default="")
    retval = fields.Dict()


class Result(object):
    """Result class"""

    def __init__(self,
                 retcode: Optional[int] = 0,
                 stdout: Optional[str] = "",
                 stderr: Optional[str] = "",
                 retval: Optional[dict] = None,
                 uuid: Optional[str] = None):
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr
        self.retval = retval or dict()
        self.uuid = uuid if uuid else random_uuid()

    def print(self, data: Any):
        """Store text in result's stdout

        :param Any data: Any printable data
        """
        self.stdout += "{}\n".format(data)

    def print_err(self, data: Any):
        """Store text in result's stderr

        :param Any data: Any printable data
        """
        self.stderr += "{}\n".format(data)

    @staticmethod
    def from_exception(exc: Exception, uuid: Optional[str] = None) -> "Result":
        """ Serialize an exception into a result"""
        return Result.from_error(
            from_exc(exc, extra=dict(uuid=uuid or random_uuid()))
        )

    @staticmethod
    def from_error(error: Error) -> "Result":
        """ Serialize an Error into a result"""
        return Result(
            uuid=error.extra.get("uuid", random_uuid()),
            retcode=error.code, stderr=error.message,
            retval=dict(error=error.to_dict())
        )

    def search_value(self,
                     xpath: str,
                     default: Optional[Any] = None,
                     fail_if_no_match: Optional[bool] = False) -> Optional[Any]:
        """ Try to find a value in the result.
        see https://github.com/kennknowles/python-jsonpath-rw#jsonpath-syntax

        :param str xpath: a xpath filter
        :param any default: default value if not found
        :param bool fail_if_no_match: Raise a ValidationError if no matches
        :return: the value found or None
        """
        matches = [
            match.value for match in
            jsonpath_rw_ext.parse(xpath).find(self.retval)
        ]
        if len(matches) == 0:
            if fail_if_no_match is True:
                raise ValidationError("No value found for xpath: '{}'".format(
                    xpath
                ))
            else:
                return default
        elif len(matches) == 1:
            return matches[0]
        else:
            return matches

    def __add__(self, o):
        """description of __add__"""
        self.retcode = self.retcode if self.retcode > o.retcode else o.retcode
        self.retval.update(o.retval)
        if o.stdout and (len(o.stdout) > 0):
            self.stdout = o.stdout
        if o.stderr and len(o.stderr) > 0:
            self.stderr = o.stderr
        return self

    def __str__(self):
        return self.stdout if self.retcode == 0 else self.stderr

    def __repr__(self):
        return "Result<retcode='{}'>".format(self.retcode)
