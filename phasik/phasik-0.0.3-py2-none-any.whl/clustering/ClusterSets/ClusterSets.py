import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score
from copy import deepcopy

from collections import Sequence
from phasik.clustering.Silhouettes import Silhouettes
from phasik.utils import drawing
from phasik.utils.plotting import plot_phases, plot_events

class ClusterSets(Sequence):
    """Class representing a range of cluster sets

    e.g. for a range of cluster sets created by stopping clustering after 2 clusters have formed, then 3 clusters,
    then 4, ..., etc. In order to plot data across a range of cluster sets, it is useful to have a dedicated class,
    rather than (e.g.) just using a Python list of ClusterSet objects

    __getitem__ and __len__ are the the two methods of the Sequence base class that we must override
    """

    def __init__(self, cluster_sets, snapshots, limit_type):
        """
        Parameters
        ----------
        cluster_sets : iterable of ClusterSet 
            
        snapshots : Snapshots
            
        limit_type : str
            Method that was used to determine when to stop clustering when creating these cluster
            sets. e.g. A cluster set can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance away from each other
            ('distance').
        """

        self._cluster_sets = cluster_sets
        self.snapshots = snapshots
        self.clusters = np.array([cluster_set.clusters for cluster_set in cluster_sets])
        self.sizes = np.array([cluster_set.size for cluster_set in cluster_sets])
        self.limit_type = limit_type
        self.limits = np.array([cluster_set.limit for cluster_set in cluster_sets])
        self.silhouettes = Silhouettes([cluster_set.silhouette for cluster_set in cluster_sets])

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Create a 'blank' ClusterSets...
            cluster_sets = ClusterSets([], self.snapshots, self.limit_type)
            # ...and populate its fields with slices from this ClusterSets
            cluster_sets._cluster_sets = self._cluster_sets[key]
            cluster_sets.clusters = self.clusters[key]
            cluster_sets.sizes = self.sizes[key]
            cluster_sets.limits = self.limits[key]
            cluster_sets.silhouettes = self.silhouettes[key]
            return cluster_sets
        else:
            return self._cluster_sets[key]

    def __len__(self):
        return len(self._cluster_sets)

    def plot(self, ax=None, colouring="consistent"):
        """Plot these cluster sets as a scatter graph

        Parameters
        ----------
        ax : matplotlib.Axes, optional 
            Matplotlib axes on which to plot
            
        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()
            
        if colouring=="consistent":
            self = sort_for_colouring(self, method="consistent")
        elif colouring=="ascending":
            self = sort_for_colouring(self, method="ascending")
        else:
            pass
            
        for cluster_set in self._cluster_sets:
#            (cmap, number_of_colors) = ('tab20', 20) if cluster_set.size > 10 else ('tab10', 10)
            # replace by single colour palette with 20 colours such that first 10 colours are same as tab10
            cmap = drawing.palette_20_ordered(as_map=True)
            number_of_colors = 20
            cluster_set.plot(
                ax=ax, y_height=cluster_set.limit, cmap=cmap, number_of_colors=number_of_colors)

    def plot_with_average_silhouettes(self, axs, colouring="consistent"):
        """Plot these cluster sets as a scatter graph, along with the average silhouettes and cluster set sizes

        Parameters
        ----------
        axs : list of matplotlib.Axes
            Axes on which to plot; should be an indexable object with at least three items
            
        Returns
        -------
        None
        """
            
        self.plot(ax=axs[0], colouring=colouring)
        self.plot_average_silhouettes(ax=axs[1])
        if len(axs)>2:
            self.plot_sizes(ax=axs[2])

    def plot_and_format_with_average_silhouettes(self, axs, events, phases, time_ticks=None, colouring="consistent"):
        """Plot and format these cluster sets as a scatter graph, along with the average silhouettes and cluster set
        sizes

        Our pattern generally has been to leave all formatting in the jupyter notebooks, but this method is used
        by several different notebooks, so it makes sense to put it somewhere common.

        Parameters
        ----------
        axs : list of matplotlib.Axes
            Axes on which to plot; should be an indexable object with at least three items
        events :
            Any events that should be plotted on the scatter graph
        phases : 
            Any phases that should be plotted on the scatter graph
        time_ticks : list or array
            The ticks that should be displayed along the x-axis (time axis)
            
        Returns
        -------
        None
        """

        (ax1, ax2, ax3) = (axs[0], axs[1], axs[2])

        # Plot
        ax3.tick_params(labelleft=True, labelbottom=True)
        self.plot_with_average_silhouettes((ax1, ax2, ax3), colouring=colouring)
        drawing.adjust_margin(ax1, bottom=(0.15 if phases else 0))
        plot_events(events, ax=ax1)
        plot_phases(phases, ax=ax1, y_pos=0.04, ymax=0.1)

        # Format
        ax1.set_xlabel("Time")
        ax1.set_ylabel(drawing.display_name(self.limit_type))
        ax1.tick_params(labelbottom=True)
        if time_ticks:
            ax1.set_xticks(time_ticks)

        ax2.set_xlabel("Average silhouette")
        ax2.set_xlim((0, 1))
        ax2.tick_params(labelleft=True, labelbottom=True)

        ax3.set_xlabel("Actual # clusters")

    def plot_average_silhouettes(self, ax=None):
        """Plot the average silhouettes across this range of cluster sets

        Parameters
        ----------
        axs : matplotlib.Axes, optional
            Axes on which to plot
        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()
        ax.plot(self.silhouettes.averages, self.limits, 'ko-')

    def plot_sizes(self, ax=None):
        """Plot the average cluster set sizes across this range of cluster sets

        Parameters
        ----------
        axs : matplotlib.Axes, optional
            Axes on which to plot
        
        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()
        ax.plot(self.sizes, self.limits, 'ko-')

    def plot_silhouette_samples(self, axs, colouring="consistent"):
        """Plot the average silhouettes across this range of cluster sets

        Parameters
        ----------
        axs : list of matplotlib.Axes
            Axes on which to plot; should be an iterable object with at least as many items as there
            are cluster sets in this class.
            
        Returns
        -------
        None
        """

        if colouring=="consistent":
            self = sort_for_colouring(self)

        for cluster_set, ax in zip(self._cluster_sets, axs.flatten()):
            cluster_set.plot_silhouette_samples(ax=ax)
            
            
            
def rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method="ward"):

    """
    Compute Rand Index to compare any method to a reference method, for all combinations of methods and number of clusters
    
    
    Parameters
    ----------
    valid_cluster_sets : list
    
    reference_method : str
    
    Returns
    -------
    
    rand_scores : ndarray 
        Array of dimension (n_sizes, n_methods) with rand index scores 
    
    """
    
    valid_methods = [sets[1] for sets in valid_cluster_sets]
    
    i_ref = valid_methods.index(reference_method)
    clusters_ref = valid_cluster_sets[i_ref][0]

    # compute Rand index to compare each method with reference method, for each number of clusters
    n_sizes = len(clusters_ref.sizes)
    n_methods = len(valid_cluster_sets)

    rand_scores = np.zeros((n_sizes, n_methods))

    for i_size, size in enumerate(clusters_ref.sizes):
        for i_method, method in enumerate(valid_methods):
            
            clusters2 = valid_cluster_sets[i_method][0]
            
            rand_index = adjusted_rand_score(clusters_ref.clusters[i_size], clusters2.clusters[i_size])
            rand_scores[i_size, i_method] = rand_index         
            
    return rand_scores  
    
    
def plot_randindex_bars_over_methods_and_sizes(valid_cluster_sets, reference_method="ward", ax=None, plot_ref=False):

    "Plot Rand Index as bars, to compare any method to a reference method, for all combinations of methods and number of clusters"""

    if ax is None:
        ax = plt.gca()

    valid_methods = [sets[1] for sets in valid_cluster_sets]
    
    i_ref = valid_methods.index(reference_method)
    clusters_ref = valid_cluster_sets[i_ref][0]

    rand_index = rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method)
    n_sizes, n_methods = rand_index.shape
    
    if not plot_ref :
        n_methods -= 1 
         
    width = 1 # bar width
    width_size = n_methods * width # width of all bars for a given # of clusters
    width_inter_size = 4 * width # width space between two # of clusters

    xlabels = clusters_ref.sizes
    xticks = np.arange(n_sizes) * (width_size + width_inter_size) # the label locations

    for i, method in enumerate(valid_methods): 
              
        heights = rand_index[:, i]
        
        if not plot_ref and i==i_ref: 
            pass
        else : # don't plot i_ref if plot_ref is False
            ax.bar(xticks + i * width - width_size / 2, heights, width, label=method)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    
