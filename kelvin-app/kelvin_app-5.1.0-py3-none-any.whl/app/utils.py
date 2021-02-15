"""Utility functions."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from functools import reduce, wraps
from importlib import import_module
from operator import itemgetter
from pathlib import Path
from typing import _GenericAlias  # type: ignore
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    cast,
    get_type_hints,
)
from warnings import warn

from pydantic import BaseModel

from kelvin.icd import Message

try:
    from importlib.metadata import Distribution, distributions  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import Distribution, distributions  # type: ignore

DurationType = Union[int, float, timedelta, Mapping[str, Union[float, int]]]
TimeType = Union[DurationType, datetime]

REPLACEMENTS = [
    (".", r"\."),
    ("*", r"([^.]+)"),
    (r"\.#", r"(\.[^.]+)*"),
    (r"#\.", r"([^.]+\.)*"),
    (r"#", r"([^.]+)(\.[^.]+)*"),
]


def topic_pattern(pattern: str) -> Pattern:
    """Create topic regular expression."""

    # just match the tail
    if pattern.isidentifier():
        pattern = f"#.{re.escape(pattern)}"

    pattern = reduce(lambda x, y: x.replace(*y), REPLACEMENTS, pattern)

    return re.compile(f"^{pattern}$")


def merge(
    x: MutableMapping[str, Any],
    *args: Optional[Mapping[str, Any]],
    ignore: Sequence[Tuple[str, ...]] = (),
) -> MutableMapping[str, Any]:
    """Merge dictionaries."""

    for arg in args:
        if arg is None:
            continue
        for k, v in arg.items():
            target = x.get(k, ...)
            if (
                target is ...
                or not (isinstance(target, Mapping) and isinstance(v, dict))
                or (k,) in ignore
            ):
                x[k] = v
            else:
                x[k] = merge({}, target, v, ignore=[x[1:] for x in ignore if x and x[0] == k])

    return x


def flatten(x: Mapping[str, Any]) -> Iterator[Tuple[str, Any]]:
    """Flatten nested mappings."""

    return (
        (k if not l else f"{k}.{l}", w)
        for k, v in x.items()
        for l, w in (flatten(v) if isinstance(v, Mapping) else [("", v)])
    )


def inflate(items: Iterable[Tuple[str, Any]], separator: str = ".") -> Dict[str, Any]:
    """Inflate flattened keys via separator into nested dictionary."""

    result: Dict[str, Any] = {}

    for key, value in sorted(items, key=itemgetter(0)):
        if separator not in key:
            head, tail = [], key
            root = result
        else:
            *head, tail = key.split(separator)
            root = reduce(lambda x, y: x.setdefault(y, {}), head, result)

        try:
            root[tail] = value
        except TypeError:
            raise ValueError(
                f"Unable to extend leaf value at {separator.join(head)!r} ({root!r}) to {key!r} ({value!r})"
            )

    return result


def gather(x: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Gather keys from a nested structure."""

    values = x.pop(key, {})

    for v in [*values.values()]:
        values.update(gather(v, key))

    return values


def build_mapping(
    items: Iterable[Mapping[str, Any]], key: str = "name"
) -> Dict[str, Dict[str, Any]]:
    """Build mapping by a designated field from a list of mappings."""

    return {cast(str, item[key]): {**item} for item in items}


def build_messages(setup: Mapping[str, Any]) -> Dict[str, Message]:
    """Build messages."""

    return {
        name: Message(
            _={"name": name, "type": data["data_model"]},
            **inflate((item["name"], item["value"]) for item in data.get("values", [])),
        )
        for name, data in setup.items()
    }


def get_io(config: Mapping[str, Any]) -> Tuple[Dict[str, Dict[str, Any]], ...]:
    """Get IO from app configuration."""

    return (
        *(
            build_mapping(config.get(section, []))
            for section in ["inputs", "outputs", "configuration", "parameters"]
        ),
    )


def duration(x: Optional[DurationType]) -> Optional[float]:
    """Get the duration in seconds."""

    if isinstance(x, float) or x is None:
        return x

    if isinstance(x, int):
        return float(x)

    if isinstance(x, Mapping):
        x = timedelta(**x)

    if isinstance(x, timedelta):
        return x.total_seconds()

    raise TypeError(f"'{type(x).__name__}' has no duration")


def resolve_period(start: Optional[TimeType], end: Optional[TimeType]) -> Tuple[datetime, datetime]:
    """Resolve start and end for a period."""

    def fix(x: Optional[TimeType]) -> Union[datetime, timedelta]:
        if x is None:
            return timedelta(0)
        if isinstance(x, (datetime, timedelta)):
            return x
        if isinstance(x, Mapping):
            return timedelta(**x)
        return datetime.fromtimestamp(x, tz=timezone.utc)

    start, end = fix(start), fix(end)

    if isinstance(start, timedelta):
        if isinstance(end, timedelta):
            raise ValueError("Start or end must be absolute")
        start = end - start
    elif isinstance(end, timedelta):
        end = start + end

    return start, end


def get_distribution(name: str) -> Optional[Distribution]:
    """Get distribution from module name."""

    module = import_module(name)

    try:
        filename = module.__file__
    except AttributeError:
        return None

    if filename is None:
        return None

    path = Path(filename)

    for dist in distributions():
        if dist.files is None:
            continue  # pragma: no cover

        try:
            relative = path.relative_to(dist.locate_file(""))
        except ValueError:  # pragma: no cover
            continue

        if relative in dist.files:
            return dist

    return None


def deep_copy(x: Any) -> Any:
    """Deep copy for mutable containers."""

    if isinstance(x, MutableMapping):
        return {k: deep_copy(v) for k, v in x.items()}

    if isinstance(x, MutableSequence):
        return [deep_copy(v) for v in x]

    if isinstance(x, MutableSet):
        return {deep_copy(v) for v in x}

    return x


def field_info(T: Any) -> Dict[str, Any]:  # pragma: no cover
    """Derive field info from type."""

    return {
        name: S.__origin__
        if isinstance(S, _GenericAlias)
        else field_info(S)
        if isinstance(S, BaseModel)
        else S
        for name, S in get_type_hints(T).items()
        if not name.startswith("_")
    }


T = TypeVar("T")


def deprecated(message: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Deprecation decorator."""

    def outer(f: Callable[..., T]) -> Callable[..., T]:
        message_ = f"{f.__name__} is deprecated" if message is None else message

        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            warn(message_, DeprecationWarning)
            return f(*args, **kwargs)

        return wrapper

    return outer
