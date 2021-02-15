"""Data-Model Messages."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from functools import wraps
from importlib import import_module
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from pydantic import BaseModel, Field, validator
from pydantic.fields import SHAPE_LIST, SHAPE_SINGLETON, ModelField
from pydantic.schema import default_ref_template
from pydantic.types import ConstrainedFloat, ConstrainedInt, ConstrainedStr
from pydantic.typing import display_as_type

from .model import CoreHeader, CoreModel, CoreModelMeta
from .utils import format_code, gather

# legacy type names
from .types import (  # isort:skip
    Float32_ as Float,
    Float64_ as Double,
    Int8_ as Int8,
    Int16_ as Int16,
    Int32_ as Int32,
    Int64_ as Int64,
    UInt8_ as UInt8,
    UInt16_ as UInt16,
    UInt32_ as UInt32,
    UInt64_ as UInt64,
)

CONSTRAINT_NAMES = [
    "gt",
    "lt",
    "ge",
    "le",
    "min_length",
    "max_length",
    "min_items",
    "max_items",
]


def format_annotation(x: ModelField, imports: Mapping[str, Set[str]]) -> str:
    """Format annotation."""

    kwargs: Dict[str, Any] = {}

    if x.default_factory is not None:
        kwargs["default_factory"] = x.default_factory
    elif x.default is not None:
        kwargs["default"] = x.default
    else:
        kwargs["default"] = ... if x.required else None

    if x.field_info.description:
        kwargs["description"] = x.field_info.description

    if issubclass(x.type_, Enum):
        annotation = x.type_.__name__
    elif (
        issubclass(x.type_, (ConstrainedFloat, ConstrainedInt, ConstrainedStr))
        and x.type_.__module__ != "kelvin.icd.types"
    ):
        kwargs.update(
            {
                k: v
                for k, v in ((name, getattr(x.type_, name, None)) for name in CONSTRAINT_NAMES)
                if v is not None
            }
        )
        annotation = display_as_type(x.type_.mro()[-2])
    else:
        annotation = display_as_type(x.type_)

    if x.shape == SHAPE_LIST:
        annotation = f"List[{annotation}]"
    if x.allow_none:
        annotation = f"Optional[{annotation}]"

    def repr_val(x: Any) -> str:
        if x is ...:
            return "..."
        if callable(x):
            return x.__name__
        return repr(x)

    field_args: List[str] = []
    if "default" in kwargs:
        field_args += [repr_val(kwargs.pop("default"))]
    field_args += (f"{k}={repr_val(v)}" for k, v in kwargs.items())

    result = f"{annotation} = Field({', '.join(field_args)})"

    # substitute imports
    for module, names in imports.items():
        for name in names:
            result = re.sub(rf"\b{module}.{name}\b", name, result)

    return result


class Header(CoreHeader):
    """Header Interface."""

    @validator("name", pre=True, always=True)
    def validate_name(cls, value: Optional[str]) -> str:
        """Validate name."""

        return value if value is not None else ""

    type: str = Field(..., title="Message Type", description="Message type.")
    # version: Optional[str] = Field(None, title="Message Type Version")
    name: str = Field(..., title="Message Name", description="Message name.")
    source: Optional[str] = Field(None, title="Message Source", description="Message source.")


class MessageMeta(CoreModelMeta):
    """Message metaclass."""

    MESSAGE_TYPES: Dict[str, Type[Message]] = {}

    def __new__(
        metacls: Type[MessageMeta], name: str, bases: Tuple[Type, ...], __dict__: Dict[str, Any]
    ) -> MessageMeta:
        """Create Message class."""

        cls = cast(MessageMeta, super().__new__(metacls, name, bases, __dict__))

        _type = __dict__.get("_TYPE")

        if isinstance(_type, str):
            metacls.MESSAGE_TYPES[_type] = cast(Type[Message], cls)

        return cls


T = TypeVar("T", bound="Message")


class Message(CoreModel[Header], metaclass=MessageMeta):
    """Message Interface."""

    _TYPE: str

    __slots__ = "_TYPE"

    class Config(CoreModel.Config):
        """Pydantic config."""

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model_class: Type[CoreModel]) -> None:  # type: ignore
            """Make schema additions."""

            definitions = schema.setdefault("definitions", {})
            properties = schema.get("properties", {})

            for name, field in model_class.__fields__.items():
                T = field.type_
                if (
                    not issubclass(T, (ConstrainedFloat, ConstrainedInt))
                    or T.__module__ != "kelvin.icd.types"
                ):
                    continue

                type_name = T.__name__[:-1]

                field_schema = properties[name]
                if field.shape == SHAPE_LIST:
                    field_schema = field_schema["items"]
                field_schema.pop("type")
                field_schema.pop("minimum", None)
                field_schema.pop("maximum", None)
                field_schema["$ref"] = default_ref_template.format(model=type_name)

                if type_name in definitions:
                    continue

                definitions[type_name] = {
                    "title": type_name,
                    "description": T.__doc__,
                    "type": "integer" if issubclass(T, int) else "number",
                    "minimum": T.ge,
                    "maximum": T.le,
                }

    def __new__(cls, *args: Any, **kwargs: Any) -> Message:
        """Initialise message."""

        if isinstance(cls._TYPE, str):
            T = cls
        else:
            try:
                _type = kwargs["_"]["type"]
            except KeyError:
                raise ValueError("Missing message type")

            T = cls.get_type(_type)

        obj = super().__new__(T)

        # only init if args provided
        if args or kwargs:
            obj.__init__(*args, **kwargs)

        return obj

    def __init__(
        self,
        _name: Optional[str] = None,
        *,
        _: Optional[Union[Header, Mapping[str, Any]]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise message."""

        _type: str = self._TYPE

        if _ is not None:
            if isinstance(_, Header):
                pass
            elif isinstance(_, Mapping):
                _ = Header.parse_obj({"type": _type, "name": _name, **_})
            else:
                raise ValueError(f"Invalid header type: {type(_).__name__!r}")

            _ = cast(Header, _)
            if _.type != _type:
                raise ValueError(f"Header type mismatch {_.type!r} != {_type!r}")
            if _name is not None and _.name != _name:
                raise ValueError(f"Header name mismatch {_.name!r} != {_name!r}")
        else:
            _ = Header(name=_name, type=_type)

        super().__init__(_, **kwargs)

    @classmethod
    def to_code(cls) -> str:
        """Generate code."""

        result: List[str] = [f'"""{cls.__name__} Message."""', ""]
        extra: List[str] = []

        imports: Dict[str, Set[str]] = defaultdict(set)
        imports["__future__"] |= {"annotations"}
        imports["typing"] |= {*[]}
        imports["pydantic"] |= {"Field"}
        imports["kelvin.icd.message"] |= {"Message"}

        for name, field in cls.__fields__.items():
            if field.shape == SHAPE_LIST:
                imports["typing"] |= {"List"}
            elif field.shape != SHAPE_SINGLETON:
                raise TypeError(f"Field {name!r} has invalid shape: {field.shape}")
            if field.allow_none:
                imports["typing"] |= {"Optional"}

            if issubclass(field.type_, Message) or field.type_.__module__ == "kelvin.icd.types":
                imports[field.type_.__module__] |= {field.type_.__name__}
            elif issubclass(field.type_, Enum):
                enum_base = field.type_.mro()[1]
                imports[enum_base.__module__] |= {enum_base.__name__}
                extra += [
                    f"class {field.type_.__name__}({enum_base.__name__}):",
                    f'    """{field.type_.__name__} enumeration."""',
                    *(f"    {x.name} = {x.value!r}" for x in field.type_),
                ]

        result += [f"from {k} import {', '.join(sorted(v))}" for k, v in imports.items() if k and v]
        result += [f"import {x}" for k, v in imports.items() if not k for x in sorted(v)]

        result += [
            *extra,
            f'''
class {cls.__name__}(Message):
    """{cls.__doc__ if cls.__doc__ else f"{cls.__name__} Message."}"""

    _TYPE = "{cls._TYPE}"
''',
        ]

        result += [
            f"    {name}: {format_annotation(field, imports)}"
            for name, field in cls.__fields__.items()
        ]

        return format_code("\n".join(result))

    @classmethod
    def get_type(cls, _type: str) -> Type[Message]:
        """Get message type by name."""

        try:
            return cls.MESSAGE_TYPES[_type]
        except KeyError:
            try:
                import_module(f"kelvin.message.{_type}")
            except ImportError:
                raise ValueError(f"Unknown message type: {_type}")
            try:
                return cls.MESSAGE_TYPES[_type]
            except KeyError:  # pragma: no cover
                raise ValueError(f"Unknown message type: {_type}")

    @classmethod
    def make_message(
        cls: Type[T],
        _type: str,
        _name: Optional[str] = None,
        _time_of_validity: Optional[Union[int, float]] = None,
        _source: Optional[str] = None,
        **kwargs: Any,
    ) -> T:
        """
        Create a message object.

        Parameters
        ----------
        _type : str, optional
            Message type (e.g. ``raw.float32``, ``kelvin.beam_pump``)
        _name : str, optional
            Message name
        _time_of_validity : int, optional
            Time of validity in nano-seconds
        _source : str, optional
            Message source
        **kwargs :
            Additional properties for message (e.g. ``value`` for raw types)

        """

        _ = {
            "type": _type,
            "name": _name,
            "time_of_validity": _time_of_validity,
            "source": _source,
        }

        return cls(_=_, **kwargs)

    @wraps(BaseModel.schema)
    @classmethod
    def schema(
        cls, by_alias: bool = True, ref_template: str = default_ref_template
    ) -> Dict[str, Any]:
        """Generate schema dictionary."""

        result = deepcopy(super().schema(by_alias=by_alias, ref_template=ref_template))
        result["definitions"] = gather(result, "definitions")

        return result

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        """Get validators."""

        # preserve overridden class-method from pydantic
        yield super().validate

    def validate(self) -> bool:  # type: ignore
        """Check the validity of the message."""

        fields_set = self.__fields_set__

        return all(
            name in fields_set for name, field in self.__fields__.items() if not field.allow_none
        )

    # legacy interface
    def to_json(self) -> str:
        """Convert to JSON."""

        return json.dumps(self.dict(exclude_unset=True))

    @classmethod
    def from_json(cls: Type[T], x: str) -> T:
        """Load from JSON."""

        return cls.parse_raw(x)

    def clone(self: T) -> T:
        """Clone message."""

        return self.copy(deep=True)


make_message = Message.make_message
