from PySide6.QtGui import QPolygonF

from repoly.geometry.abs.mixin.geoobj import GeoObj
from repoly.geometry.orientations import East


class RectPoly(GeoObj, QPolygonF):
    def __init__(self, coords, orien_class: type = East, scale=1):
        point_names = [f"p{i}" for i in range(len(coords))]
        self.coords = coords
        super().__init__(
            point_names, orien_class=orien_class, v=coords, scale=scale
        )

    def topRight(self):
        return QPolygonF.boundingRect(self).topRight()

    def topLeft(self):
        return QPolygonF.boundingRect(self).topLeft()

    def center(self):
        return QPolygonF.boundingRect(self).center()

    def bottomRight(self):
        return QPolygonF.boundingRect(self).bottomRight()

    def bottomLeft(self):
        return QPolygonF.boundingRect(self).bottomLeft()

    def top(self):
        return QPolygonF.boundingRect(self).top()

    def bottom(self):
        return QPolygonF.boundingRect(self).bottom()

    def right(self):
        return QPolygonF.boundingRect(self).right()

    def left(self):
        return QPolygonF.boundingRect(self).left()

    def __iter__(self):
        return iter(self.orientations.values())

    def replace(self, orien_class: type = None, **kwargs):
        kwargs.update(self.points)
        coords = list(kwargs.values())
        orien_class = orien_class or self.orientation.__class__
        return RectPoly(coords, orien_class, self.scale)

    def point(self, prop):
        return self.coords[int(prop[1:])]
