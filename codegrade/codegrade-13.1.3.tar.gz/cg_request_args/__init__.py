"""This module defines parsers and validators for JSON data.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import re
import abc
import sys
import copy
import enum
import json as _json
import uuid
import typing as t
import inspect
import datetime
import textwrap
import warnings
import functools
import contextlib
import collections
import dataclasses
import email.utils

import structlog
import validate_email
import dateutil.parser
from typing_extensions import Final, Literal, Protocol, TypedDict

import cg_maybe
from cg_dt_utils import DatetimeWithTimezone

from ._utils import is_typeddict

try:
    import flask
    from werkzeug.datastructures import FileStorage
except ImportError:  # pragma: no cover
    pass

try:
    from cg_helpers import readable_join
except ImportError:  # pragma: no cover

    def readable_join(lst: t.Sequence[str]) -> str:
        """Simple implementation of ``readable_join``.
        """
        return ', '.join(lst)


logger = structlog.get_logger()

if t.TYPE_CHECKING:  # pragma: no cover
    # pylint: disable=unused-import
    from .open_api import OpenAPISchema

_T = t.TypeVar('_T')
_T_COV = t.TypeVar('_T_COV', covariant=True)  # pylint: disable=invalid-name
_Y = t.TypeVar('_Y')
_Z = t.TypeVar('_Z')
_X = t.TypeVar('_X')

_ParserErrorT = t.TypeVar('_ParserErrorT', bound='ParseError')

_CallableT = t.TypeVar('_CallableT', bound=t.Callable)
_USE_SLOTS = sys.version_info >= (3, 7)


class _BaseDict(TypedDict):
    pass


class _GEComparable(Protocol):
    def __ge__(self: _T, other: _T) -> bool:
        ...


_GEComparableT = t.TypeVar('_GEComparableT', bound=_GEComparable)

_BaseDictT = t.TypeVar('_BaseDictT', bound=_BaseDict)

_GENERATE_SCHEMA: t.Optional['OpenAPISchema'] = None


@contextlib.contextmanager
def _schema_generator(schema: 'OpenAPISchema'
                      ) -> t.Generator[None, None, None]:
    global _GENERATE_SCHEMA  # pylint: disable=global-statement
    _GENERATE_SCHEMA = schema
    try:
        yield
    finally:
        _GENERATE_SCHEMA = None


class _Schema(BaseException):
    def __init__(self, typ: str, schema: t.Mapping[str, t.Any]) -> None:
        super().__init__()
        self.schema = schema
        self.typ = typ


@dataclasses.dataclass(frozen=True)
class _SwaggerFunc:
    if _USE_SLOTS:
        __slots__ = ('operation_name', 'no_data', 'func', 'query_parser')
    operation_name: str
    no_data: bool
    func: t.Callable
    query_parser: t.Optional['BaseFixedMapping']


_SWAGGER_FUNCS: t.Dict[str, _SwaggerFunc] = {}


def swaggerize(
    operation_name: str,
    *,
    no_data: bool = False,
) -> t.Callable[[_CallableT], _CallableT]:
    """Mark this function as a function that should be included in the open api
    docs.

    :param operation_name: The name that the route should have in the client
        API libraries.
    :param no_data: If this is a route that can take input data (``PATCH``,
        ``PUT``, ``POST``), but doesn't you should pass ``True`` here. If you
        don't the function should contain a call to ``from_flask`` as the first
        statement of the function.
    """

    def __wrapper(func: _CallableT) -> _CallableT:
        if func.__name__ in _SWAGGER_FUNCS:  # pragma: no cover
            raise AssertionError(
                'The function {} was already registered.'.format(
                    func.__name__
                )
            )
        query_params = [
            inspect.Parameter(
                name=value.name[len('query_'):],
                kind=value.kind,
                default=value.default,
                annotation=value.annotation,
            ) for value in inspect.signature(func).parameters.values()
            if value.name.startswith('query_')
        ]
        if not query_params:
            query_parser = None
        else:
            query_parser = BaseFixedMapping.from_function_parameters_list(
                query_params,
                from_query=True,
            )

        _SWAGGER_FUNCS[func.__name__] = _SwaggerFunc(
            operation_name, no_data, func, query_parser=query_parser
        )
        if query_parser is None:
            return func

        # Mypy know that this is never ``None`` so we can use it without check.
        _parser = query_parser

        @functools.wraps(func)
        def __inner(*args: t.Any, **kwargs: t.Any) -> t.Any:
            for key, value in _parser.try_parse_and_log(
                flask.request.args,
                msg='Query parameters processed',
            ).items():
                kwargs[f'query_{key}'] = value
            return func(*args, **kwargs)

        return t.cast(_CallableT, __inner)

    return __wrapper


class ParseError(ValueError):
    """Error raised when a parser fails.
    """
    if _USE_SLOTS:
        __slots__ = ('parser', 'found', 'extra', 'location', '__as_string')

    def __init__(
        self,
        parser: '_ParserLike',
        found: object,
        *,
        extra: t.Mapping[str, str] = None
    ):
        super().__init__()
        self.parser = parser
        self.found = found
        self.extra = {} if extra is None else extra
        self.location: t.Sequence[t.Union[int, str]] = []
        self.__as_string: t.Optional[str] = None

    def _loc_to_str(self) -> str:
        res = []
        for idx, loc in enumerate(self.location):
            if idx == 0:
                res.append(str(loc))
            elif isinstance(loc, int):
                res.append('[{}]'.format(loc))
            else:
                res.append('.{}'.format(loc))

        return ''.join(res)

    def __str__(self) -> str:
        if self.__as_string is None:
            res = f'{self._to_str()}.'
            self.__as_string = f'{res[0].upper()}{res[1:]}'
        return self.__as_string

    def _to_str(self) -> str:
        got = repr(self.found)
        described = self.parser.describe()

        if described[0].lower() in ('a', 'i', 'e', 'u'):
            prefix = 'an'
        else:
            prefix = 'a'
        base = '{} {} is required, but got {}'.format(prefix, described, got)

        if self.extra.get('message') is not None:
            base = f'{base} ({self.extra["message"]})'

        if self.location:
            return 'at index "{}" {}'.format(self._loc_to_str(), base)
        return base

    def __copy__(self: _ParserErrorT) -> _ParserErrorT:
        res = type(self)(self.parser, self.found, extra=self.extra)
        res.location = self.location
        return res

    def add_location(
        self: _ParserErrorT, location: t.Union[int, str]
    ) -> _ParserErrorT:
        """Get a new error with the added location.
        """
        res = copy.copy(self)
        res.location = [location, *res.location]
        return res

    def to_dict(self) -> t.Mapping[str, t.Any]:
        """Convert the error to a dictionary.
        """
        return {
            'found': type(self.found).__name__,
            'expected': self.parser.describe(),
        }


class SimpleParseError(ParseError):
    """The parse error raised when the value was incorrect.
    """


class MultipleParseErrors(ParseError):
    """The parse error raised when the container type the value was correct,
    but the values contained parse errors.
    """

    def __init__(
        self,
        parser: '_ParserLike',
        found: object,
        errors: t.Sequence[ParseError] = None,
        *,
        extra: t.Mapping[str, str] = None,
    ):
        super().__init__(parser, found, extra=extra)
        self.errors = [] if errors is None else errors

    def __copy__(self) -> 'MultipleParseErrors':
        res = super().__copy__()
        res.errors = self.errors
        return res

    def _to_str(self) -> str:
        res = super()._to_str()
        if not self.errors:  # pragma: no cover
            # In this case you shouldn't really use this class.
            return res
        reasons = readable_join([err._to_str() for err in self.errors])  # pylint: disable=protected-access
        return f'{res}, which is incorrect because {reasons}'

    def to_dict(self) -> t.Mapping[str, t.Any]:
        return {
            **super().to_dict(),
            'sub_errors': [{
                'error': err.to_dict(),
                'location': err.location,
            } for err in self.errors],
        }


class _ParserLike(Protocol):
    def describe(self) -> str:
        ...


LogReplacer = t.Callable[[str, object], object]

_ParserT = t.TypeVar('_ParserT', bound='Parser')


class Parser(t.Generic[_T_COV]):
    """Base class for a parser.
    """
    if _USE_SLOTS:
        __slots__ = (
            '__description',
            '__schema_name',
            '_use_readable_describe',
            '__open_api_metadata',
        )

    def __init__(self) -> None:
        self.__description: Final[t.Optional[str]] = None
        self.__schema_name: Final[t.Optional[str]] = None
        self._use_readable_describe: Final[bool] = False
        self.__open_api_metadata: Final[t.Optional[t.Mapping[str, object]]
                                        ] = None

    def use_readable_describe(self: _ParserT, readable: bool) -> _ParserT:
        """Enable (or disable) the option to use a more readable version of the
        ``describe`` method.

        This might cause the describe to be slower, so only enable when really
        needed or if the speed doesn't matter.
        """
        res = copy.copy(self)
        # We cannot assign to this property normally as it is final.
        # pylint: disable=protected-access
        res._use_readable_describe = readable  # type: ignore[misc]
        return res

    def add_description(self: _ParserT, description: str) -> _ParserT:
        """Add a description to the parser.

        :param description: The description to add.

        :returns: A new parser with the given description.
        """
        res = copy.copy(self)
        # We cannot assign to this property normally as it is final.
        # pylint: disable=protected-access
        res.__description = description  # type: ignore[misc]
        return res

    def as_schema(self: _ParserT, name: str) -> _ParserT:
        """Add this parser as a separate model to the OpenAPI spec.

        :param name: The name of the model in the spec.
        """
        res = copy.copy(self)
        # We cannot assign to this property normally as it is final.
        # pylint: disable=protected-access
        res.__schema_name = name  # type: ignore[misc]
        return res

    def add_open_api_metadata(
        self: _ParserT, key: str, value: object
    ) -> _ParserT:
        """Add metadata for open api.

        :param key: The key under which the data should be store.
        :param value: The value that should be stored.
        """
        res = copy.copy(self)
        old_metadata = self.__open_api_metadata
        if old_metadata is None:
            old_metadata = {}
        metadata = {
            **old_metadata,
            key: value,
        }
        # We cannot assign to this property normally as it is final.
        # pylint: disable=protected-access
        res.__open_api_metadata = metadata  # type: ignore[misc]
        return res

    @abc.abstractmethod
    def try_parse(self, value: object) -> _T_COV:
        """Try and parse the given ``value```.

        :param value: The value it should try and parse.

        :returns: The parsed value.

        :raises _ParserError: If the value could not be parsed.
        """
        ...

    @abc.abstractmethod
    def describe(self) -> str:
        """Describe this parser, used for error messages.
        """
        ...

    @abc.abstractmethod
    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        ...

    def to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        """Convert this parser to an OpenAPI schema.
        """
        res = self._to_open_api(schema)
        if self.__open_api_metadata is not None:
            res = {**res, **self.__open_api_metadata}

        if self.__description is not None:
            desc = schema.make_comment(self.__description)
            if '$ref' in res:
                res = {'description': desc, 'allOf': [res]}
            else:
                res = {**res, 'description': desc}

        if self.__schema_name is None:
            return res
        else:
            return schema.add_as_schema(self.__schema_name, res, object())

    def __or__(
        self: 'Parser[_T]', other: 'Parser[_Y]'
    ) -> 'Parser[t.Union[_T, _Y]]':
        return Union(self, other)

    def from_flask(self, *, log_replacer: LogReplacer = None) -> _T_COV:
        """Parse the data from the current flask request.

        :param log_replacer: See :meth:`Parser.try_parse_and_log`.

        :returns: The parsed json from the current flask request.
        """
        if _GENERATE_SCHEMA is not None:
            json_schema = self.to_open_api(_GENERATE_SCHEMA)
            raise _Schema(typ='application/json', schema=json_schema)

        json = flask.request.get_json()
        return self.try_parse_and_log(json, log_replacer=log_replacer)

    def try_parse_and_log(
        self,
        json: object,
        *,
        log_replacer: LogReplacer = None,
        msg: str = 'JSON request processed',
    ) -> _T_COV:
        """Log and try to parse the given ``json``

        :param json: The object you want to try and parse.
        :param log_replacer: This function will be used to remove any sensitive
            data from the json before logging.

        :returns: The parsed data.
        """
        if log_replacer is None:
            logger.info(msg, request_data=json)
        elif isinstance(json, dict):
            to_log = {k: log_replacer(k, v) for k, v in json.items()}
            logger.info(msg, request_data=to_log)
        else:
            # The replacers are used for top level objects, in this case it is
            # better to be extra sure we don't log passwords so simply the
            # type.
            logger.info(
                msg,
                request_data='<FILTERED>',
                request_data_type=_type_to_name(type(json)),
            )

        try:
            return self.try_parse(json)
        except ParseError as exc:
            if log_replacer is None:
                raise exc
            # Don't do ``from exc`` as that might leak the value
            raise SimpleParseError(  # pylint: disable=raise-missing-from
                self,
                '<REDACTED>',
                extra={
                    'message': (
                        'we cannot show you as this data should contain'
                        ' confidential information, but the input value was of'
                        ' type {}'
                    ).format(type(json))
                }
            )


class Union(t.Generic[_T, _Y], Parser[t.Union[_T, _Y]]):
    """A parser that is a union between two parsers.
    """
    if _USE_SLOTS:
        __slots__ = ('_parser', )

    def use_readable_describe(
        self: 'Union[_T, _Y]', readable: bool
    ) -> 'Union[t.Union[_T, _Y], _Y]':
        res = super().use_readable_describe(readable)
        res._parser = res._parser.use_readable_describe(readable)  # pylint: disable=protected-access
        return res

    def __init__(self, first: Parser[_T], second: Parser[_Y]) -> None:
        super().__init__()
        self._parser: Parser[t.Union[_T, _Y]]
        if isinstance(first, Union):
            first = first._parser

        if isinstance(second, Union):
            second = second._parser

        if (
            isinstance(first, _SimpleValue) and
            isinstance(second, _SimpleValue)
        ):
            self._parser = _SimpleUnion(first.typ, second.typ)
        elif (
            isinstance(first, _SimpleUnion) and
            isinstance(second, _SimpleValue)
        ):
            self._parser = _SimpleUnion(*first.typs, second.typ)
        elif (
            isinstance(first, _SimpleValue) and
            isinstance(second, _SimpleUnion)
        ):
            self._parser = _SimpleUnion(first.typ, *second.typs)
        elif (
            isinstance(first, _SimpleUnion) and
            isinstance(second, _SimpleUnion)
        ):
            self._parser = _SimpleUnion(*first.typs, *second.typs)
        else:
            self._parser = _RichUnion(first, second)

    def describe(self) -> str:
        return self._parser.describe()

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        res = self._parser.to_open_api(schema)
        if 'anyOf' in res:
            res = {**res, 'anyOf': schema.expand_anyof(res['anyOf'])}
        return res

    def try_parse(self, value: object) -> t.Union[_T, _Y]:
        return self._parser.try_parse(value)


class Nullable(t.Generic[_T], Parser[t.Union[_T, None]]):
    """Make a parser that also allows ``None`` values.
    """
    if _USE_SLOTS:
        __slots__ = ('__parser', )

    def __init__(self, parser: Parser[_T]):
        super().__init__()
        self.__parser = parser

    def describe(self) -> str:
        return f'Union[None, {self.__parser.describe()}]'

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            **self.__parser.to_open_api(schema),
            'nullable': True,
        }

    def try_parse(self, value: object) -> t.Optional[_T]:
        if value is None:
            return value

        try:
            return self.__parser.try_parse(value)
        except SimpleParseError as err:
            raise SimpleParseError(self, value) from err


_SimpleValueT = t.TypeVar('_SimpleValueT', str, int, float, bool)

_TYPE_NAME_LOOKUP = {
    str: 'str',
    float: 'float',
    bool: 'bool',
    int: 'int',
    dict: 'mapping',
    list: 'list',
    type(None): 'null',
}


def _type_to_name(typ: t.Type) -> str:
    if typ in _TYPE_NAME_LOOKUP:
        return _TYPE_NAME_LOOKUP[typ]
    return str(typ)  # pragma: no cover


class _AnyValue(Parser[t.Any]):
    """A validator for an ``Any`` value. This will allow any value.
    """

    @staticmethod
    def describe() -> str:
        """The description for the any parser.
        """
        return 'Any'

    @staticmethod
    def _to_open_api(_: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {'type': 'object'}

    @staticmethod
    def try_parse(value: object) -> t.Any:
        """Parse the given value, this is basically a cast to ``Any``.
        """
        return value


AnyValue = _AnyValue()


class _SimpleValue(t.Generic[_SimpleValueT], Parser[_SimpleValueT]):
    if _USE_SLOTS:
        __slots__ = ('typ', )

    def describe(self) -> str:
        return _type_to_name(self.typ)

    def __init__(self, typ: t.Type[_SimpleValueT]) -> None:
        super().__init__()
        self.typ: Final[t.Type[_SimpleValueT]] = typ

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {'type': schema.simple_type_to_open_api_type(self.typ)}

    def try_parse(self, value: object) -> _SimpleValueT:
        # Local access is faster, so 'cache' the value here.
        typ = self.typ

        # Don't allow booleans as integers
        if isinstance(value, bool) and typ != bool:
            raise SimpleParseError(self, found=value)
        if isinstance(value, typ):
            return value
        # Also allow integers as floats
        if typ is float and isinstance(value, int):
            return float(value)  # type: ignore
        raise SimpleParseError(self, found=value)


class SimpleValue:
    """A collection of validators for primitive values.
    """
    int = _SimpleValue(int)
    float = _SimpleValue(float)
    str = _SimpleValue(str)
    bool = _SimpleValue(bool)


_SimpleUnionT = t.TypeVar(
    '_SimpleUnionT', bound=t.Union[str, int, float, bool]
)


class _SimpleUnion(t.Generic[_SimpleUnionT], Parser[_SimpleUnionT]):
    if _USE_SLOTS:
        __slots__ = ('typs', )

    def __init__(self, *typs: t.Type[_SimpleUnionT]) -> None:
        super().__init__()
        self.typs: Final[t.Tuple[t.Type[_SimpleUnionT], ...]] = typs

    def describe(self) -> str:
        return 'Union[{}]'.format(', '.join(map(_type_to_name, self.typs)))

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'anyOf': [
                schema.simple_type_to_open_api_type(t.cast(t.Type, typ))
                for typ in self.typs
            ]
        }

    def _raise(self, value: object) -> t.NoReturn:
        raise SimpleParseError(
            self,
            value,
            extra={
                'message':
                    '(which is of type {})'.format(_type_to_name(type(value)))
            }
        )

    def try_parse(self, value: object) -> _SimpleUnionT:
        # Don't allow booleans as integers
        if isinstance(value, bool) and bool not in self.typs:
            self._raise(value)
        if isinstance(value, self.typs):
            return value  # type: ignore
        # Also allow integers as floats
        if float in self.typs and isinstance(value, int):
            return float(value)  # type: ignore
        return self._raise(value)


class Lazy(t.Generic[_T], Parser[_T]):
    """A wrapping parser that allows you to construct circular parsers.

    The method ``make_parser`` will be executed when you first try to parse
    something. It will only be executed once.
    """
    if _USE_SLOTS:
        __slots__ = ('_parser', '_make_parser')

    def __init__(self, make_parser: t.Callable[[], Parser[_T]]):
        super().__init__()
        self._parser: t.Optional[Parser[_T]] = None
        self._make_parser = make_parser

    @property
    def parser(self) -> Parser[_T]:
        """The parser that this lazy uses.
        """
        if self._parser is None:
            self._parser = self._make_parser()
        return self._parser

    def describe(self) -> str:
        return self.parser.describe()

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return self.parser._to_open_api(schema)  # pylint: disable=protected-access

    def try_parse(self, value: object) -> _T:
        return self.parser.try_parse(value)


_ENUM = t.TypeVar('_ENUM', bound=enum.Enum)


class EnumValue(t.Generic[_ENUM], Parser[_ENUM]):
    """A parser for an existing enum.
    """
    if _USE_SLOTS:
        __slots__ = ('__typ', )

    def __init__(self, typ: t.Type[_ENUM]) -> None:
        super().__init__()
        self.__typ = typ

    def describe(self) -> str:
        return 'Enum[{}]'.format(
            ', '.join(repr(opt.name) for opt in self.__typ)
        )

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return schema.add_schema(self.__typ)

    def try_parse(self, value: object) -> _ENUM:
        if not isinstance(value, str):
            raise SimpleParseError(
                self,
                value,
                extra={
                    'message':
                        'which is of type {}, not string'.format(
                            _type_to_name(type(value))
                        )
                }
            )

        try:
            return self.__typ[value]
        except KeyError as err:
            raise SimpleParseError(self, value) from err


_BoolT = t.TypeVar('_BoolT', bound=bool)


class LiteralBoolean(t.Generic[_BoolT], Parser[_BoolT]):
    """A parser for a single literal boolean value.
    """
    if _USE_SLOTS:
        __slots__ = ('__value', )

    def __init__(self, value: _BoolT) -> None:
        super().__init__()
        self.__value = value

    def describe(self) -> str:
        return 'Literal[{}]'.format(self.__value)

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            **SimpleValue.bool.to_open_api(schema),
            'enum': [self.__value],
        }

    def try_parse(self, value: object) -> _BoolT:
        val = SimpleValue.bool.try_parse(value)
        if val != self.__value:
            raise SimpleParseError(self, value)
        return t.cast(_BoolT, val)


class StringEnum(t.Generic[_T], Parser[_T]):
    """A parser for an list of allowed literal string values.
    """
    if _USE_SLOTS:
        __slots__ = ('__opts', )

    def __init__(self, *opts: str) -> None:
        super().__init__()
        self.__opts = opts

    def describe(self) -> str:
        return 'Enum[{}]'.format(', '.join(map(repr, self.__opts)))

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'type': 'string',
            'enum': list(self.__opts),
        }

    def try_parse(self, value: object) -> _T:
        if not isinstance(value, str):
            raise SimpleParseError(
                self,
                value,
                extra={
                    'message':
                        'which is of type {}, not string'.format(
                            _type_to_name(type(value))
                        )
                }
            )

        if value not in self.__opts:
            raise SimpleParseError(self, value)
        return t.cast(_T, value)


class _RichUnion(t.Generic[_T, _Y], Parser[t.Union[_T, _Y]]):
    if _USE_SLOTS:
        __slots__ = ('__first', '__second')

    def __init__(self, first: Parser[_T], second: Parser[_Y]) -> None:
        super().__init__()
        self.__first = first
        self.__second = second

    def describe(self) -> str:
        if self._use_readable_describe:

            def _find_parts(cur: Parser) -> t.List[str]:
                if isinstance(cur, type(self)):
                    return [
                        *_find_parts(cur.__first),  # pylint: disable=protected-access
                        *_find_parts(cur.__second),  # pylint: disable=protected-access
                    ]
                else:
                    return [cur.describe()]

            indent = ' ' * 4
            return 'Union[\n{},\n]'.format(
                ',\n'.join(
                    textwrap.indent(part, indent)
                    for part in _find_parts(self)
                )
            )
        else:
            first = self.__first.describe()
            second = self.__second.describe()
            return 'Union[{}, {}]'.format(first, second)

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'anyOf': [
                self.__first.to_open_api(schema),
                self.__second.to_open_api(schema)
            ]
        }

    def try_parse(self, value: object) -> t.Union[_T, _Y]:
        try:
            return self.__first.try_parse(value)
        except ParseError as first_err:
            try:
                return self.__second.try_parse(value)
            except ParseError as second_err:
                raise MultipleParseErrors(  # pylint: disable=raise-missing-from
                    self,
                    value,
                    errors=[first_err, second_err]
                )


class TwoTuple(t.Generic[_T, _Y], Parser[t.Tuple[_T, _Y]]):
    """A parser for a tuple that consists exactly of two arguments.
    """

    if _USE_SLOTS:
        __slots__ = ('__left', '__right')

    def __init__(self, left: Parser[_T], right: Parser[_Y]) -> None:
        super().__init__()
        self.__left = left
        self.__right = right

    def describe(self) -> str:
        return 'Tuple[{}, {}]'.format(
            self.__left.describe(), self.__right.describe()
        )

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'type': 'array',
            'items': (self.__left | self.__right).to_open_api(schema),
            'minItems': 2,
            'maxItems': 2,
        }

    def try_parse(self, value: object) -> t.Tuple[_T, _Y]:
        if not isinstance(value, (tuple, list)):
            raise SimpleParseError(self, value)
        if len(value) != 2:
            raise SimpleParseError(self, value)

        return (
            self.__left.try_parse(value[0]),
            self.__right.try_parse(value[1]),
        )


class List(t.Generic[_T], Parser[t.Sequence[_T]]):
    """A parser for a list homogeneous values.
    """
    if _USE_SLOTS:
        __slots__ = ('__el_type', )

    def __init__(self, el_type: Parser[_T]):
        super().__init__()
        self.__el_type: Final = el_type

    def describe(self) -> str:
        return f'List[{self.__el_type.describe()}]'

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'type': 'array',
            'items': self.__el_type.to_open_api(schema),
        }

    def try_parse(self, value: object) -> t.List[_T]:
        if not isinstance(value, list):
            raise SimpleParseError(self, value)

        el_type = self.__el_type
        res = []
        errors = []

        for idx, item in enumerate(value):
            try:
                res.append(el_type.try_parse(item))
            except ParseError as e:
                errors.append(e.add_location(idx))

        if errors:
            raise MultipleParseErrors(self, value, errors)
        else:
            return res


_Key = t.TypeVar('_Key', bound=str)


class _Argument(t.Generic[_T, _Key]):
    if _USE_SLOTS:
        __slots__ = ('key', 'value', 'doc')

    def __init__(
        self,
        key: _Key,
        value: Parser[_T],
        doc: str,
    ) -> None:
        self.key: Final = key
        self.value: Final = value
        self.doc: Final = doc

    @abc.abstractmethod
    def describe(self) -> str:
        """Describe this argument.
        """
        ...

    @abc.abstractmethod
    def try_parse(self, value: t.Mapping[str, object]) -> t.Any:
        """Parse this argument.
        """
        ...

    def to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        """Convert this argument to open api.
        """
        # We save a copy in the common case here, as never call this method
        # when running the server, and adding a description copies the parser.
        return self.value.add_description(self.doc).to_open_api(schema)

    def _try_parse(self, value: t.Mapping[str, object]) -> cg_maybe.Maybe[_T]:
        if self.key not in value:
            return cg_maybe.Nothing

        found = value[self.key]
        try:
            return cg_maybe.Just(self.value.try_parse(found))
        except ParseError as err:
            raise err.add_location(self.key) from err


class RequiredArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that is required to be present.
    """

    def describe(self) -> str:
        return f'{self.key}: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> _T:
        """Try to parse this required argument from the given mapping.
        """
        res = self._try_parse(value)
        if isinstance(res, cg_maybe.Just):
            return res.value
        raise SimpleParseError(self.value,
                               cg_maybe.Nothing).add_location(self.key)


class DefaultArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that doesn't have to be present.
    """
    if _USE_SLOTS:
        __slots__ = ('__default', )

    def __init__(
        self,
        key: _Key,
        value: Parser[_T],
        doc: str,
        *,
        default: t.Callable[[], _T],
    ) -> None:
        super().__init__(key, value, doc)
        self.__default: Final = default

    def describe(self) -> str:
        return f'{self.key}?: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> _T:
        """Try to parse this required argument from the given mapping.
        """
        return self._try_parse(value).or_default_lazy(self.__default)

    def to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        """Convert this argument to open api.
        """
        return {
            **super().to_open_api(schema),
            'default': self.__default(),
        }


class OptionalArgument(t.Generic[_T, _Key], _Argument[_T, _Key]):
    """An argument in a ``FixedMapping`` that doesn't have to be present.
    """

    def describe(self) -> str:
        return f'{self.key}?: {self.value.describe()}'

    def try_parse(self, value: t.Mapping[str, object]) -> cg_maybe.Maybe[_T]:
        return self._try_parse(value)


class _DictGetter(t.Generic[_BaseDictT]):
    if _USE_SLOTS:
        __slots__ = ('__data', )

    def __init__(self, data: _BaseDictT) -> None:
        self.__data = data

    if not t.TYPE_CHECKING:

        def _unsafe_get_base_data(self) -> t.Dict[str, t.Any]:
            return copy.copy(self.__data)

    def __getattr__(self, key: str) -> object:
        try:
            return self.__data[key]
        except KeyError:
            return super().__getattribute__(key)


_BaseFixedMappingT = t.TypeVar('_BaseFixedMappingT', bound='_BaseFixedMapping')


class OnExtraAction(enum.Enum):
    """Action to perform if a :class:`_BaseFixedMapping` finds keys in the
    dictionary it is parsing that were not defined on the parser.
    """
    nothing = enum.auto()
    warning = enum.auto()
    error = enum.auto()


class _BaseFixedMapping(t.Generic[_BaseDictT]):
    def __init__(self, arguments: t.Sequence[_Argument]) -> None:
        super().__init__()
        self._arguments = arguments
        self.__schema: t.Optional[t.Type[_BaseDictT]] = None
        self._on_extra = OnExtraAction.nothing

    def set_on_extra(
        self: _BaseFixedMappingT, value: OnExtraAction
    ) -> _BaseFixedMappingT:
        """Enable warnings or errors when extra keys are found in the
        dictionaries to parse.
        """
        res = copy.copy(self)
        res._on_extra = value  # pylint: disable=protected-access
        return res

    @abc.abstractmethod
    def describe(self) -> str:
        """Describe this parser.
        """
        raise NotImplementedError

    def _describe(self, readable: bool) -> str:
        if readable and len(list(self._arguments)) > 1:
            args = [
                arg.describe()
                for arg in sorted(self._arguments, key=lambda a: a.key)
            ]
            indent = ' ' * 4
            content = '\n{},\n'.format(
                ',\n'.join(textwrap.indent(arg, indent) for arg in args)
            )
        else:
            args = [arg.describe() for arg in self._arguments]
            content = ', '.join(args)
        return 'Mapping[{}]'.format(content)

    def to_open_api_as_query(self, schema: 'OpenAPISchema'
                             ) -> t.Sequence[t.Mapping[str, t.Any]]:
        """Convert this mapping to a OpenAPI object as if it were used as a
        query string.
        """
        return [{
            'in': 'query',
            'name': arg.key,
            'schema': arg.to_open_api(schema),
            'description': schema.make_comment(arg.doc),
            'required': isinstance(arg, RequiredArgument),
        } for arg in self._arguments]

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        required = [
            arg.key for arg in self._arguments
            if isinstance(arg, RequiredArgument)
        ]
        res = {
            'type': 'object',
            'properties': {
                arg.key: arg.to_open_api(schema)
                for arg in self._arguments
            },
        }
        if required:
            res['required'] = required
        return res

    def _try_parse(
        self,
        value: object,
    ) -> _BaseDictT:
        if not isinstance(value, dict):
            raise SimpleParseError(self, value)

        result = {}
        errors = []
        for arg in self._arguments:
            try:
                result[arg.key] = arg.try_parse(value)
            except ParseError as exc:
                errors.append(exc)

        if errors:
            raise MultipleParseErrors(self, value, errors)

        extra_keys = value.keys() - result.keys()
        if extra_keys:
            if self._on_extra is OnExtraAction.warning:
                warnings.warn(
                    'Got extra keys: {}'.format(extra_keys),
                    stacklevel=3,
                )
            elif self._on_extra is OnExtraAction.error:
                extra_keys_str = ', '.join(extra_keys)
                raise SimpleParseError(
                    self,
                    value,
                    extra={
                        'extra_keys': extra_keys_str,
                        'message': f'Got extra keys: {extra_keys_str}',
                    }
                )

        return t.cast(_BaseDictT, result)


class BaseFixedMapping(
    t.Generic[_BaseDictT], _BaseFixedMapping[_BaseDictT], Parser[_BaseDictT]
):
    """A fixed mapping that returns a dictionary instead of a ``_DictGetter``.

    .. note::

        You should only create this using
        :meth:`.BaseFixedMapping.from_typeddict`, not using the normal
        constructor.
    """

    def __init__(
        self,
        *arguments: object,
        schema: t.Optional[t.Type[_BaseDictT]],
    ) -> None:
        super().__init__(t.cast(t.Any, arguments))
        self.__has_optional = any(
            isinstance(arg, OptionalArgument) for arg in self._arguments
        )
        self.__schema: t.Optional[t.Type[_BaseDictT]] = schema

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        if self.__schema is None:
            return super()._to_open_api(schema)
        else:
            return schema.add_schema(self.__schema)

    def describe(self) -> str:
        return self._describe(self._use_readable_describe)

    def try_parse(self, value: object) -> _BaseDictT:
        res = self._try_parse(value)
        # Optional values are parsed as Maybe, but callers think they will
        # simply get a dict with possibly missing items. So we convert that
        # here.
        if not self.__has_optional:
            return res

        for arg in self._arguments:
            if not isinstance(arg, OptionalArgument):
                continue

            key = arg.key
            if cg_maybe.Nothing.is_nothing_instance(res[key]):
                del res[key]
            else:
                assert isinstance(res[key], cg_maybe.Just)
                res[key] = res[key].value  # type: ignore

        return res

    @classmethod
    def __from_python_type(cls, typ, from_query):  # type: ignore
        # pylint: disable=too-many-return-statements,too-many-nested-blocks,too-many-branches
        # This function doesn't play nice at all with our plugins, so simply
        # skip checking it.
        origin = getattr(typ, '__origin__', None)

        def assert_not_query(cond: bool = False) -> None:
            if from_query and not cond:  # pragma: no cover
                raise AssertionError(
                    '{} is not supported as query param'.format(typ)
                )

        if is_typeddict(typ):
            args = []
            for key, subtyp in typ.__annotations__.items():
                if key in typ.__required_keys__:
                    args.append(
                        RequiredArgument(
                            key,
                            cls.__from_python_type(subtyp, from_query),
                            '',
                        )
                    )
                else:
                    args.append(
                        OptionalArgument(
                            key,
                            cls.__from_python_type(subtyp, from_query),
                            '',
                        )
                    )
            return BaseFixedMapping(*args, schema=typ)
        elif typ in (str, int, bool, float):
            if from_query:
                return getattr(QueryParam, typ.__name__)
            else:
                return getattr(SimpleValue, typ.__name__)
        elif origin in (list, collections.abc.Sequence):
            assert_not_query()

            return List(cls.__from_python_type(typ.__args__[0], from_query))
        elif origin == t.Union:
            has_none = type(None) in typ.__args__
            assert_not_query(not has_none)

            first_arg, *args = [a for a in typ.__args__ if a != type(None)]
            res = cls.__from_python_type(first_arg, from_query)
            for item in args:
                res = res | cls.__from_python_type(item, from_query)
            return Nullable(res) if has_none else res
        elif origin == Literal:
            assert all(isinstance(arg, str) for arg in typ.__args__)
            return StringEnum(*typ.__args__)
        elif isinstance(typ, enum.EnumMeta):
            return EnumValue(typ)
        elif origin == dict:
            assert_not_query()

            key, value = typ.__args__
            assert key == str, (
                'Only mappings with strings as keys are supported'
            )
            return LookupMapping(cls.__from_python_type(value, from_query))
        elif typ == uuid.UUID:
            return RichValue.UUID
        elif origin == tuple and len(typ.__args__) == 2:
            assert_not_query()

            return TwoTuple(
                cls.__from_python_type(typ.__args__[0], from_query),
                cls.__from_python_type(typ.__args__[1], from_query),
            )
        elif typ == DatetimeWithTimezone:
            return RichValue.DateTime
        elif typ == datetime.timedelta:
            assert_not_query()
            return RichValue.TimeDelta
        elif typ == t.Any:
            return AnyValue
        else:  # pragma: no cover
            raise AssertionError(
                f'Could not convert: {typ} (origin: {origin})'
            )

    @classmethod
    def from_function_parameters_list(
        cls,
        params: t.Iterable[inspect.Parameter],
        from_query: bool,
    ) -> 'BaseFixedMapping[t.Any]':
        """Create a BaseFixedMapping from a list of function parameters.
        """
        args = []
        for param in params:
            if param.default == inspect.Parameter.empty:
                args.append(
                    RequiredArgument(  # type: ignore
                        param.name,
                        cls.__from_python_type(param.annotation, from_query),
                        '',
                    )
                )
            else:
                default = param.default

                args.append(
                    DefaultArgument(  # type: ignore
                        param.name,
                        cls.__from_python_type(param.annotation, from_query),
                        '',
                        default=t.cast(
                            t.Callable,
                            lambda _default=default: _default,
                        ),
                    )
                )
        return BaseFixedMapping(  # type: ignore
            *args, schema=None
        )

    @classmethod
    def from_function(cls, fun: t.Callable) -> 'BaseFixedMapping[t.Any]':
        """Create a mapping from a function signature.
        """
        return cls.from_function_parameters_list(
            inspect.signature(fun).parameters.values(),
            from_query=False,
        )

    @classmethod
    def from_typeddict(cls, typeddict: t.Type) -> 'BaseFixedMapping[t.Any]':
        """Create a mapping from an existing typeddict.
        """
        return cls.__from_python_type(typeddict, False)


class FixedMapping(
    t.Generic[_BaseDictT], _BaseFixedMapping[_BaseDictT],
    Parser[_DictGetter[_BaseDictT]]
):
    """A mapping in which the keys are fixed and the values can have different
    types.
    """

    def __init__(self, *arguments: object) -> None:
        super().__init__(t.cast(t.Any, arguments))
        self.__tag: t.Optional[t.Tuple[str, object]] = None

    def describe(self) -> str:
        return self._describe(self._use_readable_describe)

    def add_tag(self, key: str, value: object) -> 'FixedMapping[_BaseDictT]':
        """Add a tag to this mapping.

        This tag will always be added to the final mapping after parsing.

        :param key: The key of the tag, should be a literal string.
        :param value: The value of the tag, should be a literal string.

        :returns: The existing mapping but mutated.
        """
        self.__tag = (key, value)
        return self

    def try_parse(
        self,
        value: object,
    ) -> _DictGetter[_BaseDictT]:
        result = self._try_parse(value)

        if self.__tag is not None:
            result[self.__tag[0]] = self.__tag[1]  # type: ignore[misc]
        return _DictGetter(result)

    def combine(
        self, other: 'FixedMapping[t.Any]'
    ) -> 'FixedMapping[_BaseDict]':
        """Combine this fixed mapping with another.

        :param other: The mapping to combine with. The arguments are not
            allowed to overlap

        :returns: A new fixed mapping with arguments of both given mappings.
        """
        args = [*self._arguments, *other._arguments]  # pylint: disable=protected-access
        return FixedMapping(*args)  # type: ignore


class LookupMapping(t.Generic[_T], Parser[t.Mapping[str, _T]]):
    """A parser that implements a lookup mapping.

    This a mapping where the keys are not fixed, so only the values are parsed
    (and are all parsed the same). Currently only string keys are allowed.
    """
    if _USE_SLOTS:
        __slots__ = ('__parser', )

    _PARSE_KEY = SimpleValue.str

    def __init__(self, parser: Parser[_T]) -> None:
        super().__init__()
        self.__parser = parser

    def describe(self) -> str:
        return 'Mapping[str: {}]'.format(self.__parser.describe())

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return {
            'type': 'object',
            'additionalProperties': self.__parser.to_open_api(schema),
        }

    def try_parse(self, value: object) -> t.Mapping[str, _T]:
        if not isinstance(value, dict):
            raise SimpleParseError(self, value)

        result = {}
        errors = []
        for key, val in value.items():
            try:
                parsed_key = self._PARSE_KEY.try_parse(key)
                result[parsed_key] = self.__parser.try_parse(val)
            except ParseError as exc:
                errors.append(exc.add_location(str(key)))
        if errors:
            raise MultipleParseErrors(self, value, errors)

        return result


class Transform(t.Generic[_T, _Y], Parser[_T], abc.ABC):
    """Make a parser that transforms the result from another parser.
    """
    if _USE_SLOTS:
        __slots__ = ('_parser', '__transform', '__transform_name')

    def __init__(
        self,
        parser: Parser[_Y],
        transform: t.Callable[[_Y], _T],
        transform_name: str,
    ):
        super().__init__()
        self._parser = parser
        self.__transform = transform
        self.__transform_name = transform_name

    def describe(self) -> str:
        return f'{self.__transform_name} as {self._parser.describe()}'

    def try_parse(self, value: object) -> _T:
        res = self._parser.try_parse(value)
        return self.__transform(res)


class Constraint(t.Generic[_T], Parser[_T]):
    """Parse a value, and further constrain the allowed values.
    """
    if _USE_SLOTS:
        __slots__ = ('_parser', )

    def __init__(self, parser: Parser[_T]):
        super().__init__()
        self._parser = parser

    @abc.abstractmethod
    def ok(self, value: _T) -> bool:
        """Check if the given value passes the constraint.
        """
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the constraint, used for error messages.
        """
        ...

    def describe(self) -> str:
        return f'{self._parser.describe()} {self.name}'

    def _to_open_api(self, schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
        return self._parser.to_open_api(schema)

    def try_parse(self, value: object) -> _T:
        res = self._parser.try_parse(value)
        if not self.ok(res):
            raise SimpleParseError(self, value)
        return res


@dataclasses.dataclass(frozen=True)
class _RegisterParseResult(t.Generic[_T, _Y]):
    if _USE_SLOTS:
        __slots__ = ('key', 'value')

    key: _T
    value: _Y


class RichValue:
    """A collection of various constraints and transformers that can be used as
    parsers.
    """

    class _UUID(Transform[uuid.UUID, str]):
        if _USE_SLOTS:
            __slots__ = ()

        def __init__(self) -> None:
            super().__init__(SimpleValue.str, self.__transform_to_uuid, 'UUID')

        def _to_open_api(self,
                         schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
            return {
                **self._parser.to_open_api(schema),
                'format': 'uuid',
            }

        def __transform_to_uuid(self, value: str) -> uuid.UUID:
            try:
                return uuid.UUID(value)
            except ValueError as exc:
                raise SimpleParseError(
                    self,
                    value,
                    extra={
                        'message': "which can't be parsed as a valid uuid",
                    },
                ) from exc

    UUID = _UUID()

    class _DateTime(Transform[DatetimeWithTimezone, str]):
        if _USE_SLOTS:
            __slots__ = ()

        def __init__(self) -> None:
            super().__init__(
                SimpleValue.str, self.__transform_to_datetime, 'DateTime'
            )

        def _to_open_api(self,
                         schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
            return {
                **self._parser.to_open_api(schema),
                'format': 'date-time',
            }

        def __transform_to_datetime(self, value: str) -> DatetimeWithTimezone:
            try:
                parsed = dateutil.parser.isoparse(value)
            except (ValueError, OverflowError) as exc:
                raise SimpleParseError(
                    self,
                    value,
                    extra={
                        'message': "which can't be parsed as a valid datetime",
                    },
                ) from exc
            else:
                return DatetimeWithTimezone.from_datetime(
                    parsed, default_tz=datetime.timezone.utc
                )

    DateTime = _DateTime()

    class _EmailList(Constraint[str]):
        def __init__(self) -> None:
            super().__init__(SimpleValue.str)

        def ok(self, to_parse: str) -> bool:
            addresses = email.utils.getaddresses([to_parse.strip()])
            return all(
                validate_email.validate_email(email) for _, email in addresses
            )

        @property
        def name(self) -> str:
            return 'as email list'

    EmailList = _EmailList()

    class ValueGte(Constraint[_GEComparableT], t.Generic[_GEComparableT]):
        """Parse a number that is gte than a given minimum.
        """
        if _USE_SLOTS:
            __slots__ = ('__minimum', )

        def __init__(
            self, parser: Parser[_GEComparableT], minimum: _GEComparableT
        ) -> None:
            super().__init__(parser)
            self.__minimum: Final = minimum

        @property
        def name(self) -> str:
            return f'larger than {self.__minimum}'

        def ok(self, value: _GEComparableT) -> bool:
            return value >= self.__minimum

        def _to_open_api(self,
                         schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
            return {
                **self._parser.to_open_api(schema),
                'minimum': self.__minimum,
            }

    class _Password(_SimpleValue[str]):
        if _USE_SLOTS:
            __slots__ = ()

        def __init__(self) -> None:
            super().__init__(str)

        def describe(self) -> str:
            return f'password as {super().describe()}'

        def _to_open_api(self,
                         schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
            return {
                **super()._to_open_api(schema),
                'format': 'password',
            }

        def try_parse(self, value: object) -> str:
            try:
                return super().try_parse(value)
            except ParseError:
                # Don't raise from as that might leak the value
                raise SimpleParseError(self, found='REDACTED')  # pylint: disable=raise-missing-from

    Password = _Password()

    class _TimeDelta(Transform[datetime.timedelta, t.Union[str, float]]):
        # The regex below are copied from Pydantic
        _ISO8601_DURATION_RE = re.compile(
            r'^(?P<sign>[-+]?)'
            r'P'
            r'(?:(?P<days>\d+(.\d+)?)D)?'
            r'(?:T'
            r'(?:(?P<hours>\d+(.\d+)?)H)?'
            r'(?:(?P<minutes>\d+(.\d+)?)M)?'
            r'(?:(?P<seconds>\d+(.\d+)?)S)?'
            r')?'
            r'$'
        )

        def __init__(self) -> None:
            super().__init__(
                SimpleValue.str | SimpleValue.float,
                self.__to_timedelta,
                'TimeDelta',
            )

        def _to_open_api(self,
                         schema: 'OpenAPISchema') -> t.Mapping[str, t.Any]:
            return {
                'anyOf': [
                    SimpleValue.int.to_open_api(schema),
                    {
                        **SimpleValue.str.to_open_api(schema),
                        'format': 'time-delta',
                    },
                ],
            }

        def __to_timedelta(
            self, value: t.Union[str, float]
        ) -> datetime.timedelta:
            if isinstance(value, float):
                return datetime.timedelta(seconds=value)
            return self.__str_to_timedelta(value)

        def __str_to_timedelta(self, value: str) -> datetime.timedelta:
            match = self._ISO8601_DURATION_RE.match(value)
            if match is None:
                raise SimpleParseError(self, value)

            groupdict: t.Mapping[str, t.Optional[str]] = match.groupdict()
            groups = {k: v for k, v in groupdict.items() if v is not None}
            sign = -1 if groups.get('sign', None) == '-' else 1

            return sign * datetime.timedelta(
                days=float(groups.get('days', 0)),
                hours=float(groups.get('hours', 0)),
                minutes=float(groups.get('minutes', 0)),
                seconds=float(groups.get('seconds', 0)),
                microseconds=float(groups.get('microseconds', 0)),
            )

    TimeDelta = _TimeDelta()


class _BoolQueryParam(Transform[bool, str]):
    _TRUTHY_VALUES = ('', '1', 'true', 'yes', 't')
    _FALSY_VALUES = ('0', 'false', 'no', 'nil')
    _EXTRA_MSG = (
        'allowed truthy values are {t}; allowed falsy values are: {f}'
    ).format(
        t=readable_join(['"{}"'.format(v) for v in _TRUTHY_VALUES]),
        f=readable_join(['"{}"'.format(v) for v in _FALSY_VALUES]),
    )

    def __init__(self) -> None:
        super().__init__(
            SimpleValue.str,
            self.__to_bool,
            'BoolQueryParam',
        )

    def __to_bool(self, value: str) -> bool:
        lowered = value.lower()
        if lowered in self._TRUTHY_VALUES:
            return True
        elif lowered in self._FALSY_VALUES:
            return False

        raise SimpleParseError(self, value, extra={'message': self._EXTRA_MSG})

    def _to_open_api(self, schema: t.Any) -> t.Mapping[str, t.Any]:
        return SimpleValue.bool.to_open_api(schema)


class _IntQueryParam(Transform[int, str]):
    def __init__(self) -> None:
        super().__init__(
            SimpleValue.str,
            self.__to_int,
            'IntQueryParam',
        )

    def __to_int(self, value: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise SimpleParseError(self, value) from exc

    def _to_open_api(self, schema: t.Any) -> t.Mapping[str, t.Any]:
        return SimpleValue.int.to_open_api(schema)


class QueryParam:
    """Parsers to use for query parameters.
    """
    str = SimpleValue.str
    int = _IntQueryParam()
    bool = _BoolQueryParam()


class MultipartUpload(t.Generic[_T]):
    """This class helps you parse JSON and files from the same request.
    """
    if _USE_SLOTS:
        __slots__ = ('__parser', '__file_key')

    def __init__(
        self,
        parser: Parser[_T],
        file_key: str,
    ) -> None:
        self.__parser = parser
        self.__file_key = file_key

    def from_flask(self, *, log_replacer: LogReplacer = None
                   ) -> t.Tuple[_T, t.Sequence['FileStorage']]:
        """Parse a multipart request from the current flask request.

        :param log_replacer: If passed this function should remove any
            sensitive data from the logs.

        :returns: A tuple, where the first item is the parsed JSON (according
                  to the given parser), and the second argument is a list of
                  the parsed files.
        """
        if _GENERATE_SCHEMA is not None:
            json_schema = self.__parser.to_open_api(_GENERATE_SCHEMA)
            file_type = {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'format': 'binary',
                },
            }
            raise _Schema(
                typ='multipart/form-data',
                schema={
                    'type': 'object',
                    'properties': {
                        'json': json_schema,
                        self.__file_key: file_type,
                    },
                    'required': ['json'],
                },
            )

        body = None
        if 'json' in flask.request.files:
            body = _json.load(flask.request.files['json'])
        if not body:
            body = flask.request.get_json()

        result = self.__parser.try_parse_and_log(
            body, log_replacer=log_replacer
        )

        if not flask.request.files:
            files = []
        else:
            files = flask.request.files.getlist(self.__file_key)
            for key, f in flask.request.files.items():
                if key != self.__file_key and key.startswith(self.__file_key):
                    files.append(f)

        files = [f for f in files if f.filename]
        return result, files


class ExactMultipartUpload(t.Generic[_T]):
    """This class helps you parse JSON and files from the same request.
    """
    if _USE_SLOTS:
        __slots__ = ('__parser', '__file_keys')

    def __init__(
        self,
        parser: Parser[_T],
        file_keys: t.Sequence[str],
    ) -> None:
        self.__parser = parser
        self.__file_keys = file_keys

    def describe(self) -> str:
        return 'Request[{{"json": {json} as file, {other}}}]'.format(
            json=self.__parser.describe(),
            other=', '.join(f'"{key}": File' for key in self.__file_keys),
        )

    def from_flask(self, *, log_replacer: LogReplacer = None
                   ) -> t.Tuple[_T, t.Mapping[str, 'FileStorage']]:
        """Parse a multipart request from the current flask request.

        :param log_replacer: If passed this function should remove any
            sensitive data from the logs.

        :returns: A tuple, where the first item is the parsed JSON (according
                  to the given parser), and the second argument is a list of
                  the parsed files.
        """
        if _GENERATE_SCHEMA is not None:
            json_schema = self.__parser.to_open_api(_GENERATE_SCHEMA)
            file_type: t.Mapping[str, t.Any] = {
                'type': 'string',
                'format': 'binary',
            }
            raise _Schema(
                typ='multipart/form-data',
                schema={
                    'type': 'object',
                    'properties': {
                        'json': json_schema,
                        **{key: file_type
                           for key in self.__file_keys},
                    },
                    'required': ['json'],
                },
            )

        body = None
        if 'json' in flask.request.files:
            body = _json.load(flask.request.files['json'])
        else:
            body = cg_maybe.Nothing

        result = self.__parser.try_parse_and_log(
            body, log_replacer=log_replacer
        )

        files = flask.request.files
        if not files:
            raise SimpleParseError(self, cg_maybe.Nothing)

        file_map = {
            key: files[key]
            for key in self.__file_keys if key in files and files[key].filename
        }
        if any(key not in file_map for key in self.__file_keys):
            raise SimpleParseError(
                self,
                {
                    key: 'File'
                    for key, value in files.items() if value.filename
                },
            )

        return result, file_map
