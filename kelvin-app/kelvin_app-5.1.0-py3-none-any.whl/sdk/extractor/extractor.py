"""Kelvin SDK Extractor."""

from __future__ import annotations

import json
from operator import attrgetter
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple, Union

import pyarrow
from numpy import dtype
from pandas import DataFrame, Series, Timestamp, to_datetime
from pyarrow import Schema, Table, schema
from pyarrow.parquet import write_to_dataset

from kelvin.app import DataApplication
from kelvin.app.utils import duration, field_info, flatten
from kelvin.icd.message import Message
from kelvin.icd.utils import is_protected

from .config import ExtractorConfig


class ExtractorApp(DataApplication):
    """Kelvin SDK Extractor Application."""

    TOPICS: Mapping[str, Any] = {"#": {"target": "{name}", "storage_type": "buffer"}}

    ARROW_TYPE_MAP = {
        float: pyarrow.float64(),
        int: pyarrow.int64(),
        bool: pyarrow.bool_(),
        str: pyarrow.string(),
        list: pyarrow.list_(pyarrow.float64()),  # assume lists are numeric
    }

    fields: Dict[str, Mapping[str, Tuple[Callable[[Any], Any], dtype]]]
    schema: Schema

    last_timestamp: int = 0
    last_write: int = 0

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialise SDK Extractor."""

        self.fields = {}
        self.schema = None

        super().__init__(*args, **kwargs)

    def on_initialize(
        self,
        configuration: Mapping[str, Any],
        parameters: Optional[Union[Sequence[Message], Mapping[str, Message]]] = None,
    ) -> bool:
        """Initialise application with configuration."""

        if not super().on_initialize(configuration, parameters):
            return False

        fields = {
            "cutoff": pyarrow.timestamp("ns"),
            "time": pyarrow.timestamp("ns"),
        }

        config: ExtractorConfig = self.config.extractor

        for name, info in self.inputs.items():
            message_type = info["type"]
            info = field_info(Message.get_type(message_type))

            getters = self.fields[name] = {}
            for field, T in flatten(info):
                column = f"{name}.{field}"
                arrow_type = fields[column] = self.ARROW_TYPE_MAP[T.mro()[-2]]
                getters[field] = (attrgetter(field), arrow_type.to_pandas_dtype())

        field_summary = "\\n".join(f"  - {k}: {v}" for k, v in fields.items())
        self.logger.info(f"Fields:\\n{field_summary}")

        index_columns = json.dumps([*config.partition_cols, "cutoff", "time"])
        metadata = {"pandas": f'{{"index_columns": {index_columns}}}'.encode("utf-8")}
        self.schema = schema(fields, metadata=metadata)

        if not config.append:
            self.clean_output_path(int(1e100))

        return True

    def clean_output_path(self, cutoff: int) -> None:
        """Clean output path."""

        config: ExtractorConfig = self.config.extractor

        partition_cols = [*config.partition_cols, "cutoff"]
        depth = partition_cols.index("cutoff")

        search_root = "/".join(["*"] * (depth + 1) + ["**"])

        output_path = Path(config.output_path).expanduser().resolve()

        if is_protected(output_path):  # pragma: no cover
            self.logger.warning("Not cleaning protected path", path=str(output_path))
            return

        for path in [*output_path.glob(f"{search_root}/*.parquet")]:
            if depth >= 0:
                name, value = path.relative_to(output_path).parts[depth].split("=", 1)
                if name != "cutoff":
                    self.logger.warning(
                        f"Invalid parquet dataset partitioning: {name} != cutoff", path=str(path)
                    )
                    continue
                timestamp = Timestamp(value).value
                if timestamp >= cutoff:
                    # chunk not ready for the chop
                    continue
            path.unlink()
            for parent in path.parents:
                if parent == output_path:
                    break
                if "=" not in str(parent) or any(parent.glob("*")):
                    break
                parent.rmdir()

    def write_data(self, cutoff: Optional[int] = None) -> None:
        """Write data."""

        config: ExtractorConfig = self.config.extractor

        if cutoff is None:
            cutoff = self.last_time_of_validity

        data: Dict[str, Series] = {}

        for name, fields in self.fields.items():
            buffer = self.data.get(name)
            timestamps, values = buffer.cleanup(0, cutoff) if buffer is not None else ([], [])

            index = to_datetime(timestamps, unit="ns", utc=True)
            time_resolution = config.time_resolution
            if time_resolution is not None:
                index = index.floor(time_resolution.name)

            series = Series(values, index, dtype=object if not values else None)

            for field, (getter, dt) in fields.items():
                column = series.apply(getter)
                if column.dtype != dt:
                    column = column.astype(dt)
                data[f"{name}.{field}"] = column

        data_frame = DataFrame(data)
        if data_frame.empty:
            return

        data_frame.index.name = "time"
        data_frame["cutoff"] = Timestamp(cutoff, tz="UTC")

        partition_cols = [*config.partition_cols, "cutoff"]

        output_path = Path(config.output_path).expanduser().resolve()

        self.logger.info(f"Writing data to {output_path}", shape=data_frame.shape)

        write_to_dataset(
            Table.from_pandas(data_frame, self.schema),
            str(output_path),
            partition_cols,
            coerce_timestamps="us",
            allow_truncated_timestamps=True,
        )

        if config.retention_window is not None:
            self.clean_output_path(cutoff - duration(config.retention_window) * 1e9)

    def process(self) -> None:
        """Update data."""

        config: ExtractorConfig = self.config.extractor

        last_time_of_validity = self.last_time_of_validity

        if last_time_of_validity >= self.last_write + duration(config.batch) * 1e9:
            self.write_data(last_time_of_validity - duration(config.delay) * 1e9)
            self.last_write = last_time_of_validity

    def on_terminate(self) -> None:
        """Terminate app."""

        try:
            self.write_data()
        except Exception:  # nosec
            pass
