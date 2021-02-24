import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

class DistanceMatrix:
    def __init__(self, full, condensed, metric):
        """
        Parameters
        ----------
        full : ndarray
            Distance matrix whose (i,j)th entry holds the distance between items i and j of the dataset whose
            distances we're interested in.
        condensed : ndarray
            Vector created by flattening the upper triangular half of the full matrix above. Its usefulness
            stems from the fact that a distance matrix created from an 'undirected' dataset will be symmetric.
        metric : str
            Distance metric used to create this matrix
            
        """

        self.full = full
        self.condensed = condensed
        self.metric = metric

    def plot_heatmap(self, ax=None, triangular=True, cmap="YlGnBu"):
        """Plot this distance matrix as a heatmap

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Matplotlib Axes to plot on
        triangular : bool, optional
            Whether or not to omit the upper triangular entries; only useful if matrix is symmetric
        cmap : matplotlib.cm
            Desired colour map to use for the plot
            
        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()

        # A distance matrix created from an undirected graph will be symmetric, so a triangular heatmap omits
        # redundant data in this case
        if triangular:
            mask = np.zeros_like(self.full)
            mask[np.triu_indices_from(mask)] = True
        else:
            mask = None
        with sb.axes_style("ticks"):
            sb.heatmap(self.full, ax=ax, mask=mask, square=True, cmap=cmap)
