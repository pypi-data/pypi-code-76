"""Application State."""

from __future__ import annotations

from collections import ChainMap
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Sequence, Set, Union

import structlog

from kelvin.icd import Message

from ..config import Topic
from ..data import DataBuffer
from ..mapping_proxy import MappingProxy
from ..utils import flatten

if TYPE_CHECKING:
    from IPython.lib.pretty import PrettyPrinter
    from pandas import DataFrame

logger = structlog.get_logger(__name__)


class State:
    """Application State."""

    __slots__ = ("_topics", "_data", "_last_message", "_updates")

    def __init__(
        self, topics: Optional[Sequence[Topic]] = None, messages: Optional[Sequence[Message]] = None
    ) -> None:
        """Initialise application state."""

        self._topics = topics
        self._data = MappingProxy({})
        self._updates = MappingProxy({})
        self._last_message: Dict[str, Message] = {}

        if messages is not None:
            self(messages)

    def __getitem__(self, name: Union[str, Iterable[str]]) -> Any:
        """Get item."""

        if isinstance(name, Iterable) and not isinstance(name, str):
            return {x: self._data[x] for x in name}

        return self._data[name]

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_") or name in super().__dir__():
            return super().__getattribute__(name)

        return self._data[name]

    @property
    def updates(self) -> Dict[str, int]:
        """Updated keys."""

        updates = {k: v for k, v in flatten(self._updates)}

        self._updates.clear()

        return updates

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *self._data]

    def __call__(self, messages: Sequence[Message]) -> None:
        """Update state."""

        if self._topics is None:
            for message in messages:
                name = message._.name
                if message == self._last_message.get(name):
                    continue
                self._data[name] = self._last_message[name] = message
                try:
                    self._updates[name] += 1
                except KeyError:
                    self._updates[name] = 1
            return

        for message in messages:
            targets: Set[str] = {*[]}

            name = message._.name
            if message == self._last_message.get(name):
                continue
            self._last_message[name] = message

            final = False

            for topic in self._topics:
                if final:
                    break
                if not topic.match(f"{message._.type}.{name}"):
                    continue

                target = topic.target
                final = topic.final

                if target is None:
                    # stop here - return any earlier matches
                    break

                if "{" in target:
                    try:
                        target = target.format_map(ChainMap(message, message._))
                    except Exception:  # pragma: no cover
                        logger.exception(
                            "Invalid topic target", pattern=topic.pattern, target=target
                        )
                        continue

                if target in targets:
                    continue

                targets |= {target}

                # store single value
                if topic.init is None:
                    self._data[target] = message
                else:
                    data = self._data.get(target)
                    if data is not None:
                        data += [message]
                    else:
                        self._data[target] = topic.init([message])  # type: ignore

                try:
                    self._updates[target] += 1
                except KeyError:
                    self._updates[target] = 1

    def __str__(self) -> str:
        """Return str(self)."""

        name = type(self).__name__

        return f"<{name}>({', '.join(f'{k}={v!r}' for k, v in self._data.items())})"

    def __repr__(self) -> str:
        """Return repr(self)."""

        return str(self)

    def _repr_pretty_(self, p: PrettyPrinter, cycle: bool) -> None:
        """Pretty representation."""

        name = type(self).__name__

        with p.group(4, f"<{name}>(", ")"):
            if cycle:  # pragma: no cover
                p.text("...")
                return

            for i, (k, v) in enumerate(self._data.items()):
                if i:
                    p.text(",")
                    p.breakable()
                else:
                    p.breakable("")
                p.text(f"{k}=")
                p.pretty(v)

    @property
    def frame(self) -> DataFrame:
        """Get a dataframe."""

        from pandas import DataFrame, DatetimeIndex

        data = {
            (*k.split("."),) if "." in k else k: v.series()
            for k, v in self._data.flatten()
            if isinstance(v, DataBuffer)
        }

        if not data:
            return DataFrame(index=DatetimeIndex([], name="time", tz="UTC"))

        return DataFrame(data)