def cluster_sort(clusters, final_labels=None) : 
    """
    Return array of cluster labels sorted in order of appearance, with clusters unchanged
    Example: 
    >>> clusters = np.array([2, 2, 2, 3, 3, 1, 1, 1])
    >>> cluster_sort(clusters)
    [ 1 1 1 2 2 3 3 3 ]
    """
    arr = - clusters 
    i = 1
    for j, el in enumerate(arr) :
        if el >= 0 : 
            pass
        else : 
            arr[arr==el] = i
            i += 1
            
    if isinstance(final_labels , list) :
        arr = list(map(lambda i : final_labels[i-1], arr))
            
    # check that the clustering has not changed
    assert adjusted_rand_score(clusters, arr)==1
    
    return arr
    
def sort_for_colouring(cluster_sets, method="consistent") : 
    
    n = len(cluster_sets.sizes)
    
    cluster_sets_sorted = deepcopy(cluster_sets)
    new_clusters = []
    
    if method=="ascending" : 
        cluster_sets_sorted.clusters[0] = cluster_sort(cluster_sets_sorted.clusters[0])
        cluster_sets_sorted[0].clusters = cluster_sort(cluster_sets_sorted.clusters[0])
    
    # compute without modifying original
    for i in range(n-1) : 
#        print("dealing now with")
#        print(i+1, "th no. of clusters", cluster_sets.sizes[i+1], "clusters")
        if method=="consistent" :
            cluster_sets_sorted = sort_next_clusters_for_colouring(cluster_sets, cluster_sets_sorted, i)
        elif method=="ascending" : 
            cluster_sets_sorted.clusters[i+1] = cluster_sort(cluster_sets_sorted.clusters[i+1])
            cluster_sets_sorted[i+1].clusters = cluster_sort(cluster_sets_sorted.clusters[i+1])
        else : 
            print("Unknown method")
    return cluster_sets_sorted    
    
    
