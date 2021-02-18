from abc import ABC
from xbokeh.common.assertions import assert_type
from bokeh.models import Annotation as _Annotation
from typing import Type


class Annotation(ABC):
    def __init__(self, type_: Type, annotation: _Annotation) -> None:
        super().__init__()
        assert_type(annotation, "annotation", type_)

        self._annotation = annotation

    def set_property(self, **kwargs):
        """
        Updates the model's property
        """
        self._annotation.update(**kwargs)
