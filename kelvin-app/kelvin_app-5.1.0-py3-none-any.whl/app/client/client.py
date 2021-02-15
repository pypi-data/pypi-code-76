"""Kelvin Core Client."""

from __future__ import annotations

from typing import Any, Mapping, Optional, Union, cast, overload

from .config import CoreClientConfig
from .connection import AsyncConnection, SyncConnection

try:
    from typing import Literal  # type: ignore
except ImportError:  # pragma: no cover
    from typing_extensions import Literal  # type: ignore


class CoreClient:
    """Kelvin Core Client."""

    def __init__(
        self, config: Union[Optional[CoreClientConfig], Mapping[str, Any]] = None, **kwargs: Any
    ) -> None:
        """Initialise Kelvin Core Client."""

        if config is None:
            config = CoreClientConfig(**kwargs)
        elif isinstance(config, CoreClientConfig):
            config = config.copy(deep=True)
            for name, value in kwargs.items():
                setattr(config, name, value)
        elif isinstance(config, Mapping):
            config = CoreClientConfig.parse_obj({**config, **kwargs})
        else:
            raise TypeError(f"Invalid config type {type(config).__name__!r}")

        self._config = cast(CoreClientConfig, config)

    @property
    def config(self) -> CoreClientConfig:
        """Core client configuration."""

        return self._config

    @overload
    def connect(self, sync: Literal[True], **kwargs: Any) -> SyncConnection:  # type: ignore
        """Connect client to server (sync)."""

    @overload
    def connect(self, sync: Literal[False], **kwargs: Any) -> AsyncConnection:  # type: ignore
        """Connect client to server (async)."""

    @overload
    def connect(
        self, sync: Literal[None] = None, **kwargs: Any
    ) -> Union[AsyncConnection, SyncConnection]:
        """Connect client to server."""

    def connect(
        self, sync: Optional[bool] = None, connect: bool = False, **kwargs: Any
    ) -> Union[AsyncConnection, SyncConnection]:
        """Connect client to server."""

        config = self.config

        if sync is None:
            sync = config.sync

        cls = SyncConnection if sync else AsyncConnection
        connection = cls(config, **kwargs)

        if connect:
            connection.connect()

        return connection
