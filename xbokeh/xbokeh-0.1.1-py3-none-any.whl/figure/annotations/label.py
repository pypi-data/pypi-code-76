
from xbokeh.figure.annotations.annotation import Annotation
from bokeh.models import Label as _Label


class Label(Annotation):
    def __init__(self, label: _Label) -> None:
        super().__init__(_Label, label)
        self._prev_text_alpha = label.text_alpha

    def show(self):
        self.set_property(text_alpha=self._prev_text_alpha)

    def hide(self):
        self._prev_text_alpha = self._annotation.text_alpha
        self.set_property(text_alpha=0.0)
