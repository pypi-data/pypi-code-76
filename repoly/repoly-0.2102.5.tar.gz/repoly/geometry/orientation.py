from typing import TYPE_CHECKING, Union

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF, Qt, QPainter, QColor
from PySide6.QtWidgets import QGraphicsPolygonItem

if TYPE_CHECKING:
    from repoly.geometry.abs.mixin.geoobj import GeoObj
    from repoly.geometry.entity import Entity
    from repoly.geometry.rectpoly import RectPoly


class Orientation(QPolygonF):
    matrix = None

    def __init__(
        self, entity: Union["GeoObj", "Entity", "RectPoly"], scale: float
    ):
        super().__init__()
        self.scale = scale
        self.entity = entity
        self.name = self.__class__.__name__.lower()

    @property
    def asshape(self):
        scaled = QPolygonF([self.scale * c for c in self.toList()])
        return QGraphicsPolygonItem(scaled).shape()

    def contains(self, point):
        if self.containsPoint(point, Qt.OddEvenFill):
            return self

    def draw(self, painter: QPainter, color: QColor, highlight: bool):
        if highlight:
            color = color.lighter()
        painter.setBrush(color)
        painter.setPen(QColor(0, 0, 0, 0))
        painter.drawPath(self.asshape)
        painter.setPen(QColor("red"))

    def __lshift__(self, other):  # Override due to a bug in qt.
        self.append(other)
        return self

    @classmethod
    def encode(cls, absolute_size: QPointF):
        w = QPointF.dotProduct(absolute_size, cls.matrix[0])
        h = QPointF.dotProduct(absolute_size, cls.matrix[1])
        return QPointF(w, h)

    @classmethod
    def decode(cls, relative_size: QPointF):
        """Transform a given point to deltas applicable to absolute coordinate system"""
        w = QPointF.dotProduct(relative_size, cls.matrixt("x"))
        h = QPointF.dotProduct(relative_size, cls.matrixt("y"))
        return QPointF(w, h)

    @classmethod
    def matrixt(cls, axis):
        """Transpose"""
        return QPointF(
            getattr(cls.matrix[0], axis)(), getattr(cls.matrix[1], axis)()
        )
