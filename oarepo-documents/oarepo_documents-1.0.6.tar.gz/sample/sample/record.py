from invenio_records.api import Record
from oarepo_actions.decorators import action
from oarepo_validate import MarshmallowValidatedRecordMixin, SchemaKeepingRecordMixin

from oarepo_documents.api import DocumentRecordMixin

from .constants import SAMPLE_ALLOWED_SCHEMAS, SAMPLE_PREFERRED_SCHEMA
from .marshmallow import SampleSchemaV1


class SampleRecord(SchemaKeepingRecordMixin,
                   MarshmallowValidatedRecordMixin,
                   DocumentRecordMixin,
                   Record):
    ALLOWED_SCHEMAS = SAMPLE_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = SAMPLE_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = SampleSchemaV1

    @property
    def canonical_url(self):
        return f'https://localhost:5000/records/{self["pid"]}'

    def validate(self, **kwargs):
        return super().validate(**kwargs)
