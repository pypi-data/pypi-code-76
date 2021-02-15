"""Kelvin SDK Injector."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import cycle, groupby
from math import isfinite
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping, Optional, Sequence, Tuple, Union

import pandas
from numpy import generic
from pandas import DataFrame, MultiIndex

from kelvin.app import PollerApplication
from kelvin.app.utils import inflate
from kelvin.icd.message import Message

from .config import DataType, InjectorConfig


class InjectorApp(PollerApplication):
    """Kelvin SDK Injector Application."""

    _DATA_TYPE_READER: Mapping[str, DataType] = {
        ".txt": DataType.TABLE,
    }
    _generator: Optional[Iterator[Tuple[datetime, Mapping[str, Any]]]] = None

    @classmethod
    def _get_loader(
        cls, filename: Path, data_type: Optional[DataType] = None
    ) -> Callable[..., DataFrame]:
        """Get dataframe loader."""

        if data_type is not None:
            suffix = data_type.value
        else:
            # infer data type
            extension = filename.suffix
            if not extension:
                raise ValueError(f"No file extension on {str(filename)!r}")

            try:
                suffix = cls._DATA_TYPE_READER[extension].value
            except KeyError:
                # try the extension directly as a last option
                suffix = extension[1:]

        try:
            return getattr(pandas, f"read_{suffix}")
        except AttributeError:
            raise ValueError(f"Unknown data type {data_type!r}")

    def _make_generator(self) -> Iterator[Tuple[datetime, Mapping[str, Any]]]:
        """Make data iterator."""

        config: InjectorConfig = self.config.injector

        filenames = cycle(config.filenames) if config.repeat else config.filenames
        data_type = config.data_type

        for filename in filenames:
            path = Path(filename).resolve()
            if not path.exists():
                self.logger.error("File does not exist", path=str(path))
                continue

            try:
                loader = self._get_loader(path, data_type)
            except Exception:
                self.logger.exception("Unable to load data", path=str(path), data_type=data_type)
                continue

            self.logger.info("Loading data", path=str(path), data_type=data_type)

            options = {x.name: json.loads(x.value) for x in config.options}
            try:
                data: DataFrame = loader(path, **options)
            except Exception:
                self.logger.exception("File not loadable", path=str(path), data_type=data_type)
                continue

            # index
            if isinstance(data.index, MultiIndex):
                data.reset_index([x for x in data.index.names if x != "time"], inplace=True)

            if "time" in data:
                kind = data["time"].dtype.kind
                unit = "ns" if kind == "i" else "s" if kind == "f" else None
                data["time"] = pandas.to_datetime(data["time"], unit=unit, utc=True)
                data.set_index("time", inplace=True)

            self.logger.info("Emitting data", path=str(path))

            iterator = data.iterrows()
            if data.index.name == "time" and not config.ignore_timestamps:
                iterator = ((timestamp, row.to_dict()) for timestamp, row in iterator)
            else:
                iterator = ((datetime.now(timezone.utc), row.to_dict()) for _, row in iterator)

            yield from iterator

    def on_initialize(
        self,
        configuration: Mapping[str, Any],
        parameters: Optional[Union[Sequence[Message], Mapping[str, Message]]] = None,
    ) -> bool:
        """Initialise application with configuration."""

        if not super().on_initialize(configuration, parameters):
            return False

        self._generator = self._make_generator()

        return True

    @staticmethod
    def _message_name(pair: Tuple[str, Any]) -> str:
        column_name, _ = pair
        return column_name.rsplit(":", 1)[0]

    @staticmethod
    def _field_name(column_name: str) -> str:
        if ":" not in column_name:
            return "value"
        return column_name.rsplit(":", 1)[-1]

    def process(self) -> None:
        """Emit row."""

        if self._generator is None:
            return

        data = next(self._generator, None)

        if data is None:
            self._generator = None
            return

        timestamp, row = data

        time_of_validity = int(timestamp.timestamp() * 1e9)
        messages = {
            name: {
                self._field_name(k): v.tolist() if isinstance(v, generic) else v
                for k, v in values
                if v is not None and (not isinstance(v, float) or isfinite(v))
            }
            for name, values in groupby(
                sorted(row.items(), key=self._message_name), key=self._message_name
            )
        }

        for name, fields in messages.items():
            if not fields:
                continue
            try:
                message = self.make_message(
                    _name=name, time_of_validity=time_of_validity, **inflate(fields.items())
                )
            except Exception:
                self.logger.exception("Unable to create message", message_name=name)
                continue

            self.emit(message)
