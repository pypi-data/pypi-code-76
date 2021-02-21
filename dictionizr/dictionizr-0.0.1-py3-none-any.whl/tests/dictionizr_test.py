from __future__ import annotations
from typing import Optional

from dictionizr import dictionize, undictionize


class Data():
    name: str
    data: Optional[Data] = None
    optional: Optional[str] = None
    def __init__(self, name: str, sub_name: Optional[str] = None):
        self.name = name
        if sub_name is not None:
            self.data = Data(sub_name)
    def __eq__(self, o: Data) -> bool:
        return o is not None \
            and self.name == o.name \
            and ((self.data is None and o.data is None) or (self.data == o.data)) \
            and ((self.optional is None and o.optional is None) or (self.optional == o.optional))


def test__dictionize__property():
    data = Data('Joe')
    actual = dictionize(data)
    expected = { 'name': 'Joe' }
    assert expected == actual


def test__dictionize__no_functions():
    data = Data('Joe')
    actual = dictionize(data)
    expected = { 'name': 'Joe' }
    assert expected == actual


def test__dictionize__sub_objects():
    data = Data('Joe', 'John')
    actual = dictionize(data)
    expected = {
        'name': 'Joe',
        'data': { 'name': 'John'}
    }
    assert expected == actual


def test__undictionize__object():
    data = { 'name': 'Joe' }
    actual = undictionize(data, Data)
    expected = Data('Joe')
    assert expected == actual


def test__undictionize__sub_object():
    data = {
        'name': 'Joe',
        'data': { 'name': 'John'}
    }
    actual = undictionize(data, Data)
    expected = Data('Joe', 'John')
    assert expected == actual