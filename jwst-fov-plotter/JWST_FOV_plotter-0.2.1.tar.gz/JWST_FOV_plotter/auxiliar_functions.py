import matplotlib.pyplot as plt


def plot_single_FOV(SIAF_row, ax=None, color='r', alpha=1.0, **kwargs):
    """
    Plots a contour or shaded area corresponding to a single FOV.

    Arguments:
    SIAF_row -- single row of the the pandas DataFrame including
                the geometry of a single JWST aperture in ICRS coordinates.

    Optional arguments:
    ax -- matplotlib axis to plot the FOV. If None, it gets the current
          axis from matplotlib. Default: None.
    color -- matplotlib color to plot. Default: 'r'.
    alpha -- float transparency value between 0-1. If 1.0, it only plots the
             FOV edges without filling the inner region. Default: 1.0.
    **kwargs -- any other optional matplotlib plotting argument.

    """

    # Reading axes.
    ax = ax or plt.gca()

    # Getting polygon vertices.
    RA = [SIAF_row.RA_1, SIAF_row.RA_2, SIAF_row.RA_3, SIAF_row.RA_4]
    DEC = [SIAF_row.DEC_1, SIAF_row.DEC_2, SIAF_row.DEC_3, SIAF_row.DEC_4]

    # Plotting FOV edges.
    ax.fill(RA, DEC, facecolor='none', edgecolor=color, alpha=alpha, **kwargs)
    # Filling inner region when requested.
    if alpha != 1:
        ax.fill(RA, DEC, facecolor=color, edgecolor='none', alpha=alpha,
                **kwargs)

    return


def reg_file_line(fovs_row, extra_params=''):
    """
    Translates a line of the SIAF DataFrame row to the DS9 region file line
    format.

    Arguments:
    fovs_row -- pandas DataFrame row with the geometry of a single JWST
                aperture.

    Optional arguments:
    extra_params -- str including any additional text to be included at the end
                    of the line of the region file, for extra DS9 region
                    parameters. Default: ''.

    Returns:
    line -- str with a DS9 region file line.

    """

    line = ('polygon(%s, %s, %s, %s, %s, %s, %s, %s) # color=%s %s\n' %
            (fovs_row.RA_1, fovs_row.DEC_1, fovs_row.RA_2, fovs_row.DEC_2,
             fovs_row.RA_3, fovs_row.DEC_3, fovs_row.RA_4, fovs_row.DEC_4,
             fovs_row.plot_color, extra_params))

    return line
