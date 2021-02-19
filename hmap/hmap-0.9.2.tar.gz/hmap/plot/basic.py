'''This class offers basic plot Functions for generating nice heatmaps.
'''

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import pandas as pnd

##################
# Some color lists
colors = {}
colors["set22"] = ["#a6cee3", "#2076b4", "#b2df8a", "#33a02c", "#fb9a99",
                   "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#653d9a",
                   "#ffff99", "#d6604d", "#8dd3c7", "#ffffb3", "#bdbbdb",
                   "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#f8cce5",
                   "#d9d9d9", "#bc80bd"]
colors["xkcd"] = ["#812b9c", "#d0a6fd", "#00ad1f", "#c27ef6", "#8cf67d",
                  "#004fdf", "#29f9a2", "#6bbefd", "#ff84bf", "#0020aa",
                  "#8d89fe", "#683600", "#d4b06f", "#ffd2df", "#b08050",
                  "#ed0400", "#ff7200", "#c81477", "#690220", "#fffb19",
                  "#d1b003", "#000000"]

################
# Plot Functions
def Heatmap(table,
        cmap="Reds",
        distance_metric="correlation",
        linkage_method="complete",
        show_column_labels = False,
        show_row_labels = False,
        row_clustering = True,
        column_clustering = True,
        custom_row_clustering = None,
        custom_column_clustering = None,
        vmin = None,
        vmax = None,
        symmetric_color_scale = False,
        symmetry_point = 0,
        show_plot = True,
        optimal_row_ordering = True,
        optimal_col_ordering = True,
        ax = None):
    """Function that plots a two dimensional matrix as clustered heatmap.
    Sorting of rows and columns is done by hierarchical clustering.

    :param table: Two dimensional array containing numerical values to be
        clustered.
    :type table: Object of type :class:`pandas.DataFrame`
    :param cmap: Colormap used to produce color scale, defaults to "Reds".
    :type cmap: str, optional
    :param distance_metric: Distance metric used to determine distance
        between two vectors.The distance function can be either of
        'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'dice', 'euclidean', 'hamming', 'jaccard',
        'jensenshannon', 'kulsinski', 'mahalanobis', 'matching',
        'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
        'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule', defaults to
        'correlation'.
    :type distance_metric: str, optional
    :param linkage_method: methods for calculating the distance between the
        newly formed cluster u and each v. Possible methods are, 'single',
        'complete', 'average', 'weighted', and 'centroid', defaults to
        'complete'.
    :type linkage_method: str, optional
    :param show_column_labels: If true, show labels of columns, as defined
        in table, defaults to False.
    :type show_column_labels: bool, optional
    :param show_row_labels: If true, show labels of rows, as defined in
        table, defaults to False.
    :type show_row_labels: bool, optional
    :param row_clustering: If true, the rows a clustered according to
        distance_metric, and linkage_method, defaults to True.
    :type row_clustering: bool, optional
    :param column_clustering: If true, the columns are clustered according
        to distance_metric, and linkage_method, defaults to True.
    :type column_clustering: bool, optional
    :param custom_row_clustering: List of Row ids from table in the order
        they should appear in the heatmap. Only applies if row_clustering is
        False, defaults to None.
    :type custom_row_clustering: list, optional
    :param custom_column_clustering: List of column ids from table in the
        order they should appear in the heatmap. Only applies if
        column_clustering is False, defaults to None.
    :type custom_column_clustering: list, optional
    :param vmin: Minimal value of data_table, that has a color
        representation, defaults to None.
    :type vmin: float, optional
    :param vmax: Maximal value of data_table, that has a color
        representation, defaults to None.
    :type vmax: float, optional
    :param symmetric_color_scale: If true, vmin, and vmax will be set to
        have equal distance from symmetry point, defaults to False.
    :type symmetric_color_scale: bool, optional
    :param symmetry_point: Only used, when symmetric_color_scale is true. If
        symmetric_color_scale is true, and symmetry_point is not set,
        defaults to zero.
    :type symmetry_point: float, optional
    :param show_plot: If True, the heatmap will be shown on the given axis,
        else the function only returns the return values, defaults to True.
    :type show_plot: bool, optional
    :param optimal_row_ordering: If True, the rows will be ordered optimally
        with regards to the cluster separation. Be careuful: Can take a
        long time, depending on the number of rows, defaults to True.
    :type optimal_row_ordering: bool, optional
    :param optimal_col_ordering: If True, the columns will be ordered
        optimally with regards to the cluster separation. Be careuful:
        Can take a long time, depending on the number of columns, defaults
        to True.
    :type optimal_col_ordering: bool, optional
    :param ax: Axes instance on which to plot heatmap, defaults to None.
    :type ax: :class:`matplotlib.axes._subplots.AxesSubplot`,
        optional

    :return: Tuple containing: 1. column_names_reordered: List of
        column names after reordering as given as column names of table.
        2. row_names_reordered: List of row names after reordering as given
        as index names of table.
        3. vmin: Minimal value of table, that gets a color representation in
        heatmap.
        4. vmax: Maximal value of table, that gets a color representation in
        heatmap.
    :rtype: tuple
    """
    if(show_plot):
        ax = ax if ax is not None else plt.gca()

    # Sort column names
    column_names_reordered = list(table.columns)
    if(column_clustering):
        distance_matrix = pdist(table.T, metric=distance_metric)
        linkage_matrix = linkage(distance_matrix,
                                 metric=distance_metric,
                                 method=linkage_method,
                                 optimal_ordering=optimal_col_ordering)
        dendrogram_dict = dendrogram(linkage_matrix, no_plot=True)

        leaves = dendrogram_dict["leaves"]

        column_names = list(table.columns)
        column_names_reordered = [ column_names[i] for i in leaves ]
    elif(not(custom_column_clustering is None)):
        column_names_reordered = custom_column_clustering

    # Sort row names
    row_names_reordered = list(table.index)
    if(row_clustering):
        distance_matrix = pdist(table, metric=distance_metric)
        linkage_matrix = linkage(distance_matrix,
                                 metric=distance_metric,
                                 method=linkage_method,
                                 optimal_ordering=optimal_row_ordering)
        dendrogram_dict = dendrogram(linkage_matrix, no_plot=True)

        leaves = dendrogram_dict["leaves"]

        row_names = list(table.index)
        row_names_reordered = [ row_names[i] for i in leaves ]
    elif(not(custom_row_clustering is None)):
        row_names_reordered = custom_row_clustering

    # Override vmin and vmax if symmetric_color_scale is True
    if(symmetric_color_scale):
        if(vmin is None):
            vmin = np.min(np.min(table))
        if(vmax is None):
            vmax = np.max(np.max(table))
        abs_max = max([abs(vmin-symmetry_point), abs(vmax-symmetry_point)])

        vmin = symmetry_point - abs_max
        vmax = symmetry_point + abs_max

    # Plot heatmap
    if(show_plot):
        interpolation_method = "nearest"
        ncols = len(column_names_reordered)
        nrows = len(row_names_reordered)
    #    if(nrows > 1000):
    #        interpolation_method = "bilinear"
        img = ax.imshow(table.loc[row_names_reordered, column_names_reordered],
                        vmin=vmin,
                        vmax=vmax,
                        cmap=cmap,
                        aspect="auto",
                        origin="lower",
                        interpolation=interpolation_method)
        plt.ylim(-0.5, nrows-.5)
        plt.xlim(-0.5, ncols-.5)
        img.set_rasterized(True)

        # Plot column/ row labels
        if(show_column_labels):
            plt.xticks([ i for i in range(len(column_names_reordered))],
                 column_names_reordered, rotation=90, fontsize=7)
        else:
            plt.xticks([], [])
        if(show_row_labels):
            ax.yaxis.tick_right()
            plt.yticks([ i for i in range(len(row_names_reordered))],
                 row_names_reordered, fontsize=7)
        else:
            plt.yticks([], [])

    return column_names_reordered, row_names_reordered, vmin, vmax

