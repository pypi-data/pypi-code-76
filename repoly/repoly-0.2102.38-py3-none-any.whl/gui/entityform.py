from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPainter, Qt, QBrush

from repoly.geometry.entity import Entity
from repoly.gui.abs.form import Form


class EntityForm(Form):
    def __init__(
        self,
        title: str,
        entity: Entity,
        callback: callable,
        color: QColor,
        scale: float,
    ):
        super().__init__(title, "Property", entity, callback, color)
        self.scale = scale

    @property
    def entity(self):
        return self.geoobj

    def draw(self, painter: QPainter):
        for triangle in self.entity:
            highlight = triangle.name == self.entity.orientation.name
            triangle.draw(painter, self.color, highlight)
        self.draw_origin(painter)

    def draw_origin(self, painter):
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        margin = QPointF(8, 8)
        reddot = self.scale * self.entity.position
        painter.drawEllipse(reddot, *margin.toTuple())

    def replace(
        self,
        title: str = None,
        geoobj: Entity = None,
        callback: callable = None,
        color: QColor = None,
    ):
        if title is None:
            title = self.title()
        if geoobj is None:
            geoobj = self.entity
        if callback is None:
            callback = self.callback
        if color is None:
            color = self.color
        return EntityForm(title, geoobj, callback, color, self.scale)

    def orientation_at(self, pos):
        if not self.entity.contains(pos):
            return
        for orientation in self.entity:
            if orientation.containsPoint(pos, Qt.OddEvenFill):
                return orientation

    @property
    def asdict(self):
        dic = {}
        dic.update(
            type="Rectangle",
            pos={"x": self.entity.position.x(), "y": self.entity.position.y()},
            size={"x": self.relative_size.x(), "y": self.relative_size.y()},
            orientation=self.entity.orientation.name,
        )
        return dic
