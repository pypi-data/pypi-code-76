#!/usr/bin/env python3
import unittest

from ltpylib.common_types import DataWithUnknownProperties, DataWithUnknownPropertiesAsAttributes


class TestDataWithUnknownProperties(unittest.TestCase):

  def test_DataWithUnknownProperties_empty(self):
    val = DataWithUnknownProperties(values={})
    assert val.unknownProperties is None

  def test_DataWithUnknownProperties_none(self):
    val = DataWithUnknownProperties(values=None)
    assert val.unknownProperties is None

  def test_DataWithUnknownProperties_some(self):
    values = {
      "field_num": 3,
      "field_str": "abc",
    }
    val = DataWithUnknownProperties(values=values)
    assert val.unknownProperties == values


class TestDataWithUnknownPropertiesAsAttributes(unittest.TestCase):

  def test_DataWithUnknownPropertiesAsAttributes(self):
    values = {
      "field_num": 3,
      "field_str": "abc",
    }
    val = DataWithUnknownPropertiesAsAttributes(values=values)
    assert hasattr(val, "field_num")
    assert getattr(val, "field_num") == 3
    assert val.field_num == 3

    assert hasattr(val, "field_str")
    assert getattr(val, "field_str") == "abc"
    assert val.field_str == "abc"

  def test_DataWithUnknownPropertiesAsAttributes_none(self):
    val = DataWithUnknownPropertiesAsAttributes(values=None)
    assert val is not None

    val = DataWithUnknownPropertiesAsAttributes(values={})
    assert val is not None


if __name__ == '__main__':
  unittest.main()