def Dendrogram(table,
        distance_metric="correlation",
        linkage_method="complete",
        axis = 1,
        lw = 1.,
        n_clust = None,
        optimal_row_ordering=True,
        optimal_col_ordering=True,
        ax = None):
    """Function that plots a dendrogram on axis 0 (rows), or axis 1
    (columns) of a :class:`pandas.DataFrame`.

    :param table: Data matrix used to calculate dendrograms.
    :type table: :class:`pandas.DataFrame`
    :param distance_metric: Distance metric used to determine distance between
        two vectors. The distance function can be either of 'braycurtis',
        'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice',
        'euclidean', 'hamming', 'jaccard', 'jensenshannon', 'kulsinski',
        'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 
        'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule',
        defaults to 'correlation'.
    :type distance_metric: str, optional
    :param linkage_method: Methods for calculating the distance between the
        newly formed cluster u and each v. Possible methods are, 'single',
        'complete', 'average', 'weighted', and 'centroid', defaults to
        'complete'.
    :type linkage_method: str, optional
    :param axis: Axis of table used for plotting dendrogram (0 = rows,
        1 = columns), defaults to 1.
    :type axis: int, optional
    :param lw: Width of the lines (in points) defining the dengrogram, defaults
        to 1.
    :type lw: float, optional
    :param n_clust: Number of clusters in which the dendrogram should be cut.
        Note: Dendrogram cutting makes use of scipy.cluster.hierarchy.cut_tree
        function, defaults to None.
    :type n_clust: int, optional
    :param optimal_row_ordering: If True, the rows will be ordered optimally
        with regards to the cluster separation. Be careuful: Can take a long
        time, depending on the number of rows, defaults to True.
    :type optimal_row_ordering: bool, optional
    :param optimal_col_ordering: If True, the columns will be ordered optimally 
        with regards to the cluster separation. Be careuful: Can take a long
        time, depending on the number of columns, defaults to True.
    :type optimal_col_ordering: bool, optional
    :param ax: Axes n which to plot the dendrogram, defaults to None.
    :type ax: :class:`matplotlib.axes._subplots.AxesSubplot`

    :return: Tuple containing the following entries:
        1. Resulting dictionary from scipy.cluster.hierarchy.dendrogram
        function.
        2. linkage matrix, that is returned from
        scipy.cluster.hierarchy.linkage function
        3. dictionary containing the row_ids, (in case of axis = 0), or
        column_ids (in case of axis = 1) that are assigned to different
        clusters. Only makes sense if n_clust is not None.
    :rtype: dict
    """
    ax = ax if ax is not None else plt.gca()

    ids = None
    dendrogram_dict = None
    linkage_matrix = None
    cluster_dict = None
    color_threshold = 0
    if(axis == 0):
        ids = list(table.index)
        distance_matrix = pdist(table, metric=distance_metric)
        linkage_matrix = linkage(distance_matrix,
                                 metric=distance_metric,
                                 method=linkage_method,
                                 optimal_ordering=optimal_row_ordering)
        if(not n_clust is None):
            cluster_dict = {}
            color_threshold = linkage_matrix[-1*(n_clust-1), 2]
            grouping = cut_tree(linkage_matrix, n_clusters = n_clust)
            for i in range(len(grouping)):
                group = grouping[i, 0]
                if(not(group in cluster_dict)):
                    cluster_dict[group] = [ids[i]]
                else:
                    cluster_dict[group] += [ids[i]]
        with plt.rc_context({'lines.linewidth': lw}):
            dendrogram_dict = dendrogram(linkage_matrix,
                                         orientation="left",
                                         color_threshold = color_threshold)
    elif(axis == 1):
        ids = table.columns
        distance_matrix = pdist(table.T, metric=distance_metric)
        linkage_matrix = linkage(distance_matrix, metric=distance_metric,
                                 method=linkage_method,
                                 optimal_ordering=optimal_col_ordering)
        if(not n_clust is None):
            cluster_dict = {}
            color_threshold = linkage_matrix[-1*(n_clust-1), 2]
            grouping = cut_tree(linkage_matrix, n_clusters = n_clust)
            for i in range(len(grouping)):
                group = grouping[i, 0]
                if(not(group in cluster_dict)):
                    cluster_dict[group] = [ids[i]]
                else:
                    cluster_dict[group] += [ids[i]]

        with plt.rc_context({'lines.linewidth': lw}):
            dendrogram_dict = dendrogram(linkage_matrix,
                                         color_threshold = color_threshold)

    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.xticks([], [])
    plt.yticks([], [])

    return dendrogram_dict, linkage_matrix, cluster_dict

