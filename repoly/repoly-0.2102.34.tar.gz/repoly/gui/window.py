from dataclasses import dataclass

from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QLabel,
)

from repoly.app.client import Client
from repoly.geometry.entity import Entity
from repoly.geometry.orientations import North, East
from repoly.geometry.rectpoly import RectPoly
from repoly.gui.canvas import Canvas
from repoly.gui.entityform import EntityForm
from repoly.gui.rectpolyform import RectPolyForm


@dataclass
class Window(QWidget):
    client: Client = None
    position: (int, int) = (30, 30)
    dimensions: (int, int) = (800, 800)
    n_poly_sides: int = 6
    n_entities: int = 3  # Not used by now.
    scale: float = 10

    pressed = False

    def __post_init__(self):
        super().__init__()
        self.setGeometry(*self.position, *self.dimensions)
        self.hlayout = QHBoxLayout(self)
        self._setup_canvas()
        self._setup_right_panel()

    def _setup_canvas(self):
        self.canvas = Canvas(self)
        self.callback = self.canvas.update
        self.hlayout.addWidget(self.canvas)

    def _setup_right_panel(self):
        self.vgroup = QGroupBox()
        self.vgroup.setFixedWidth(650)
        self.vlayout = QVBoxLayout(self.vgroup)
        self._setup_forms()
        self._setup_ioform()
        self.hlayout.addWidget(self.vgroup)

    def _setup_forms(self):
        self._setup_rectpoly()
        self._setup_entities()

    def _setup_rectpoly(self):
        """Rectilinear polygon."""
        vertices = [[17, 25], [24, 25], [24, 17], [40, 17], [40, 42], [17, 42]]
        rectpoly = RectPoly(
            list(map(QPointF, *zip(*vertices))), East, scale=self.scale
        )
        caption = "Rect. Polygon"
        color = QColor("gray").lighter()
        polygonform = RectPolyForm(
            caption, rectpoly, self.callback, color, self.scale
        )
        self.canvas << polygonform
        self.vlayout.addWidget(polygonform)

    def _setup_entities(self):
        # Temporary initial arbitrary setup values...
        a, b, c = QPointF(34, 37), QPointF(17, 26), QPointF(17, 33)
        sizea, sizeb, sizec = QPointF(10, 7), QPointF(3, 5), QPointF(4, 4)
        enta = Entity(a, sizea, North, scale=self.scale)
        entb = Entity(b, sizeb, East, scale=self.scale)
        entc = Entity(c, sizec, East, scale=self.scale)
        self.entityforms = [
            EntityForm("Fst", enta, self.callback, QColor("blue"), self.scale),
            EntityForm(
                "Snd", entb, self.callback, QColor("green"), self.scale
            ),
            EntityForm("Trd", entc, self.callback, QColor("red"), self.scale),
        ]

        for entityform in self.entityforms:
            self.canvas << entityform
            self.vlayout.addWidget(entityform)

    def _setup_ioform(self):
        brgroup = QGroupBox()
        brlayout = QHBoxLayout(brgroup)
        button = QPushButton("Send")
        button.setFixedHeight(150)
        button.clicked.connect(self.send)
        brlayout.addWidget(button)
        self.statusbar = QLabel(text="------", alignment=Qt.AlignCenter)
        brlayout.addWidget(self.statusbar)
        self.vlayout.addWidget(brgroup)

    def send(self):
        msg = self.client.send(geometries=[form.asdict for form in self.canvas.forms])
        self.statusbar.setText(msg)
