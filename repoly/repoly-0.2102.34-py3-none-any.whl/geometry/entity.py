from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPolygonF

from repoly.geometry.abs.mixin.geoobj import GeoObj
from repoly.geometry.orientations import East


class Entity(GeoObj, QRectF):
    def __init__(
            self,
            position: QPointF,
            relative_size: QPointF,
            orien_class: type = East,
            scale=1,
    ):
        topleft, bottomright = self.calc_absolute_coords(
            position, relative_size, orien_class
        )
        self.position = position
        self.relative_size = relative_size
        super().__init__(
            ["position", "relative_size"],
            orien_class,
            scale,
            topleft=topleft,
            bottomright=bottomright,
        )

    @staticmethod
    def calc_absolute_coords(position, relative_size, orien_class):
        corners = [position, position + orien_class.decode(relative_size)]
        rect = QPolygonF(corners).boundingRect()
        return rect.topLeft(), rect.bottomRight()

    def update_size_for_orientation(self, orien_class):
        relative_size = orien_class.encode(
            self.orientation.decode(self.relative_size)
        )
        return Entity(self.position, relative_size, orien_class, self.scale)

    def replace(
            self,
            orien_class: type = None,
            position: QPointF = None,
            relative_size: QPointF = None,
    ):
        """Create an updated Rect object

        Usage:
        >>> from repoly.geometry.orientations import North, South
        >>> entity = Entity(QPointF(0,0), QPointF(1,3), North)
        >>> entity.topLeft()
        PySide6.QtCore.QPointF(0.000000, -1.000000)
        >>> entity.bottomRight()
        PySide6.QtCore.QPointF(3.000000, 0.000000)
        >>> entity = Entity(QPointF(0,0), QPointF(1,3), South)
        >>> entity.topLeft()
        PySide6.QtCore.QPointF(-3.000000, 0.000000)
        >>> entity.bottomRight()
        PySide6.QtCore.QPointF(0.000000, 1.000000)
        """
        position = position or self.position
        relative_size = relative_size or self.relative_size
        orien_class = orien_class or self.orientation.__class__
        return Entity(position, relative_size, orien_class, self.scale)

    def __iter__(self):
        return iter(self.orientations.values())

    def __getitem__(self, item):
        return self.points[item]

    def point(self, prop):
        return getattr(self, prop)

    @property
    def diagonal(self):
        return self.topLeft(), self.bottomRight()


class PropsMismatch(Exception):
    pass
