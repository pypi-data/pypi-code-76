import networkx as nx
import numpy as np

from pge.init.classes.graph import SGraph


class Status(object):
    def __init__(self):
        self.node2com = dict([])
        self.total_weight = 0
        self.out_degrees = dict([])
        self.in_degrees = dict([])
        self.in_gdegrees = dict([])
        self.out_gdegrees = dict([])
        self.internals = dict([])
        self.loops = dict([])

    def copy(self):
        new_status = Status()
        new_status.node2com = self.node2com.copy()
        new_status.internals = self.internals.copy()
        new_status.in_degrees = self.in_degrees.copy()
        new_status.out_degrees = self.out_degrees.copy()
        new_status.in_gdegrees = self.in_gdegrees.copy()
        new_status.out_gdegrees = self.out_gdegrees.copy()
        new_status.total_weight = self.total_weight
        new_status.loops = self.loops

    def init(self, graph):
        count = 0
        self.total_weight = graph.size_edge()

        for node in graph.get_ids():
            self.node2com[node] = count
            out_deg = graph.count_out_degree(node, w="weight")
            in_deg = graph.count_in_degree(node, w="weight")
            self.out_degrees[count] = out_deg
            self.in_degrees[count] = in_deg
            self.in_gdegrees[node] = in_deg
            self.out_gdegrees[node] = in_deg

            self.loops[node] = graph.get_edge_data(node, node, "weight", bsc=0)
            self.internals[count] = self.loops[node]
            count += 1


__PASS_MAX = -1
__MIN = 0.0000001


def partition_at_level(dendrogram, level):
    partition = dendrogram[0].copy()
    for index in range(1, level + 1):
        for node, community in partition.items():
            partition[node] = dendrogram[index][community]
    return partition


def modularity(partition, graph):
    inc = dict([])
    deg = dict([])

    links = graph.size_edge()
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph.get_ids():
        com = partition[node]
        node_in_deg = graph.count_in_degree(node)
        for neighbor in graph.get_out_degrees(node):
            if partition[neighbor] == com:
                deg[com] = deg.get(com, 0.) + node_in_deg * graph.count_out_degree(neighbor)
                inc[com] = inc.get(com, 0.) + 1

    res = 0.
    for com in set(partition.values()):
        res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (links ** 2))
    return res


def best_partition_to(graph, starts=10, com_sz=1):
    part = {node: i for i, node in enumerate(graph.get_ids(stable=True))}
    mod = modularity(part, graph)

    for _ in range(starts):
        dendo = generate_dendrogram(graph)
        part_ = partition_at_level(dendo, len(dendo)-1)
        ln = len(set(part_.values()))
        if ln >= com_sz:
            mod_ = modularity(part_, graph)
            if mod_ > mod:
                mod = mod_
                part = part_
    return part, mod


def generate_dendrogram(graph):
    if graph.number_of_edges() == 0:
        part = dict([])
        for i, node in enumerate(graph.get_ids(stable=True)):
            part[node] = i
        return [part]

    current_graph = graph.clean_copy()
    status = Status()
    status.init(current_graph)
    status_list = list()
    __one_level(current_graph, status)

    new_mod = __modularity(status)
    partition = __renumber(status.node2com)
    status_list.append(partition)
    mod = new_mod
    current_graph = induced_graph(partition, current_graph)
    status.init(current_graph)

    while True:
        __one_level(current_graph, status)
        new_mod = __modularity(status)
        if new_mod - mod < __MIN:
            break
        partition = __renumber(status.node2com)
        status_list.append(partition)
        mod = new_mod
        current_graph = induced_graph(partition, current_graph)
        status.init(current_graph)
    return status_list


