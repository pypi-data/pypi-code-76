from abc import abstractmethod

from repoly.geometry.orientations import East, North, West, South


class GeoObj:
    _relative_size = None

    def __init__(
        self, point_names: list, orien_class: type = East, scale=1, **kwargs
    ):
        super().__init__(*kwargs.values())
        self.scale = scale

        # Instantiate orientations.
        self.orientation = orien_class(self, scale)
        self.orientations = {}
        for klass in [East, North, West, South]:
            if klass == self.orientation:
                self.orientations[klass.__name__.lower()] = self.orientation
            else:
                self.orientations[klass.__name__.lower()] = klass(self, scale)

        # Dict for relevant points.
        self.__dict__.update(self.orientations)
        self.points = {}
        for prop in point_names:
            self.points[prop] = self.point(prop)
        self.__dict__.update(self.points)

    def missing_impl(self, method):
        """Qt prevents ABC inheritance, so we raise the exception by hand."""
        raise TypeError(
            f"Can't instantiate abstract class {self.__class__} with abstract method '{method}'."
        )

    @abstractmethod
    def point(self, prop):
        self.missing_impl("point")