def Annotation(ids_sorted,
               annotation_df,
               annotation_col_id,
               axis = 1,
               color_list = colors["xkcd"],
               is_categorial=True,
               cmap = plt.cm.GnBu_r,
               color_dict = None,
               ax = None):
    """Function that plots annotations.

    :param ids_sorted: List of ids in the order in which the annotation shall be
        plotted.
    :type ids_sorted: list
    :param annotation_df: DataFrame containing grouping informatation for the
        ids for which the annotation shall be plotted. Columns: groups, rows:
        ids.
    :type annotation_df: :class:`pandas.DataFrame`
    :param annotation_col_id: Column id of the group in annotation_df, for which
        the annotation mshall be plotted.
    :type annotation_col_id: str
    :param axis: If 0, then the annotation is plotted vertically, i.e. for rows
        of a DataFrame. If 1, then the annotation is plotted horizontally, i.e.
        for columns of a DataFrame, defaults to 1
    :type axis: int, optional
    :param color_list: List of colors used to plot annotations, defaults to
        colors["xkcd"].
    :type color_list: list, optional
    :param is_categorial: Boolean parameter that defines if the colorscale shall
        be categorial, or continuous (e.g. age), defaults to True
    :type is_categorial: bool, optional
    :param cmap: ColorMap object, that defines the colormap used for plotting
        continuous variables, defaults to plt.cm.GnBu_r.
    :type cmap: :class:`matplotlib.colors.LinearSegmentedColormap`, optional
    :param color_dict: If is_categorial is True you can define colors for each
        category. These colors have to be given as a dict, where the key is the
        category and the value is the color code, defaults to None.
    :type color_dict: dict, optional
    :param ax: Axes on which to plot the annotation, defaults to None.
    :type ax: class:`matplotlib.axes._subplots.AxesSubplot`, optional

    :return: tuple containing the following two elements:
        1. True, if the annotation was categorial, False otherwise.
        2. If the first element is True, then it is a list containing one
        representative patch per group, along with the group name and the color
        representation of the group. If the first element is False, then it is
        a list, containing the
        :class:`matplotlib.colors.LinearSegmentedColormap` object, the min, and
        the max value from the floating value annotations.
    :rtype: tuple
    """
    ax = ax if ax is not None else plt.gca()

    max_val = None
    min_val = None
    if(not is_categorial):
        max_val = max(
            list(annotation_df.loc[ids_sorted,
                                   annotation_col_id].replace(np.nan, 0))
        )
        min_val = min(
            list(annotation_df.loc[ids_sorted,
                                   annotation_col_id].replace(np.nan, 0))
        )

    groups = list(set(annotation_df.loc[:, annotation_col_id]))

    groups_color_dict = {}

    if(not color_dict is None):
       groups_color_dict = color_dict
    else:
        color_counter = 0
        for group in groups:
            groups_color_dict[group] = color_list[color_counter %
                                                  len(color_list)]
            color_counter += 1

    idx_counter = 0
    patch_list = []
    if(axis == 1):
        groups_list = []
        for id_current in ids_sorted:
            color = None
            if(is_categorial):
                color = groups_color_dict[annotation_df.loc[id_current,
                                                        annotation_col_id]]
            else:
                value = annotation_df.loc[id_current, annotation_col_id]
                print(type(value))
                color = "w"
                if(not(np.isnan(value))):
                    color = cmap((float(value)-min_val)/
                                 (float(max_val)-min_val))
            patch = Rectangle((float(idx_counter), 0.),
                              1,
                              1,
                              color=color,
                             capstyle="butt",
                             edgecolor=None,
                             linewidth=0)
            ax.add_patch(patch)
            idx_counter += 1

            if(not annotation_df.loc[id_current, annotation_col_id] in
               groups_list):
                patch_list += [[patch,
                                annotation_df.loc[id_current,
                                                  annotation_col_id],
                                color ]]
                groups_list += [annotation_df.loc[id_current,
                                                  annotation_col_id]]
        plt.xlim(0, len(ids_sorted))
        plt.ylim(0, 1)
        ax.yaxis.set_label_position("right")
        plt.ylabel(annotation_col_id, rotation=0, verticalalignment="center",
                   horizontalalignment="left", fontsize=7)
    elif(axis == 0):
        groups_list = []
        for id_current in ids_sorted:
            color = None
            if(is_categorial):
                color = groups_color_dict[annotation_df.loc[id_current,
                                                        annotation_col_id]]
            else:
                value = annotation_df.loc[id_current, annotation_col_id]
                color = cmap((float(value)-min_val)/(float(max_val)-min_val))
            patch = Rectangle((0., float(idx_counter)),
                              1,
                              1,
                              color=color,
                             capstyle="butt",
                             edgecolor=None,
                             linewidth=0)
            ax.add_patch(patch)
            idx_counter += 1

            if(not annotation_df.loc[id_current, annotation_col_id] in
               groups_list):
                patch_list += [[patch,
                                annotation_df.loc[id_current,
                                                  annotation_col_id],
                                color ]]
                groups_list += [annotation_df.loc[id_current,
                                                  annotation_col_id]]
        plt.ylim(0, len(ids_sorted))
        plt.xlim(0, 1)
        plt.xlabel(annotation_col_id, rotation=90, verticalalignment="top",
                   horizontalalignment="center", fontsize=7)

    ax.axes.spines["top"].set_visible(False)
    ax.axes.spines["bottom"].set_visible(False)
    ax.axes.spines["left"].set_visible(False)
    ax.axes.spines["right"].set_visible(False)
    plt.xticks([] ,[])
    plt.yticks([] ,[])

    if(not is_categorial):
        patch_list = [cmap, min_val, max_val]

    return [is_categorial, patch_list]

