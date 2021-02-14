"""
This module provides helpers to setup the graph network
"""
import logging

import ipycytoscape
import networkx as nx


class CustomNode(ipycytoscape.Node):
    def __init__(self, id, label, classes):
        super().__init__()
        self.data['id'] = id
        self.data['label'] = label
        self.data['role'] = None
        self.classes = classes


class LevelNode(CustomNode):
    def __init__(self, properties, category):
        super().__init__(properties['id'], properties['label'], f'{category} level')
        self.data['category'] = category
        self.data['group'] = 'level'


class ResourceNode(CustomNode):
    def __init__(self, properties, category):
        super().__init__(properties['id'], properties['label'], f'{category} resource')
        self.data['category'] = category
        self.data['group'] = 'resource'


class InputNode(ResourceNode):
    def __init__(self, properties, category, connect_id_name):
        super().__init__(properties, f'{category} input')
        self.data['category'] = category  # override FIXMZ role in concat
        self.data['role'] = 'input'
        self.data['connect_id'] = properties[connect_id_name]


class OutputNode(ResourceNode):
    def __init__(self, properties, category, connect_id_name):
        super().__init__(properties, f'{category} output')
        self.data['category'] = category   # override FIXMZ role in concat
        self.data['role'] = 'output'
        self.data['connect_id'] = properties[connect_id_name]


