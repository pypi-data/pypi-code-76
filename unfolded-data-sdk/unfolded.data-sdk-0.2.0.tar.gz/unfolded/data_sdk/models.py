from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    """A model representing an Unfoled Studio Dataset
    """
    id: UUID
    name: str
    created_at: datetime = Field(..., alias='createdAt')
    updated_at: datetime = Field(..., alias='updatedAt')
    description: Optional[str]
    is_valid: bool = Field(..., alias='isValid')


class MediaType(str, Enum):
    CSV = 'text/csv'
    GEOJSON = 'application/geo+json'
    JSON = 'application/json'
