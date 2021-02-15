from PySide6.QtGui import QColor, QPainter, Qt, QPolygonF
from PySide6.QtWidgets import QGraphicsPolygonItem

from repoly.geometry.rectpoly import RectPoly
from repoly.gui.abs.form import Form


class RectPolyForm(Form):
    def __init__(
        self,
        title: str,
        rectpoly: RectPoly,
        callback: callable,
        color: QColor,
        scale: float,
    ):
        super().__init__(title, "Vertex", rectpoly, callback, color)
        self.scale = scale

    def draw(self, painter: QPainter):
        painter.setBrush(self.color)
        painter.drawPath(self.asshape)
        color = self.color.darker()
        color.setAlpha(50)
        self.geoobj.orientation.draw(painter, color, True)

    @property
    def rectpoly(self):
        return self.geoobj

    @property
    def asshape(self):
        scaled = QPolygonF([self.scale * c for c in self.rectpoly.coords])
        return QGraphicsPolygonItem(scaled).shape()

    def replace(
        self,
        title: str = None,
        geoobj: RectPoly = None,
        callback: callable = None,
        color: QColor = None,
    ):
        if title is None:
            title = self.title()
        if geoobj is None:
            geoobj = self.rectpoly
        if callback is None:
            callback = self.callback
        if color is None:
            color = self.color
        return RectPolyForm(title, geoobj, callback, color, self.scale)

    def orientation_at(self, pos):
        if not self.rectpoly.containsPoint(pos, Qt.OddEvenFill):
            return
        for orientation in self.rectpoly:
            if orientation.containsPoint(pos, Qt.OddEvenFill):
                return orientation

    @property
    def asdict(self):
        dic = {}
        dic.update(
            type="Polygon",
            coordinates=[list(c.toTuple()) for c in self.rectpoly.coords],
            orientation=self.rectpoly.orientation.name,
        )
        return dic