def induced_graph(partition, graph):
    ret = nx.DiGraph()
    ret.add_nodes_from(partition.values())

    for node1, node2 in graph.get_nx_graph().edges():
        wl = graph.get_edge_data(node1, node2, "weight", bsc=1)
        com1 = partition[node1]
        com2 = partition[node2]
        w_prec = ret.get_edge_data(com1, com2, {"weight": 0}).get("weight", 1)
        ret.add_edge(com1, com2, **{"weight": w_prec + wl})
    return SGraph(ret)


def __renumber(dictionary):
    values = set(dictionary.values())
    target = set(range(len(values)))

    if values == target:
        ret = dictionary.copy()
    else:
        renumbering = dict(zip(target.intersection(values), target.intersection(values)))
        renumbering.update(dict(zip(values.difference(target), target.difference(values))))
        ret = {k: renumbering[v] for k, v in dictionary.items()}
    return ret


def __one_level(graph, status):
    modified = True
    nb_pass_done = 0
    cur_mod = __modularity(status)
    new_mod = cur_mod

    while modified and nb_pass_done != __PASS_MAX:
        cur_mod = new_mod
        modified = False
        nb_pass_done += 1

        ids = graph.get_ids(stable=True)
        np.random.shuffle(ids)
        for node in ids:
            com_node = status.node2com[node]
            in_degc_totw = status.in_gdegrees.get(node, 0.) / status.total_weight
            out_degc_totw = status.out_gdegrees.get(node, 0.) / status.total_weight
            neigh_communities = __neighcom(node, graph, status)

            remove_cost = -  neigh_communities.get(com_node, 0) + (
                        status.out_degrees.get(com_node, 0.) - status.out_gdegrees.get(node, 0.)) * in_degc_totw + (
                        status.in_degrees.get(com_node, 0.) - status.in_gdegrees.get(node, 0.)) * out_degc_totw
            __remove(node, com_node, neigh_communities.get(com_node, 0.), status)

            best_com = com_node
            best_increase = 0

            for com, dnc in __randomize(neigh_communities.items()):
                incr = remove_cost + dnc - (status.out_degrees.get(com, 0.) * in_degc_totw + status.in_degrees.get(com, 0.) * out_degc_totw)
                if incr > best_increase:
                    best_increase = incr
                    best_com = com
            __insert(node, best_com, neigh_communities.get(best_com, 0.), status)
            if best_com != com_node:
                modified = True
        new_mod = __modularity(status)
        if new_mod - cur_mod < __MIN:
            break


def __neighcom(node, graph, status):
    weights = {}
    for neighbor in graph.get_out_degrees(node):
        if neighbor != node:
            edge_weight = graph.get_edge_data(node, neighbor, "weight", bsc=1)
            neighborcom = status.node2com[neighbor]
            weights[neighborcom] = weights.get(neighborcom, 0) + edge_weight
    return weights


def __remove(node, com, weight, status):
    status.in_degrees[com] = status.in_degrees.get(com, 0.) - status.in_gdegrees.get(node, 0.)
    status.out_degrees[com] = status.out_degrees.get(com, 0.) - status.out_gdegrees.get(node, 0.)
    status.internals[com] = status.internals.get(com, 0.) - weight - status.loops.get(node, 0.)
    status.node2com[node] = -1


def __insert(node, com, weight, status):
    status.node2com[node] = com
    status.in_degrees[com] = status.in_degrees.get(com, 0.) + status.in_gdegrees.get(node, 0.)
    status.out_degrees[com] = status.out_degrees.get(com, 0.) + status.out_gdegrees.get(node, 0.)
    status.internals[com] = status.internals.get(com, 0.) + weight + status.loops.get(node, 0.)


def __modularity(status):
    links = status.total_weight
    result = 0.
    if links > 0:
        for community in set(status.node2com.values()):
            in_degree = status.internals.get(community, 0.)
            degree = status.in_degrees.get(community, 0.) * status.out_degrees.get(community, 0.)
            result += (in_degree / links) - (degree / (links ** 2))
    return result


def __randomize(items):
    randomized_items = list(items)
    np.random.shuffle(randomized_items)
    return randomized_items
