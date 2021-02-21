from flask import Flask
from nidhoggr.core.texture import TextureType
from werkzeug.routing import BaseConverter, ValidationError


class TextureTypeConverter(BaseConverter):
    def to_python(self, value):
        try:
            return TextureType(value.upper())
        except ValueError as e:
            raise ValidationError(f"Failed to parse {value} as registered texture type") from e

    def to_url(self, value):
        return str(value)


class FlaskTextureType:
    """Flask extension providing a Texture type url converter"""
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.url_map.converters['kind'] = TextureTypeConverter