class GraphModel():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, G):
        self.G = G

    @classmethod
    def remove_category(self, category):
        self.logger.debug(f"removing nodes having category {category}")
        selected_nodes = [node[0]
                          for node in self.G.nodes(data=True)
                          if node[0].data['category'] == category]
        self.logger.debug(f'selected_nodes {selected_nodes}')
        self.G.remove_nodes_from(selected_nodes)

    @classmethod
    def aggregate_level(self, levels_list):
        # TODO cannot remove first level - need to be aware of the schema
        self.logger.debug(f"aggregating on level category {levels_list}")

        def is_level(node): return node.data['group'] == 'level'
        def should_keep(node): return node.data['category'] in levels_list

        # detect nodes that should be replaced by their parent
        # data=True
        replacements = []
        for node in self.G.nodes():
            self.logger.debug(f"{node.classes} {node.data['id']}")
            if is_level(node) and not should_keep(node):
                self.logger.debug(f"{node.classes} {node.data['id']}")
                parent_node = None
                current_node = node
                while parent_node is None:
                    for pred_node in self.G.predecessors(current_node):
                        if is_level(pred_node):
                            current_node = pred_node
                            if should_keep(pred_node):
                                parent_node = pred_node
                                replacements.append((node, parent_node))

        self.logger.debug(f"adding {len(replacements)} nodes")
        for (node, parent) in replacements:
            # inputs
            for pred_node in self.G.predecessors(node):
                if not is_level(pred_node):
                    self.G.add_edge(pred_node, parent)
            # other resources
            for next_node in self.G.successors(node):
                if not is_level(next_node):
                    self.G.add_edge(parent, next_node)

        self.logger.debug("will remove extra levels")
        selected_nodes = [node[0]
                          for node in self.G.nodes(data=True)
                          if is_level(node[0]) and not should_keep(node[0])]
        self.logger.debug(f'selected_nodes {selected_nodes}')
        self.G.remove_nodes_from(selected_nodes)

    @classmethod
    def aggregate_level_old(self, levels_list):
        self.logger.debug(f"aggregating on level category {levels_list}")

        ref = None

        jumps = []
        for l0 in self.G.nodes():
            self.logger.debug(f"{l0.classes} {l0.data['id']}")
            ref = l0 if l0.data['category'] in levels_list else ref
            for l1 in self.G.successors(l0):
                self.logger.debug(f"--> {l1.classes} {l1.data['id']}")
                ref = l1 if l1.data['category'] in levels_list else ref
                for l2 in self.G.successors(l1):
                    self.logger.debug(f"----> {l2.classes} {l2.data['id']}")
                    ref = l2 if l2.data['category'] in levels_list else ref
                    for res in self.G.successors(l2):
                        self.logger.debug(f"------> {res.classes} {res.data['id']}")
                        jumps.append((ref, res))

        self.logger.debug(f"adding {len(jumps)} edges")
        [self.G.add_edge(ref, res) for (ref, res) in jumps]

        self.logger.debug("will remove other levels")

        def is_level(node): return node[0].data['group'] == 'level'
        def should_ignore(node): return node[0].data['category'] not in levels_list

        selected_nodes = [node[0]
                          for node in self.G.nodes(data=True)
                          if is_level(node) and should_ignore(node)]
        self.logger.debug(f'selected_nodes {selected_nodes}')
        self.G.remove_nodes_from(selected_nodes)

    @classmethod
    def merge_connection(self, left_name, right_name, connect_id_name):
        # FIXME replace with schema identification and connect_id_name -> connection_name
        self.logger.debug(f"merging left and right side of the connection {connect_id_name}")

        merges = []
        for node in self.G.nodes():
            self.logger.debug(f"{node.classes} {node.data['id']}")
            if node.data['category'] == left_name:
                for paired_node in self.G.successors(node):
                    self.logger.debug(f"--> {paired_node.classes} {paired_node.data['id']}")
                    if paired_node.data['category'] == right_name:
                        connect_id = paired_node.data['connect_id']
                        merges.append((node, paired_node))

        self.logger.debug(f"adding {len(merges)} nodes")
        for (left, right) in merges:
            connect_id = left.data['connect_id']
            flight = ResourceNode({'id': connect_id, 'label': connect_id}, connect_id_name)
            self.G.add_node(flight)
            for previous_node in self.G.predecessors(left):
                self.G.add_edge(previous_node, flight)
            for next_node in self.G.successors(right):
                self.G.add_edge(flight, next_node)

        self.logger.debug("will remove extra categories")
        self.remove_category(left_name)
        self.remove_category(right_name)

    @classmethod
    def fold_category(self, category, hide_inner=False):
        self.logger.debug(f"folding category {category}")

        merges = []
        for node in self.G.nodes():
            if node.data['category'] == category:
                self.logger.debug(f"{node.classes} {node.data['id']}")
                merges.append(node)

        self.logger.debug(f"adding {len(merges)} edges")
        for node in merges:
            for previous_node in self.G.predecessors(node):
                for next_node in self.G.successors(node):
                    is_accepted = previous_node != next_node or not hide_inner
                    if is_accepted:
                        self.G.add_edge(previous_node, next_node)

        self.logger.debug("will remove extra category")
        self.remove_category(category)

    @classmethod
    def summary(self):
        count_by_class = {}
        for node in self.G.nodes(data=True):
            if not node[0].classes in count_by_class:
                count_by_class[node[0].classes] = 0
            count_by_class[node[0].classes] += 1
        return count_by_class

    @classmethod
    def pretty_print(self):
        lines = []
        lines.append('Nodes:')
        for n in self.G.nodes(data=True):
            lines.append(f"{n[0].classes} - {n[0].data['label']}")
        lines.append('')
        lines.append('Edges:')
        for e in self.G.edges:
            lines.append(f"{e[0].classes} {e[0].data['id']} -> {e[1].classes} {e[1].data['id']}")
        return lines

