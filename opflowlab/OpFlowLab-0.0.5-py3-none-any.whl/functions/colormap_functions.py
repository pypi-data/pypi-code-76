import colorsys
import os
import random

import matplotlib.pyplot as plt
import numpy as np


def list_colormaps():
    return plt.colormaps()


def parse_colormap(colormap):
    if colormap is None:
        _colormap = colormap
    elif type(colormap) == str:
        if colormap.lower() == "none":
            _colormap = None
        else:
            assert colormap in plt.colormaps()
            _colormap = plt.cm.get_cmap(colormap)
    else:
        _colormap = colormap

    return _colormap


# color functions
def create_color(use_alpha=False):
    hue, saturation, luminance = random.random(), 0.5 + random.random() / 2.0, 0.6 + random.random() / 5.0
    red, green, blue = colorsys.hls_to_rgb(hue, saturation, luminance)

    if use_alpha:
        return np.array([red, green, blue, 1])
    else:
        return np.array([[[red, green, blue]]])


def get_colors(inputs, colormap, vmin=None, vmax=None):
    norm = plt.Normalize(vmin, vmax)
    return colormap(norm(inputs))


def plot_colorwheel(colormap,
                    output_folder=None,
                    filename="colormap.png",
                    figsize=(8, 8)):
    """
    Output colormap as a color wheel

    Parameters
    ----------
    colormap : str or None
        Colormap to plot
    output_folder : str
        Folder name that will be created in the main directory to store the vector trace images
    filename : str
        File name of the output
    figsize : (int, int)
        Size of output figure

    Returns
    -------

    See Also
    --------

    """
    # See: https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
    from matplotlib.colors import Normalize

    # Generate a figure with a polar projection
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

    # Define colormap normalization for 0 to 2*pi
    norm = Normalize(np.pi, 3 * np.pi)

    # Plot a color mesh on the polar plot
    # with the color set by the angle
    n = 500  # the number of secants for the mesh
    t = np.linspace(np.pi, 3 * np.pi, n)  # theta values
    r = np.linspace(.8, 1, 2)  # radius values change 0.6 to 0 for full circle
    rg, tg = np.meshgrid(r, t)  # create a r,theta meshgrid
    c = tg  # define color values as theta value
    ax.pcolormesh(t, r, c.T, shading='auto', norm=norm,
                  cmap=colormap)  # plot the colormesh on axis with colormap
    ax.set_yticklabels([])  # turn of radial tick labels (yticks)
    ax.tick_params(pad=20, labelsize=24)  # cosmetic changes to tick labels
    ax.spines['polar'].set_visible(False)  # turn off the axis spine.

    if output_folder is not None:
        plt.savefig(os.path.join(output_folder, filename))

    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    colorwheel = np.asarray(buf)
    colorwheel = colorwheel[np.newaxis, ...]  # to facilitate loading into the imageviewer widget

    return colorwheel
