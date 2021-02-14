"""
This module provides helpers to show the graph inline
"""
import logging

import ipycytoscape


class GraphViewer():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, graph_model):
        self.graph_model = graph_model

    @classmethod
    def render(self, layout_name, graph_style, rank_dir):
        cytoscapeobj = ipycytoscape.CytoscapeWidget()
        cytoscapeobj.set_style(graph_style)
        cytoscapeobj.graph.add_graph_from_networkx(self.graph_model.G)

        cytoscapeobj.set_layout(name=layout_name, nodeSpacing=10, edgeLenghVal=10, rankDir=rank_dir)
        # klay, dagre, cola

        cytoscapeobj.set_tooltip_source('label')

        return cytoscapeobj
