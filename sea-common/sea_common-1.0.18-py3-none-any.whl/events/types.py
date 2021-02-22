from enum import Enum
from typing import List, TypedDict
import strawberry


class Subjects(Enum):
    TargetCreated = 'target:created'
    AntisenseSeriesCreated = 'antisenseSeries:created'
    SirnaSeriesCreated = 'sirnaSeries:created'
    AsosCreated = 'asos:created'


class TargetCreatedData(TypedDict):
    organism_id: int
    id: strawberry.ID
    custom: bool
    rna_id: str
    spliced: bool
    symbol: str


class AntisenseSeriesCreatedData(TypedDict):
    target_id: int
    id: strawberry.ID
    length: int


class SirnaSeriesCreatedData(TypedDict):
    target_id: int
    id: strawberry.ID
    config: List[int]


class AsoData(TypedDict):
    antisense_id: int
    id: strawberry.ID
    name: str


class AsosCreatedData(TypedDict):
    asos: List[AsoData]
