from typing import List
from x7.geom.geom import PointUnionList
import matplotlib.pyplot as plt
from matplotlib.artist import Artist

ArtistList = List[Artist]

__all__ = ['ArtistList', 'plot', 'plot_show']


def plot(xy: PointUnionList, color='black', label=None,
         linewidth=None, linestyle=None,
         plotter=None) -> Artist:
    """Quick entry to pyplot.plot() for List[Point]"""
    plotter = plotter or plt
    artist, = plotter.plot(*zip(*xy), color, label=label,
                           linestyle=linestyle, linewidth=linewidth,
                           solid_capstyle='round' if linewidth and linewidth > 1 else None)
    # if label:
    #    for artist in artists:
    #        artist.set_label(label)
    return artist


def plot_show():
    """Quick entry to pyplot.show()"""
    plt.show()
