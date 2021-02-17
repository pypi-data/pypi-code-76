#!/usr/bin/env python3


class TypeWithDictRepr(object):

  def __repr__(self):
    return str(self.__dict__)


class DataWithUnknownProperties(TypeWithDictRepr):

  def __init__(self, values: dict = None, skip_field_if_no_unknown: bool = False):
    if not skip_field_if_no_unknown or values:
      self.unknownProperties: dict = values if values else None


class DataWithUnknownPropertiesAsAttributes(DataWithUnknownProperties):

  def __init__(self, values: dict = None):
    if values:
      self.hasUnknownProperties: bool = True
      for item in values.items():
        setattr(self, str(item[0]), item[1])

      values.clear()

    DataWithUnknownProperties.__init__(self, values=None, skip_field_if_no_unknown=True)
