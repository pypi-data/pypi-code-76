from __future__ import annotations

from dictionizr import dictionize, undictionize

from .utils import eq


class ComplexObject:
    def __init__(self,
        required: str,
        *args,
        optional: str = '',
        **kwargs
    ) -> None:
        self.required = required
        self.args = args
        self.optional = optional
        self.kwargs = kwargs
    def __eq__(self, o: ComplexObject) -> bool:
        return eq(self, o)


def test__dictionize__complex_object():
    data = ComplexObject(
        'required',
        'arg1',
        'arg2',
        optional='optional',
        hello='world',
        hola='mundo',
    )
    actual = dictionize(data)
    expected = {
        'required': 'required',
        'optional': 'optional',
        'args': [
            'arg1',
            'arg2',
        ],
        'kwargs': {
            'hello': 'world',
            'hola': 'mundo',
        }
    }
    assert expected == actual


def test__undictionize__complex_object():
    data = {
        'required': 'required',
        'optional': 'optional',
        'args': [
            'arg1',
            'arg2',
        ],
        'kwargs': {
            'hello': 'world',
            'hola': 'mundo',
        }
    }
    actual = undictionize(data, ComplexObject)
    expected = ComplexObject(
        'required',
        'arg1',
        'arg2',
        optional='optional',
        hello='world',
        hola='mundo',
    )
    assert expected == actual
