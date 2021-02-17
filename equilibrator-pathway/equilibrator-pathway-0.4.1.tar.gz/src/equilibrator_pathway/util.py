# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018-2020 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018-2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from typing import Iterable

import numpy as np
from equilibrator_api import Q_
from matplotlib import pyplot as plt
from scipy import stats


# cell dry weight, [Winkler and Wilson, 1966,
# http://www.jbc.org/content/241/10/2200.full.pdf+html]
CELL_VOL_PER_DW = Q_("2.7 milliliter / gram")

ECF_DEFAULTS = {
    "flux_unit": "mM/s",
    "version": "3",  # options: '1', '2', '3', or '4'
    "kcat_source": "gmean",  # options: 'fwd' or 'gmean'
    "denominator": "CM",  # options: 'S', 'SP', '1S', '1SP', or 'CM'
    "regularization": "volume",  # options: None, 'volume', or 'quadratic'
    "objective": "enzyme + metabolite",  # options: 'enzyme' or 'enzyme + metabolite'
    "standard_concentration": "1 M",  # must be explicit in order to avoid
    # confusion with other scripts that use different conventions (e.g. 1 mM)
}


def PlotCorrelation(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    labels: Iterable[str],
    mask=None,
    scale="log",
    grid=True,
) -> None:
    """Plot correlations between predicted and observed values.

    scale - if 'log' indicates that the regression should be done on the
        logscale data.
    """
    assert x.shape == y.shape, "x and y must be arrays of the same shape"

    if mask is None:
        mask = (np.nan_to_num(x) > 0) & (np.nan_to_num(y) > 0)

    ax.grid(grid)
    if scale == "log":
        ax.set_xscale("log")
        ax.set_yscale("log")
        log_x = np.log10(x[mask])
        log_y = np.log10(y[mask])
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            log_x.flat, log_y.flat
        )
        rmse = np.sqrt(np.power(log_x - log_y, 2).mean())
    else:
        ax.set_xscale("linear")
        ax.set_yscale("linear")
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            x[mask].flat, y[mask].flat
        )
        rmse = np.sqrt(np.power(x[mask] - y[mask], 2).mean())
    ax.plot(x[mask], y[mask], ".", markersize=15, color="red", alpha=0.5)
    ax.plot(x[~mask], y[~mask], ".", markersize=15, color="blue", alpha=0.5)

    min_x, max_x = ax.get_xlim()
    min_y, max_y = ax.get_ylim()
    ax.set_xlim(min(min_x, min_y), max(max_x, max_y))
    ax.set_ylim(min(min_x, min_y), max(max_x, max_y))
    ax.plot(
        [0, 1], [0, 1], ":", color="black", alpha=0.4, transform=ax.transAxes
    )

    box_text = "RMSE = %.2f\n$r^2$ = %.2f\n(p = %.1e)" % (
        rmse,
        r_value ** 2,
        p_value,
    )

    ax.text(
        0.05,
        0.95,
        box_text,
        verticalalignment="top",
        horizontalalignment="left",
        transform=ax.transAxes,
        color="black",
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.5, "pad": 10},
    )

    for label, x_i, y_i, m in zip(labels, x, y, mask):
        if m:
            ax.text(x_i, y_i, label, alpha=1.0)
        elif np.isfinite(x_i) and np.isfinite(y_i):
            if scale == "linear" or (x_i > 0 and y_i > 0):
                ax.text(x_i, y_i, label, alpha=0.4)
