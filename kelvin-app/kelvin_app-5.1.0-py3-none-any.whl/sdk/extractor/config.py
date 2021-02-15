"""ExtractorConfig Message."""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import Field

from kelvin.icd.message import Message
from kelvin.icd.types import Float64_


class TimeResolution(Enum):
    """TimeResolution enumeration."""

    S = "s"
    L = "ms"
    U = "us"
    N = "ns"


class ExtractorConfig(Message):
    """Extractor Configuration"""

    _TYPE = "kelvin.sdk.extractor.config"

    output_path: str = Field("", description="Output path for saving data")
    partition_cols: List[str] = Field([], description="Columns to partition data")
    time_resolution: Optional[TimeResolution] = Field(None, description="Time resolution")
    append: bool = Field(False, description="Append data")
    batch: Float64_ = Field(0.0, description="Batch window")
    delay: Float64_ = Field(0.0, description="Delay window")
    retention_window: Optional[Float64_] = Field(None, description="Retention window")
