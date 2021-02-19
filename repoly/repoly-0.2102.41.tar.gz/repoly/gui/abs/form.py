from typing import TYPE_CHECKING
from typing import Union

from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QGroupBox, QLineEdit, QHBoxLayout

from repoly.geometry.entity import PropsMismatch

if TYPE_CHECKING:
    from repoly.geometry.entity import Entity
    from repoly.geometry.rectpoly import RectPoly


class Form(QGroupBox):
    def __init__(
        self,
        title: str,
        prefix: str,
        geoobj: Union["Entity", "RectPoly"],
        callback: callable,
        color: QColor,
    ):
        super().__init__(title)
        self.prefix = prefix
        self.geoobj = geoobj
        self.callback = callback
        self.color = color

        hlayout = QHBoxLayout(self)
        for point in self.geoobj.points:
            hlayout.addWidget(self._setup_point(point))

    def _setup_point(self, name):
        group = QGroupBox(f"{self.prefix} {name}:")
        hlayout = QHBoxLayout(group)
        for axis in ["x", "y"]:
            ledit = QLineEdit(alignment=Qt.AlignRight)
            hlayout.addWidget(ledit)
            point = self.geoobj.points[name]
            ledit.textEdited.connect(self._handle_input__f(name, axis))
            ledit.setText(str(int(round(getattr(point, axis)()))))
        return group

    def _handle_input__f(self, prop, axis):
        """Only accept integers."""

        def func(txt: str):
            try:
                val = int(float(txt))
                if (val < 0 and prop == "position") or val != float(txt):
                    raise ValueError
            except ValueError:
                return
            point = self.geoobj.point(prop)
            oldval = getattr(point, axis)()
            getattr(point, f"set{axis.upper()}")(val)
            try:
                self._update(prop, point)
                self.callback()
            except PropsMismatch:
                # Revert due to inconsistency.
                getattr(point, f"set{axis.upper()}")(oldval)

        return func

    def _update(self, prop, point):
        self.geoobj = self.geoobj.replace(**{prop: point})

    @property
    def relative_size(self):
        return self.geoobj.relative_size
