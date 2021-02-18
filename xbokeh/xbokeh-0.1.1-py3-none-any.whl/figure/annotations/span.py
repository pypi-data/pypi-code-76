
from xbokeh.figure.annotations.annotation import Annotation
from bokeh.models import Span as _Span


class Span(Annotation):
    def __init__(self, span: _Span) -> None:
        super().__init__(_Span, span)
        self._prev_line_alpha = span.line_alpha

    def show(self):
        self.set_property(line_alpha=self._prev_line_alpha)

    def hide(self):
        self._prev_line_alpha = self._annotation.line_alpha
        self.set_property(line_alpha=0.0)
