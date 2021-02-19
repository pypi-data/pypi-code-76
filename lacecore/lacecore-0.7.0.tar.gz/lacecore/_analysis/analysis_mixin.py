from polliwog import Box
import vg


class AnalysisMixin:
    @property
    def vertex_centroid(self):
        """
        The centroid or geometric average of the vertices.
        """
        return vg.average(self.v)

    @property
    def bounding_box(self):
        """
        A bounding box around the vertices.

        Returns:
            polliwog.Box: The bounding box.

        See also:
            https://polliwog.readthedocs.io/en/latest/#polliwog.Box
        """
        return Box.from_points(self.v)

    def apex(self, along):
        """
        Find the most extreme vertex in the direction provided.

        Args:
            along (np.arraylike): A `(3,)` direction of interest.

        Returns:
            np.ndarray: A copy of the point in `self.v` which lies furthest
                in the direction of interest.
        """
        return vg.apex(self.v, along=along)
