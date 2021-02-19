from PySide6.QtCore import QPointF

from repoly.geometry.orientation import Orientation


class East(Orientation):
    matrix = [QPointF(1, 0), QPointF(0, 1)]

    def __init__(self, entity, scale):
        super().__init__(entity, scale)
        self << entity.topRight() << entity.center() << entity.bottomRight()


class South(Orientation):
    matrix = [QPointF(0, 1), QPointF(-1, 0)]

    def __init__(self, entity, scale):
        super().__init__(entity, scale)
        self << entity.bottomRight() << entity.center() << entity.bottomLeft()


class West(Orientation):
    matrix = [QPointF(0, -1), QPointF(-1, 0)]

    def __init__(self, entity, scale):
        super().__init__(entity, scale)
        self << entity.topLeft() << entity.center() << entity.bottomLeft()


class North(Orientation):
    matrix = [QPointF(0, -1), QPointF(1, 0)]

    def __init__(self, entity, scale):
        super().__init__(entity, scale)
        self << entity.topRight() << entity.center() << entity.topLeft()
