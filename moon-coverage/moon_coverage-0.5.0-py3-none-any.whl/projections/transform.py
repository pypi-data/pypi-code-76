"""Projection transform."""

import numpy as np

from matplotlib.transforms import Transform

from .proj import Projection


class ProjTransform(Transform):
    """Ground projection transform.

    Parameters
    ----------
    proj: moon_coverage.projections.proj.Projection
        Projection object.

    Raises
    ------
    TypeError:
        If the projection type is invalid.

    """

    input_dims = output_dims = 2

    def __init__(self, proj):
        super().__init__(self)

        if not isinstance(proj, Projection):
            raise TypeError(f'Invalid projection: `{proj}`')

        self._proj = proj

    def __copy__(self, *args):
        raise NotImplementedError('TransformNode instances can not be copied. '
                                  'Consider using frozen() instead.')

    def transform_non_affine(self, values):
        """Projection direct transformation."""
        lon_e, lat = np.transpose(values)
        x, y = self._proj.xy(lon_e, lat)
        return np.column_stack([x, y])

    def transform_path_non_affine(self, path):
        """Path direct transformation."""
        return self._proj.xy_path(path)

    def inverted(self):
        """Projection inverted transformation."""
        return InvertedProjTransform(self._proj)


class InvertedProjTransform(Transform):
    """Inverted ground projection transform.

    Parameters
    ----------
    proj: moon_coverage.projections.proj.Projection
        Projection object.

    Raises
    ------
    TypeError:
        If the projection type is invalid.

    """

    input_dims = output_dims = 2

    def __init__(self, proj):
        super().__init__(self)

        if not isinstance(proj, Projection):
            raise TypeError(f'Invalid projection: `{proj}`')

        self._proj = proj

    def __copy__(self, *args):
        raise NotImplementedError('TransformNode instances can not be copied. '
                                  'Consider using frozen() instead.')

    def transform_non_affine(self, values):
        """Projection inverted transformation."""
        x, y = np.transpose(values)
        lon_e, lat = self._proj.lonlat(x, y)
        return np.column_stack([lon_e, lat])

    def inverted(self):
        """Projection direct transformation."""
        return ProjTransform(self._proj)
