from IPython.display import Image
import networkx as nx
import pygraphviz as pgv


def create_rule_graph(rules):
    G = nx.DiGraph()

    for node in rules:
        G.add_node(node, rule=rules[node]["rule"])

    for node in G.nodes:
        if node[:-2] in G.nodes:
            lbl = "score: {:f}\nsize: {}".format(
                rules[node]["score"], rules[node]["size"]
            )
            G.add_edge(node[:-2], node, label=lbl)

    lbl = "score: {:f}\nsize: {}".format(
        rules[(0, "IN", 0, "IN")]["score"], rules[(0, "IN", 0, "IN")]["size"]
    )
    G.add_edge((0, "IN", 0, "IN"), (0, "IN", 0, "IN"), label=lbl)

    return G


def visualize_rule_graph(G):
    nx.nx_agraph.write_dot(G, "rules.dot")
    G = pgv.AGraph("rules.dot", directed=True)

    G.node_attr["shape"] = "box"
    G.edge_attr["color"] = "red"

    G.layout("dot")
    G.draw("graph.png")

    return Image(filename="graph.png")


def visualize_rule_tree(rule_tree):
    return visualize_rule_graph(create_rule_graph(rule_tree))
