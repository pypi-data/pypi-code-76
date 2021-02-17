#!/usr/bin/env python3

"""
|===========================|
| Modelisation du cluster   |
| de travail par un graphe. |
|===========================|

* Cela permet de modeliser et de representer
les connections qu'il peut y avoir entre
les differentes machines d'un reseau.
* Cette partie permet de pouvoir optimiser la
repartition des taches en se basant sur la theorie
des graphes.
* De facon generale, avoir une information precise
des machines environante est necessaire pour
pouvoir faire du travail en grappe.
"""

from .basegraph import BaseGraph


__all__ = ["segment", "vertex", "Graph", "BaseGraph", "clustergraph"]


class Graph(BaseGraph):
    """
    |===================================|
    | Graphe abstrait mathematique avec |
    | le plus de proprietes possible.   |
    |===================================|


    Example
    -------
    >>> from raisin.graph import *
    >>> g1 = Graph() # graphe modifiable car pas d'arguments
    >>> g1
    Graph()
    >>> g1.add_edges((0, 2), (0, 3), (1, 2))
    >>> g1
    Graph({Edge(Vertex(n=0), Vertex(n=2), n=0), ..., Edge(Vertex(n=1), Vertex(n=2), n=2)})
    >>> g1 = Graph(g1) # graphe fige, mais avec plus de methodes
    >>> g1
    BipartiteGraph({Edge(Vertex(n=0), Vertex(n=2), n=0), ..., Edge(Vertex(n=1), Vertex(n=2), n=2)})
    >>>
    """
    def __new__(cls, *args, **kwargs):
        """
        |========================================|
        | Constructeur qui retourne une instance |
        | de graphe la plus evoluee possible.    |
        |========================================|

        * L'assemblage est fait par une metaclasse.
        """
        graph = super(BaseGraph, cls).__new__(cls)
        graph.__init__(*args, **kwargs)

        if graph: # Seulement si le graphe est non-vide:
            name, bases, methodes = "", [], {} # Pour la metaclasse.

            if graph.is_complete():
                from .specifics import completegraph
                name += "Complete"
                bases.append(completegraph.CompleteGraph)
            if graph.is_bipartite():
                from .specifics import bipartitegraph
                name += "Bipartite"
                bases.append(bipartitegraph.BipartiteGraph)
            if graph.is_arborescence():
                from .specifics import arborescencegraph
                name += "Arborescence"
                bases.append(arborescencegraph.ArborescenceGraph)

            if name: # Si le graphe a des proprietes particulieres.
                name += "Graph"
                from . import basegraph
                methodes["__init__"] = basegraph.FrozenGraph.__init__
                methodes["__delitem__"] = basegraph.FrozenGraph.__delitem__
                methodes["add_segment"] = basegraph.FrozenGraph.add_segment
                methodes["add_arrow"] = basegraph.FrozenGraph.add_arrow
                methodes["add_edge"] = basegraph.FrozenGraph.add_edge
                methodes["add_segments"] = basegraph.FrozenGraph.add_segments
                methodes["add_arrows"] = basegraph.FrozenGraph.add_arrows
                methodes["add_edges"] = basegraph.FrozenGraph.add_edges
                methodes["add_vertex"] = basegraph.FrozenGraph.add_vertex
                methodes["add_vertices"] = basegraph.FrozenGraph.add_vertices
                methodes["del_segment"] = basegraph.FrozenGraph.del_segment
                methodes["del_arrow"] = basegraph.FrozenGraph.del_arrow
                methodes["del_edge"] = basegraph.FrozenGraph.del_edge
                methodes["del_vertex"] = basegraph.FrozenGraph.del_vertex
                graph = type(name, tuple(bases), methodes)(graph)
            
        return graph
