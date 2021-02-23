import base64
import pathlib
import os.path
import textwrap
from typing import Dict
from marshmallow import Schema, fields
from .utils import get_mimetype


class SafeAssetStringField(fields.Field):
    """
    Custom field handler for making strings safer and enforcing maximum length.
    """

    def __init__(self, *args, max_width: int = 100, **kwargs):  # type: ignore
        self._max_width = max_width
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):  # type: ignore
        if value and len(value) > self._max_width:
            name, ext = os.path.splitext(value)
            name = textwrap.shorten(
                name,
                width=(self._max_width - len(ext)),
                placeholder='')
            return f'{name}{ext}'
        return value

    def _deserialize(self, value, attr, data, **kwargs):  # type: ignore
        return value


class Base64Field(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):  # type: ignore
        if value:
            return base64.b64encode(value).decode()

    def _deserialize(self, value, attr, data, **kwargs):  # type: ignore
        if value:
            return base64.b64decode(value)


class FileSchema(Schema):
    user_id = fields.String(data_key='userId')
    name = SafeAssetStringField()
    mime_type = fields.String(data_key='mimeType')
    metadada = fields.Dict()
    file_size = fields.Integer(data_key='fileSize')
    contents = Base64Field()
    id = fields.String()
    created = fields.DateTime()
    updated = fields.DateTime()


class FileCreateSchema(FileSchema):
    class Meta:
        fields = ('name', 'mime_type', 'contents', 'metadata')

    @classmethod
    def from_file(cls, file_path: pathlib.Path, metadata: Dict = None, mime_type: str = None) -> Dict:
        """
        Create a Json payload, from a Path object.

        Args:
            file_path: file to process
            metadata: optional object for extra metadata
            mime_type: optional file mime type; guesses when not provided

        """
        data = {
            'name': file_path.name,
            'mime_type': mime_type or get_mimetype(file_path),
            'contents': file_path.read_bytes(),
        }
        if metadata is not None:
            data['metadata'] = metadata
        return cls().dump(data)
