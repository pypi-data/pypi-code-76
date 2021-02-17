from marshmallow import Schema as Schema_, validate
from marshmallow_dataclass import dataclass as ma_dataclass
from dataclasses import field
from datetime import datetime
from typing import ClassVar, Type, Optional
import enum


class Granularity(enum.Enum):
    PATIENT = "patient"
    EVENT = "event"
    OTHER = "other"


class AnalyticDatasetStatus(enum.Enum):
    NOT_STARTED = "notStarted"
    IN_PROGRESS = "inProgress"
    COMPRESSING = "compressing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalyticDatasetFormat(enum.Enum):
    PARQUET = "parquet"
    CSV = "csv"
    ZIP = "zip"
    MULTIPARTPARQUETZIP = "MULTIPARTPARQUETZIP"


class AnalyticDatasetSource(enum.Enum):
    STANDARD = "standard"
    UPLOAD = "upload"


@ma_dataclass
class AnalyticDatasetModel:
    definition_id: str = field(metadata=dict(data_key="analyticDatasetDefinitionId"))
    asset_id: str = field(metadata=dict(data_key="assetId"))
    created_by: str = field(metadata=dict(data_key="createdByUserId"))
    cohort_of_interest: int = field(metadata=dict(data_key="cohortOfInterestId"), default=0)
    granularity: str = field(metadata=dict(validate=validate.OneOf([o.value for o in Granularity])), default=Granularity.PATIENT.value)
    status: str = field(metadata=dict(validate=validate.OneOf([o.value for o in AnalyticDatasetStatus])), default="")
    source: str = field(metadata=dict(validate=validate.OneOf([o.value for o in AnalyticDatasetSource])), default="")
    output_type: str = field(metadata=dict(validate=validate.OneOf([o.value for o in AnalyticDatasetFormat]), data_key="outputType"), default=AnalyticDatasetFormat.CSV.value)
    result: dict = field(default_factory=dict)
    id: str = ""
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking


@ma_dataclass
class AnalyticDatasetDefinitionModel:
    dataset_schema_id: str = field(metadata=dict(data_key="datasetSchemaId"), default="")
    created_by_user_id: str = field(metadata=dict(data_key="createdByUserId"), default="")
    original_cohort_id: int = field(metadata=dict(data_key="originalCohortId"), default=0)
    original_cohort_asset_id: str = field(metadata=dict(data_key="originalCohortAssetId"), default="")
    study_period_from: Optional[datetime] = field(metadata=dict(data_key="studyPeriodFrom"), default=None)
    study_period_to: Optional[datetime] = field(metadata=dict(data_key="studyPeriodTo"), default=None)
    container_id: str = field(metadata=dict(data_key="containerId"), default="")
    asset_id: str = field(metadata=dict(data_key="workspaceAssetId"), default="")
    patient_count: int = field(metadata=dict(data_key="patientCount"), default=0)
    characteristics: list = field(default_factory=list)
    demographic_characteristics: Optional[list] = field(metadata=dict(data_key="demographicCharacteristics"), default=None)
    rights: dict = field(default_factory=dict)
    capabilities: dict = field(default_factory=dict)
    cohort_of_interest_indexdate_type: Optional[int] = field(metadata=dict(data_key="cohortOfInterestIndexDateType"), default=None)
    source: str = ""
    default_granularity: str = field(metadata=dict(data_key="defaultGranularity"), default="")
    id: str = ""
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    Schema: ClassVar[Type[Schema_]] = Schema_  # needed for type checking