def sort_next_clusters_for_colouring(cluster_sets, cluster_sets_sorted, i):
    
    # first we need the original clusters 
    # to determine which cluster was split going from i to i+1 clusters
    clusters_ref = cluster_sets.clusters[i] # i clusters
    clusters_up = cluster_sets.clusters[i+1] # i+1 clusters
    
    n_ref = cluster_sets.sizes[i]
    n_up = cluster_sets.sizes[i+1]
    
    # those labels that changed between ref and up
    diff = clusters_ref[clusters_ref!=clusters_up]
    
    if diff.size==0 : # empty array, no difference between i and i+1
#        print("pass, empty array")
        pass 
        
    else : # otherwise, sort
        # label of reference cluster that was split in up
        label_split = min(diff)
        
        # size of cluster before splitting (in ref)
        len_ref = len(clusters_ref[clusters_ref==label_split])
        # size of cluster after splitting (in up)
        len_up = len(clusters_up[clusters_up==label_split])
        
        # the cluster is split into two clusters: they have labels label_split and label_split+1. 
        # we keep the same colour for the bigger of the two, i.e. we assign it label label_split
        # the smaller one is assigned the new colour, i.e. label n_up
        # we need to shift the other labels accordingly
        clusters_ref_sorted = cluster_sets_sorted.clusters[i]
        clusters_up_sorted = cluster_sets_sorted.clusters[i+1]

        n_diff = n_up - n_ref # number of additional clusters between i and i+1
        
        if n_diff==1 :
            if len_up >= len_ref / 2 : # split cluster with old label is bigger than new label: old label stays unchanged
                clusters_up_sorted[clusters_up==label_split+1] = -1 # flag new cluster
                unchanged = (clusters_up_sorted!=-1)
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[clusters_up_sorted==-1] = n_up # assign new colour to new cluster
            else :
                clusters_up_sorted[clusters_up==label_split] = -1 # flag old cluster
                unchanged = (clusters_up_sorted!=-1)
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[clusters_up_sorted==-1] = n_up # assign new colour to old cluster
        else : # more than 1, then cluster is split into labels label_split, label_split+1, label_split+2, ...
            lens_new = [ len(clusters_up[clusters_up==label_split+j]) for j in range(n_diff+1)] 
            j_max = np.argmax(lens_new) - 1
            if j_max==-1 : # split cluster with old label is bigger than new label: old label stays unchanged
                for j in range(n_diff) :
                    clusters_up_sorted[clusters_up==label_split+1+j] = -1-j # flag new cluster
                unchanged = (clusters_up_sorted>0)
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                for j in range(n_diff) :
                    clusters_up_sorted[clusters_up_sorted==-1-j] = n_up - n_diff + 1 + j # assign new colour to new cluster
            else : # swap old cluster label_split with j_max
                clusters_up_sorted[clusters_up==label_split] = -label_split # flag old cluster
                for j in range(n_diff): 
                    clusters_up_sorted[clusters_up==label_split+1+j] = -label_split-1-j # flag new clusters
                unchanged = (clusters_up_sorted>0)
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[clusters_up_sorted==-label_split-1-j_max] = label_split
                for j in range(n_diff) :
                    if j!=j_max : 
                        clusters_up_sorted[clusters_up_sorted==-label_split-1-j] = n_up - n_diff + 1 + j # assign new colour to new cluster
                clusters_up_sorted[clusters_up_sorted==-label_split] = n_up - n_diff + 1 + j_max # assign new colour to old cluster
            
        # update clusters also in cluster_set instance
        cluster_sets_sorted[i+1].clusters = clusters_up_sorted
        
        # check that the clustering has not changed
        assert adjusted_rand_score(clusters_up_sorted, clusters_up)==1
    
    return cluster_sets_sorted    
