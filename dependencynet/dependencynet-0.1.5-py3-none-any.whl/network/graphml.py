

"""
This module provides helpers to convert the graph into GraphML
"""
import logging

import pyyed
import codecs


class GraphMLConverter():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, graph_model, graph_style, schema):
        self.graph_model = graph_model
        self.graph_style = graph_style
        self.schema = schema
        self.graphml_network = self.__to_graphml()

    @classmethod
    def save(self, filename):
        with codecs.open(filename, 'w', 'utf-8') as fp:
            graph = self.graphml_network.get_graph()
            fp.write(graph)
            self.logger.info(f'file saved under {filename}')

    @classmethod
    def __to_graphml(self):
        g = pyyed.Graph()

        colors = {}
        shapes = {}
        widths = {}
        kl = self.schema.levels_keys()
        kr = self.schema.resources_keys()
        for element in self.graph_style:
            if element['selector'] == 'node':
                for k in kl:
                    widths[k] = '80'  # element['css']['width']
                for k in kr:
                    widths[k] = '80'  # element['css']['width']
            elif element['selector'] == 'node.level':
                for k in kl:
                    shapes[k] = element['css']['shape']
            elif element['selector'] == 'node.resource':
                for k in kr:
                    shapes[k] = element['css']['shape']
            elif element['selector'].startswith('node.'):
                k = element['selector'].split('.')[1]
                colors[k] = element['css']['background-color']

        self.logger.debug(colors)
        self.logger.debug(shapes)
        self.logger.debug(widths)

        for node in self.graph_model.G.nodes(data=True):
            n = node[0]
            category = n.data['category']
            g.add_node(n.data['id'],
                       label=n.data['label'],
                       shape=shapes[category],
                       shape_fill=colors[category],
                       font_size='8',
                       font_style='bold',
                       width=widths[category],
                       height='30')

        for n1, n2 in self.graph_model.G.edges():
            g.add_edge(n1.data["id"], n2.data["id"], width="1.0", color="#888888",
                       arrowhead="standard", arrowfoot="none")

        return g