def ColorScale(table,
        cmap="Reds",
        symmetric_color_scale = True,
        symmetry_point=0.,
        vmin = None,
        vmax = None,
        ax = None):
    """Function that plots the color scale of values inside a dataframe.

    :param table: Table containing numerical values.
    :type table: :class:`pandas.DataFrame`
    :param cmap: Colormap used to produce color scale, defaults to "Reds".
    :type cmap: str, optional
    :param symmetric_color_scale: If true, vmin, and vmax will be set to have
        equal distance from symmetry point, defaults to True.
    :type symmetric_color_scale: bool, optional
    :param symmetry_point: Only used, when symmetric_color_scale is true. If
        symmetric_color_scale is true, and symmetry_point is not set, defaults
        to zero.
    :type symmetry_point: float, optional
    :param vmin: Minimal value of data_table, that has a color representation,
        defaults to None.
    :type vmin: float, optional
    :param vmax: Maximal value of data_table, that has a color representation,
        defaults to None.
    :type vmax: float, optional
    :param ax: Axes instance on which to plot the color scale, defaults to None.
    :type ax: class:`matplotlib.axes._subplots.AxesSubplot`, optional

    :returns: Min. and max value displayed on color scale
    :rtype: tuple
    """
    ax = ax if ax is not None else plt.gca()

    # Calculate min and max value from table
    if(vmin is None):
        vmin = np.min(np.min(table))
    if(vmax is None):
        vmax = np.max(np.max(table))

    # Calculate maximal distance to symmetry point
    max_dist = max([np.abs(vmax-symmetry_point), np.abs(vmin-symmetry_point)])

    # Calculate x axis extensions
    xlim = [0, 256]
    if(symmetric_color_scale):
        xlim = [(0.5-(np.abs(vmin-symmetry_point)/max_dist)*.5)*256,
            (.5+np.abs(np.abs(vmax-symmetry_point)/max_dist)*.5)*256]

    # Plot color scale
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    plt.imshow(gradient, cmap=cmap, aspect="auto")
    plt.xlim(xlim)

    plt.xticks(xlim, [round(vmin, 2), round(vmax, 2)], fontsize=6)
    ax.xaxis.set_ticks_position('top')
    plt.title("Values", fontsize=7)
    plt.yticks([], [])

    return vmin, vmax