# TODO pattern builder
class GraphBuilder():
    logger = logging.getLogger(__name__)
    # TODO unit tests

    @classmethod
    def __init__(self):
        self.node_class = {}
        self.G = nx.DiGraph()

    @classmethod
    def with_types(self, node_class_mapping):
        self.node_class = node_class_mapping
        return self

    @classmethod
    def with_model(self, model):
        self.model = model
        return self

    @classmethod
    def render(self):
        self.logger.debug('render graph data')
        self.__build_from_schema()
        return GraphModel(self.G)

    #  basic operations

    @classmethod
    def __build_from_schema(self):
        self.logger.info('adding nodes from levels')
        self.add_nodes_from_levels()
        for key in self.model.schema.resources_keys():
            self.logger.info(f'adding resource nodes {key}')
            self.add_nodes_from_resource(key)
        for left, right in self.model.schema.connections_pairs():
            # FIXME no match - data id contains In or Out
            self.logger.info(f'adding connection {left} {right}')
            df = self.model.resource_dataset(right)
            left_definition = self.model.schema.resource_definition(left)
            right_definition = self.model.schema.resource_definition(right)
            # FIXME connect_id_name magic string
            # TODO insulate connection management and base class
            self.add_edges_from(df, left, right,
                                on_target_key=left_definition['connect_id_name'],
                                on_source_key=right_definition['connect_id_name'],
                                graph_key='connect_id')

    @classmethod
    def register_node_type(self, category, class_name, color='black'):
        # FIXME unused color
        self.node_class[category] = class_name

    @classmethod
    def add_nodes_from_levels(self):
        keys = self.model.schema.levels_keys()
        dfs = self.model.levels_datasets
        nb = len(keys)

        self.logger.info('creating nodes for each level dataset')
        for i in range(0, nb):
            self.add_nodes_from(dfs[i], keys[i])

        self.logger.info('creating edges between levels')
        for i in range(1, nb):
            self.add_edges_from(dfs[i], keys[i-1], keys[i])

    @classmethod
    def add_nodes_from_resource(self, resource_key):
        keys = self.model.schema.levels_keys()
        df = self.model.resource_dataset(resource_key)

        self.logger.info(f'creating nodes for resource dataset {resource_key}')
        self.add_nodes_from(df, resource_key)

        self.logger.info('creating edges between lower level and resource')
        self.logger.debug(f'lower level {keys[-1]} resource_key {resource_key}')
        role = self.model.schema.resource_definition(resource_key)['role']
        self.logger.debug(f'role={role}')
        preceding = (role == 'INPUT')  # FIXME magic string
        # FIXME juste inverser le passage des parametres
        self.add_edges_from(df, keys[-1], resource_key, preceding=preceding)

    @classmethod
    def add_nodes_from(self, df, category):
        wf_records = df.to_dict('records')
        ctor = self.node_class.get(category)
        wf_nodes = [ctor(row) for row in wf_records]
        self.logger.debug(f'adding {len(wf_nodes)} as {category}')
        self.G.add_nodes_from(wf_nodes)

    @classmethod
    def add_edges_from(self, target_df, source_category, target_category,
                       preceding=False, graph_key='id',
                       on_source_key='id_parent', on_target_key='id'):
        source_nodes_by_id = {n.data[graph_key]: n for n in self.G.nodes() if source_category in n.classes}
        target_nodes_by_id = {n.data[graph_key]: n for n in self.G.nodes() if target_category in n.classes}
        self.logger.debug(f'preceding={preceding}')
        if preceding:
            edge_label = f'{target_category}_{source_category}'
        else:
            edge_label = f'{source_category}_{target_category}'
        self.logger.debug(f'edge_label={edge_label}')

        def add_edge(row):
            id_source = row[on_source_key]
            id_target = row[on_target_key]
            self.logger.debug(f'{id_source} -> {id_target}')
            self.logger.debug(f'{source_nodes_by_id[id_source]} -> {target_nodes_by_id[id_target]}')
            self.logger.debug(f'preceding={preceding}')
            if preceding:
                self.G.add_edge(target_nodes_by_id[id_target], source_nodes_by_id[id_source], label=edge_label)
            else:
                self.G.add_edge(source_nodes_by_id[id_source], target_nodes_by_id[id_target], label=edge_label)

        target_df.apply(add_edge, axis=1)
