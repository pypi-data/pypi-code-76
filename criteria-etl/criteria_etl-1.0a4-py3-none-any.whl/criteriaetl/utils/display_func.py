import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.display import display


def unlimit_display_option(option, *args):
    """
    Wrapper for display function. It displays a DataFrame temporally
    setting an option to infinite.

    Parameters
    ----------
    option : str,
        indicates the option to be set to infinite.
    args : positional arguments,
        used as arguments of the `display` function.
    """
    current_option_value = pd.get_option(option)
    pd.set_option(option, None)
    display(*args)
    pd.set_option(option, current_option_value)


def cdisplay(*args):
    """
    Wrapper for display function. It displays  all columns of DataFrame
    objects present in `*args`
    """
    unlimit_display_option('display.max_columns', *args)


def rdisplay(*args):
    """
    Wrapper for display function. It displays  all columns of DataFrame
    objects present in `*args`
    """
    unlimit_display_option('display.max_rows', *args)


def percentage_count_plot(
        plot_srs, labels='index', pct_display='pdf', pct_scale='sum',
        display_legend=True, subplots_kwargs={}):
    """
    Draws barplot with percentages annotations calculated from
    `plot_srs`.

    Parameters
    ----------
    plot_srs : Series
        contains heighs of bars to be drawn. Percentages are calculated
        from it.
    labels : str or iterable
        contains the labels to be used as ticklabels on the x axis.
    pct_display : str in {'pdf', 'cdf'},
        Whether the displayed percentages show the Probability Density
        Function or the Cummulative Distribution Function.
    pct_scale : str in {'sum', ?}
        Defines which agggregation is used for normalizing `plot_srs`
        and derive percentages.
    display_legend : bool,
        Whether or not the legend is displayed.
    subplots_kwargs
    """

    fig, ax = plt.subplots(constrained_layout=True, **subplots_kwargs)
    labels_ = plot_srs.index if labels == 'index' else labels

    ax.bar(x=labels_, height=plot_srs,
           color=sns.color_palette(n_colors=len(plot_srs)))

    plot_srs_pct = plot_srs if pct_display == 'pdf' else plot_srs.transform(
        'cumsum')
    plot_srs_pct /= plot_srs.agg(pct_scale)

    # Add this loop to add the annotations
    for i, (p, l) in enumerate(zip(ax.patches, labels_)):
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        annotation = ax.annotate('{:.1%}'.format(plot_srs_pct.iloc[i]),
                                 (x + width / 2, y + height + 0.01),
                                 ha='center', va='bottom')
        p.set_label(l)
    if display_legend:
        plt.legend(bbox_to_anchor=(1., 1))

    return fig, ax