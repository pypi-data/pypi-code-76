from typing import List, Optional
from pydantic import BaseModel

from pyrasgo.schemas.data_source import DataSource
from pyrasgo.schemas.granularity import Granularity
from pyrasgo.schemas.feature_set import v0


class FeatureBase(BaseModel):
    id: int


class FeatureCreate(BaseModel):
    name: str
    code: Optional[str]
    description: Optional[str]
    columnId: int
    featureSetId: Optional[int]
    organizationId: int
    orchestrationStatus: Optional[str]
    tags: Optional[List[str]]
    gitRepo: Optional[str]

class FeatureUpdate(BaseModel):
    id: int
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    gitRepo: Optional[str]
    #Can't include these until we create a v1 patch endpoint for features
    #columnId: Optional[int]
    #featureSetId: Optional[int]
    #organizationId: Optional[int]
    orchestrationStatus: Optional[str]
    #tags: Optional[List[str]]

class Feature(FeatureBase):
    id: str  # TODO: Returning feature ids as strings, ensure consistency.
    name: str
    description: Optional[str]
    code: Optional[str]
    columnId: Optional[int]
    dataType: Optional[str]
    dataSource: Optional[DataSource]
    featureSet: Optional[v0.FeatureSet]
    granularities: Optional[List[Granularity]]
    orchestrationStatus: Optional[str]
    tags: Optional[List[str]]
    gitRepo: Optional[str]
    organizationId: Optional[int]

class FeatureStats(BaseModel):
    recCt: Optional[int]
    distinctCt: Optional[int]
    nullRecCt: Optional[int]
    zeroValRecCt: Optional[int]
    meanVal: Optional[str]
    medianVal: Optional[str]
    maxVal: Optional[str]
    minVal: Optional[str]
    sumVal: Optional[str]
    stdDevVal: Optional[str]
    varianceVal: Optional[str]
    rangeVal: Optional[str]
    skewVal: Optional[str]
    kurtosisVal: Optional[str]
    q1Val: Optional[str]
    q3Val: Optional[str]
    IQRVal: Optional[str]
    pct5Val: Optional[str]
    pct95Val: Optional[str]