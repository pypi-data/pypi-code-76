from marshmallow import fields, validate

#from oarepo_invenio_model.marshmallow import InvenioRecordMetadataSchemaV1Mixin
from oarepo_documents.marshmallow.document import DocumentSchemaV1


class SampleSchemaV1(DocumentSchemaV1):
    extra_property = fields.String(validate=validate.Length(min=5), required=False)
