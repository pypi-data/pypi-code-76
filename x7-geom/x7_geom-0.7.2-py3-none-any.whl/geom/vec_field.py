import random
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

from .geom import *
from .transform import Transformer, NumpyArray
from .typing import unused


class Mesh(object):
    def __init__(self, bbox: BBox, steps=21):
        self.bbox = bbox
        self.steps = steps
        self.coord_x = np.linspace(bbox.xl, bbox.xh, steps, dtype=np.dtype(float))
        self.coord_y = np.linspace(bbox.yl, bbox.yh, steps, dtype=np.dtype(float))

        mesh = np.meshgrid(self.coord_x, self.coord_y)
        self.x_grid, self.y_grid = mesh
        self.x_shape = self.x_grid.shape

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and self.bbox == other.bbox and self.steps == other.steps
            and np.array_equal(self.coord_x, other.coord_x) and np.array_equal(self.coord_y, other.coord_y)
            and np.array_equal(self.x_grid, other.x_grid) and np.array_equal(self.y_grid, other.y_grid)
            and np.array_equal(self.x_shape, other.x_shape)
        )

    def zeros(self) -> 'VectorField':
        return VectorField(self)

    def uniform(self, magnitude) -> 'VectorField':
        vf = self.zeros()
        for i in range(self.x_shape[0]):
            for j in range(self.x_shape[1]):
                vf.vx[i, j] = random.uniform(-magnitude, magnitude)
                vf.vy[i, j] = random.uniform(-magnitude, magnitude)
        return vf


class VectorField(Transformer):
    LINEAR = False

    def __init__(self, mesh: Mesh, vx=None, vy=None):
        self._mesh = mesh
        self.vx = vx if vx is not None else np.zeros(self.mesh.x_shape)
        self.vy = vy if vy is not None else np.zeros(self.mesh.x_shape)
        self.interp_x = None
        self.interp_y = None

    def __eq__(self, other):
        return (
            isinstance(other, type(self)) and self._mesh == other._mesh
            and np.array_equal(self.vx, other.vx) and np.array_equal(self.vy, other.vy)
        )

    def copy(self):
        return VectorField(self.mesh, np.copy(self.vx), np.copy(self.vy))

    @property
    def mesh(self):
        return self._mesh

    def interp_coords(self, pts: NumpyArray):
        """Lookup/interpolate at all pts.  Return (vx-list, vy-list)"""
        if not self.interp_x:
            coords = (self.mesh.coord_x, self.mesh.coord_y)
            rgi = scipy.interpolate.RegularGridInterpolator
            self.interp_x = rgi(coords, self.vx, method='linear', bounds_error=False, fill_value=None)
            self.interp_y = rgi(coords, self.vy, method='linear', bounds_error=False, fill_value=None)
        return self.interp_x(pts), self.interp_y(pts)

    def lookup(self, x, y):
        """Lookup/interpolate at x, y.  Return (vx, vy)"""
        vx, vy = self.interp_coords(np.array([(x, y)]))
        return vx[0], vy[0]

    def transform_np_pts(self, np_pts: NumpyArray):
        np_pts = np_pts[:2, :].T
        vx_vals, vy_vals = self.interp_coords(np_pts)
        return [(x+vx, y+vy) for (x, y), vx, vy in zip(np_pts, vx_vals, vy_vals)]

    def quiver(self, ax):                               # pragma: no cover
        ax.quiver(self.mesh.x_grid, self.mesh.y_grid, self.vx, self.vy, units='xy', scale=0.1, color='red')

    def plot(self, title=None, ax=None):                # pragma: no cover
        if ax is None:
            fig, ax = plt.subplots()
        self.quiver(ax)

        # ax.set_aspect('equal')

        # plt.xlim(-5, 5)
        # plt.ylim(-5, 5)

        if title:
            plt.title(title, fontsize=10)

        plt.show()

    def normalized(self) -> 'VectorField':
        mags = np.sqrt(np.add(np.multiply(self.vx, self.vx), np.multiply(self.vy, self.vy)))
        max_mag = np.amax(mags)
        vx = np.multiply(self.vx, 1 / max_mag)
        vy = np.multiply(self.vy, 1 / max_mag)
        return VectorField(self.mesh, vx, vy)

    def smoothed(self) -> 'VectorField':
        shape = self.mesh.x_shape
        vx_smoothed = np.zeros(shape)
        vy_smoothed = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                u, v = 0, 0
                count = 0
                r = 2
                for x in range(max(0, i - r), min(shape[0], i + r)):
                    for y in range(max(0, j - r), min(shape[1], j + r)):
                        u += self.vx[x, y]
                        v += self.vy[x, y]
                        count += 1
                center_weight = 20 - 1
                count += center_weight
                u += center_weight * self.vx[i, j]
                v += center_weight * self.vy[i, j]
                vx_smoothed[i, j] = u / count
                vy_smoothed[i, j] = v / count
        vf = VectorField(self.mesh, vx_smoothed, vy_smoothed).normalized()
        return vf

    def scaled(self, sx, sy=None) -> 'VectorField':
        sy = sy if sy is not None else sx
        return VectorField(self.mesh, self.vx * sx, self.vy * sy)


def animate():          # pragma: no cover
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()
    vf = Mesh(BBox(-10, -10, 10, 30), 20).uniform(1)
    vf.quiver(ax)
    data = [vf]

    def update(frame):
        unused(frame)
        data[0] = data[0].smoothed()

    ani = FuncAnimation(fig, update, frames=20)
    try:
        ani.save('/tmp/ani.gif')
    except Exception as err:
        print(err)
    from PIL import Image
    print(Image.SAVE_ALL)
    print(Image.SAVE)
    plt.show()


def main():          # pragma: no cover
    vf = Mesh(BBox(-100, -100, 100, 300), 5).uniform(1)
    vf.plot()

    for n in range(2):
        vf = vf.smoothed()
        vf.plot()

    print('xs:', vf.mesh.coord_x)
    print('ys:', vf.mesh.coord_y)
    print((3, 4))
    print((vf.mesh.coord_x[3], vf.mesh.coord_y[4]))
    print((vf.vx[3][4], vf.vy[3][4]))
    print((4, 4))
    print((vf.mesh.coord_x[4], vf.mesh.coord_y[4]))
    print((vf.vx[4][4], vf.vy[4][4]))
    print('--')
    for dx, dy in [(0, 0), (5, 5), (49, 0)]:
        x, y = (vf.mesh.coord_x[3]+dx, vf.mesh.coord_y[4]+dy)
        print('pt:', (x, y))
        print('->', vf.lookup(x, y))


if __name__ == '__main__':          # pragma: no cover
    main()
    # animate()
