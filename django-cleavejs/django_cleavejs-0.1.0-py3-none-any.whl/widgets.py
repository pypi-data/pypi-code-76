import json
from dataclasses import InitVar, asdict, dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

from django.conf import settings
from django.forms import Media
from django.forms.widgets import TextInput


__all__ = ("CleaveWidget",)


@dataclass
class CleaveWidget(TextInput):
    # Generic options
    blocks: Optional[Sequence[int]] = None
    delimiter: Optional[str] = None
    delimiters: Optional[Sequence[str]] = None
    delimiterLazyShow: Optional[bool] = None
    prefix: Optional[str] = None
    noImmediatePrefix: Optional[bool] = None
    rawValueTrimPrefix: Optional[bool] = None
    numericOnly: Optional[bool] = None
    uppercase: Optional[bool] = None
    lowercase: Optional[bool] = None
    swapHiddenInput: Optional[bool] = None

    # Numeral options
    numeral: Optional[bool] = None
    numeralThousandsGroupStyle: Optional[bool] = None
    numeralIntegerScale: Optional[int] = None
    numeralDecimalScale: Optional[int] = None
    numeralDecimalMark: Optional[str] = None
    numeralPositiveOnly: Optional[bool] = None
    signBeforePrefix: Optional[bool] = None
    tailPrefix: Optional[bool] = None
    stripLeadingZeroes: Optional[bool] = None

    # Date/Time options
    date: Optional[bool] = None
    datePattern: Optional[Sequence[str]] = None
    dateMin: Optional[str] = None
    dateMax: Optional[str] = None
    time: Optional[bool] = None
    timePattern: Optional[Sequence[str]] = None
    timeFormat: Optional[str] = None

    # Phone number options
    phone: Optional[bool] = None
    phoneRegionCode: Optional[str] = None

    # Credit card number options
    creditCard: Optional[bool] = None
    creditCardStrictMode: Optional[bool] = None

    attrs: InitVar[Optional[Dict[str, str]]] = None

    def __post_init__(self, attrs: Optional[Dict[str, str]] = None):
        # Allow passing own HTML attributes, like TextInput itself
        attrs = {} if attrs is None else attrs.copy()

        # Build dictionary from all Cleave.js options that were set
        cleave_options = {name: value for name, value in asdict(self).items() if value is not None}
        # Pass as JSON string in a data attribute
        attrs["data-dj-cleavejs"] = json.dumps(cleave_options)

        # Allow TextInput to do whatever it is supposed to do
        super().__init__(attrs)

    @property
    def media(self) -> Media:
        js = []
        if hasattr(settings, "CLEAVE_JS"):
            # Add Cleave.js to form media if requested by setting
            js.append(settings.CLEAVE_JS)
        js.append("dj_cleave.js")
        return Media(js=js)