def Legends(patch_list_dict,
            annotation_ids = None,
            ax = None):
    """Function that plots Legends based on pathc lists from Annotation
    function.

    :param patch_list_dict: A dictionary, storing patches used for legend
        plotting. The key is the name of the Annotation, and the value is a list
        of 2 elements. The first element is a boolean value, defining if the
        annotation was catgorial (True) or non-categorial (False). The second
        element is in the case of categorial annotations the patch list, and in
        the case of non categorial annotations the cmap used, as well as the min
        and the max values.
    :type patch_list_dict: dict
    :param annotation_ids: List of annotation ids, for which the Legend shall
        be plotted. Legends will be plotted in the same order as given in
        annotation_ids list, defaults to None.
    :type annotation_ids: list, optional
    :param ax: Axes instance on which to plot the legends, defaults to None.
    :type ax: class:`matplotlib.axes._subplots.AxesSubplot`, optional

    :return: Nothing to be returned.
    :rtype: None
    """
    annotation_ids = (annotation_ids if
                      annotation_ids is not None else
                      patch_list_dict.keys())
    ax = ax if ax is not None else plt.gca()

    plt.xlim([0, 1.])
    plt.ylim([0, 1.])

    x = 0
    y = 1
    x_max = 0

    # Get width and height of figure
    fig = plt.gcf()
    box = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = box.width*25.4, box.height*25.4

    # calculate width and height of colorscales as ratios of axis width, and
    # height
    color_scale_height = 5.*(1./height)
    color_scale_width = 20.*(1./width)

    for annotation_id in annotation_ids:
        # If annotation data is categorial
        if(patch_list_dict[annotation_id][0]):
            patch_list = patch_list_dict[annotation_id][1]
            legend = ax.legend([p[0] for p in patch_list],
                               [p[1] for p in patch_list],
                               title=annotation_id,
                               title_fontsize=7,
                               fontsize=6,
                               loc = "upper left",
                               bbox_to_anchor=(x, y),
                               frameon = False)
            plt.draw()
            p = legend.get_window_extent().inverse_transformed(ax.transAxes)
            if(p.p0[1] < 0):
                legend.remove()
                y = 1
                x = x_max
                legend = ax.legend([p[0] for p in patch_list],
                               [p[1] for p in patch_list],
                               title=annotation_id,
                               title_fontsize=7,
                               fontsize=6,
                               loc = "upper left",
                               bbox_to_anchor=(x, y),
                               frameon=False)
                plt.draw()
                p = legend.get_window_extent().inverse_transformed(ax.transAxes)

            if(p.p1[0] > x_max):
                x_max = p.p1[0]+2.*(1./width)
            y = p.p0[1]
            ax.add_artist(legend)
            ax.axis("off")
        else:
            patch_list = patch_list_dict[annotation_id][1]
            img = ax.imshow([[0, 1], [0, 1]],
                        cmap = patch_list[0],
                        interpolation = 'bicubic',
                        extent=[x, x+color_scale_width, y, y-color_scale_height],
                        vmin=0
                      )
            p = img.get_window_extent().inverse_transformed(ax.transAxes)
            if(p.y1-6.*(1./height) <= 0):
                img.remove()
                y = 1.-4.*(1./height)
                x = x_max
                img = ax.imshow([[0, 1], [0, 1]],
                        cmap = patch_list[0],
                        interpolation = 'bicubic',
                        extent=[x, x+color_scale_width, y, y-color_scale_height],
                        vmin=0
                      )
                p = img.get_window_extent().inverse_transformed(ax.transAxes)

            # Plot annotation ID
            plt.text(x+color_scale_width/2.,
                     y,
                     annotation_id,
                     fontsize=7,
                     verticalalignment="bottom",
                     horizontalalignment="center")
            plt.text(x,
                     y-((.6)*(1./height)+color_scale_height),
                     str(round(patch_list[1], 3)),
                     verticalalignment="top",
                     horizontalalignment="left",
                     fontsize=6)
            plt.text(x+color_scale_width,
                     y-((.6)*(1./height)+color_scale_height),
                     str(round(patch_list[2], 3)),
                     verticalalignment="top",
                     horizontalalignment="right",
                     fontsize=6)

            if(p.x1 > x_max):
                x_max = p.x1+2.*(1./width)
            y = p.y1-6.*(1./height)
            ax.set_aspect('auto')
            ax.axis("off")
