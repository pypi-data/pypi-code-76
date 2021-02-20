import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .widgets import HexColorWidget


HEX_COLOR_RE = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
hex_color_validator = RegexValidator(
    HEX_COLOR_RE,
    message=_("Enter a valid hex color, eg. #ff00ff or #f0f"),
    code="invalid",
)


class HexColorField(models.CharField):
    description = _("A css color with a preview")
    default_validators = [hex_color_validator]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 7)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = HexColorWidget
        return super().formfield(**kwargs)
