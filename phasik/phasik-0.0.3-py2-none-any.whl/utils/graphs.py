import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def create_graph_from_interactions(filename, sheet, source, target):
    """Create a networkx.Graph from an excel sheet describing edges

    Parameters
    ----------
    filename : str 
        Path to the excel file
    sheet : str 
        Name of the sheet within the excel file
    source : str 
        Name of the column containing the source nodes
    target : str 
        Name of the column containing the target nodes
        
    Returns
    -------
    graph : networkx.Graph
    """

    interactions = pd.read_excel(filename, sheet_name=sheet)
    graph = nx.from_pandas_edgelist(interactions, source, target)
    return graph


def draw_graph(graph, ax=None, label_nodes=True, color='mediumseagreen'):
    """Basic graph drawing function

    Parameters
    ----------
    graph : networkx.Graph 
        
    ax : matplotlib.Axes, optional
        Axes on which to draw the graph
    label_nodes : bool, optional 
        Whether to label the nodes or just leave them as small circles (default True)
    color : str, optional
        Color to use for the graph nodes and edges (default mediumseagreen)
        
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    layout = graphviz_layout(graph, prog='neato')
    _draw_graph(graph, layout, ax, label_nodes, color)


def _draw_graph(graph, layout, ax, label_nodes, color):
    # PRIVATE function for the parts of graph drawing that are common to multiple methods
    params = standard_node_params(color)
    nx.draw_networkx_nodes(graph, ax=ax, pos=layout, **params)
    nx.draw_networkx_edges(graph, ax=ax, pos=layout, **params)
    if label_nodes:
        nx.draw_networkx_labels(graph, ax=ax, pos=layout, **params)


def highlight_subgraphs(graphs, colors, ax=None, label_nodes=True):
    """Draw multiple nested subgraphs on the same axes

    Parameters
    ----------
    graphs : list of networkx.Graph
        
    colors : list of str
        List of colours, one for each of the graphs in 'graphs'
    ax : matplotlib.Axes, optional
        Axes to plot on
    label_nodes : bool, optional 
        Whether or not to label the graph nodes or leave them as circles
        
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    layout = graphviz_layout(graphs[0], prog='neato')
    for graph, color in zip(graphs, colors):
        _draw_graph(graph, layout, ax, label_nodes, color)


def graph_size_info(graph):
    """Return basic size info on about graph"""
    return f"{len(graph)} nodes and {len(graph.edges)} edges"


def standard_node_params(color):
    return {
        'node_color': color,
        'edge_color': color,
        'font_color': 'k',
        'font_size' : 'medium',
        'edgecolors': 'k',
        'node_size': 100,
        'bbox': dict(facecolor=color, edgecolor='black', boxstyle='round, pad=0.2', alpha=1)
    }
