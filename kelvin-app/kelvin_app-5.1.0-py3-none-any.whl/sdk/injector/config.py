"""InjectorConfig Message."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import Field

from kelvin.icd.message import Message


class DataType(Enum):
    """DataType enumeration."""

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    TABLE = "table"


class Option(Message):
    """Option"""

    _TYPE = "kelvin.sdk.injector.option"

    name: str = Field("", description="Option name")
    value: str = Field("", description="Option value (JSON-encoded)")


class InjectorConfig(Message):
    """Injector Configuration"""

    _TYPE = "kelvin.sdk.injector.config"

    filenames: List[str] = Field([], description="Filenames to load")
    data_type: Optional[DataType] = Field(None, description="Type of data to load from files")
    options: List[Option] = Field([], description="Additional options for loader")
    repeat: bool = Field(False, description="Loop files continuously")
    ignore_timestamps: bool = Field(False, description="Ignore timestamps from files")
