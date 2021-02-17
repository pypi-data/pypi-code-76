import math
import os
import random

from matplotlib import gridspec
from matplotlib import pyplot as plt

import ternary


def load_sample_heatmap_data(filename="sample_heatmap_data.txt",
                             directory="sample_data"):
    """Loads sample heatmap data."""
    full_filename = os.path.join(directory, filename)
    data = dict()
    handle = open(full_filename)
    for line in handle:
        line = line.strip()
        i, j, k, v = line.split(' ')
        data[(int(i), int(j), int(k))] = float(v)
    return data

def shannon_entropy(p):
    """Computes the Shannon Entropy at a distribution in the simplex."""
    s = 0.
    for i in range(len(p)):
        try:
            s += p[i] * math.log(p[i])
        except ValueError:
            continue
    return -1.*s


if __name__ == '__main__':
    ## Heatmap roundup
    # Careful -- these can use a lot of RAM!
    scale = 30
    function = shannon_entropy
    plt.figure()
    gs = gridspec.GridSpec(2, 3)

    ax = plt.subplot(gs[0, 0])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="triangular")
    tax.boundary()
    tax.set_title("Triangular with Boundary")

    ax = plt.subplot(gs[1, 0])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="t")
    tax.boundary()
    tax.set_title("Triangular without Boundary")

    ax = plt.subplot(gs[0, 1])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="dual-triangular")
    tax.boundary()
    tax.set_title("Dual Triangular with Boundary")

    ax = plt.subplot(gs[1, 1])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="d")
    tax.boundary()
    tax.set_title("Dual Triangular without Boundary")

    ax = plt.subplot(gs[0, 2])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=True, style="hexagonal")
    tax.boundary()
    tax.set_title("Hexagonal with Boundary")

    ax = plt.subplot(gs[1, 2])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmapf(function, boundary=False, style="h")
    tax.boundary()
    tax.set_title("Hexagonal without Boundary")

    ## Heatmaps from data
    # Careful -- these can use a lot of RAM!
    scale = 60
    data = load_sample_heatmap_data()
    plt.figure()
    gs = gridspec.GridSpec(1, 3)
    ax = plt.subplot(gs[0, 0])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="dual-triangular")
    tax.boundary()
    tax.set_title("Dual-Triangular Heatmap from Data")

    ax = plt.subplot(gs[0, 1])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="triangular")
    tax.boundary()
    tax.set_title("Triangular Heatmap from Data")

    ax = plt.subplot(gs[0, 2])
    fig, tax = ternary.figure(ax=ax, scale=scale)
    tax.heatmap(data, style="hexagonal")
    tax.boundary()
    tax.set_title("Hexagonal Heatmap from Data")

    plt.show()
