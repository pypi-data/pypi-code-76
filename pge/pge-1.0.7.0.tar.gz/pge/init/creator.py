import numpy as np
import networkx as nx

from scipy.stats import powerlaw

from pge.init.classes.graph import SGraph
from pge.init.add import actual


class Creator:
    @staticmethod
    def tbt(nm, alpha, beta):
        ind_d = np.around(1/powerlaw.rvs(alpha, size=nm))
        out_d = np.around(1/powerlaw.rvs(beta, size=nm))

        zv = np.sum(np.subtract(ind_d, out_d))
        k = 1 - min([0.5, 1 - alpha ** -1, 1 - beta ** -1]) / 2
        while np.abs(zv) > nm ** k:
            i_s = np.random.choice(nm, min(int(np.abs(zv)), nm), replace=False)

            for i in i_s:
                if zv < 0:
                    ind_d[i] = ind_d[i] + 1
                else:
                    out_d[i] = out_d[i] + 1
            zv = np.sum(np.subtract(ind_d, out_d))

        gr = SGraph(nx.DiGraph())
        gr.add_nodes(np.arange(nm))

        for i in np.arange(nm):
            if ind_d[i] == 0:
                continue
            i_s = np.setdiff1d(np.arange(nm), i)
            np.random.shuffle(i_s)

            for j in i_s:
                if out_d[int(j)] > gr.count_out_degree(j):
                    gr.add_edge(j, i)

        return gr

    @staticmethod
    def make_from_data(network, pre="../", nm=None, sigma=None):
        path = pre + "pge/samples/networks/web-"
        if network == "BS":
            path += "BerkStan.txt"
        elif network == "S":
            path += "Stanford.txt"
        elif network == "G":
            path += "Google.txt"
        else:
            path = network
        gr = nx.read_edgelist(path, create_using=nx.DiGraph())
        print("loaded")

        if nm is None:
            res = SGraph(gr)
        else:
            choiced = np.random.choice(gr.nodes())
            res = Creator.create_subgraph(gr, choiced, nm)

        actual(res, sigma)
        print("attrs added")
        return res

    @staticmethod
    def simple_graph(network, pre="../", typ=nx.DiGraph, dl=" ", clean=False):
        path = pre + "pge/samples/networks/web-"
        if network == "BS":
            path += "BerkStan.txt"
        elif network == "S":
            path += "Stanford.txt"
        elif network == "G":
            path += "Google.txt"
        else:
            path = network
        res = nx.read_edgelist(path, create_using=typ(), delimiter=dl)

        sub = max(nx.connected_components(res), key=len)
        res = SGraph(res).subgraph(sub)

        if clean:
            res.del_attrs(["pos"])
        return res

    @staticmethod
    def fire_forest(p_f, p_r, n):
        graph = nx.DiGraph()
        graph.add_nodes_from(np.arange(n))
        graph = SGraph(graph)

        for i in np.arange(1, n):
            add_n = np.array([])
            if i - 1 == 0:
                ws = np.array([0])
            else:
                ws = []  # ws = np.array([rand_int(mn=0, mx=i - 1, sz=1)])

            while ws.size > 0:
                n_ws = np.array([])
                for w in ws:
                    x = graph.get_in_degrees(w)
                    sub_x = np.random.geometric(p_f) - 1
                    if sub_x < x.size:
                        x = np.random.choice(x, sub_x, replace=False)

                    if x.size != 0:
                        n_ws = np.append(n_ws, x)

                    y = graph.get_out_degrees(w)
                    sub_y = np.random.geometric(p_r) - 1
                    if sub_y < y.size:
                        y = np.random.choice(y, sub_y, replace=False)

                    if y.size != 0:
                        n_ws = np.append(n_ws, y)

                if n_ws.size != 0:
                    n_ws = np.setdiff1d(n_ws, add_n)

                for nl in ws:
                    graph.add_edge(i, int(nl))
                add_n = np.append(add_n, ws)
                ws = n_ws
        return graph

    @staticmethod
    def gnp_random_graph(n, p, directed=True):
        return SGraph(nx.generators.fast_gnp_random_graph(n, p, directed=directed))

    @staticmethod
    def geometric(n, dis, clean=True, dim=2):
        res = nx.random_geometric_graph(n, dis, dim=dim)
        sub = max(nx.connected_components(res), key=len)
        res = SGraph(res).subgraph(sub)

        if clean:
            res.del_attrs(["pos"])
        return res

    @staticmethod
    def waxman(n, beta=0.11, alpha=0.1, L=None, clean=True):
        res = nx.waxman_graph(n, beta=beta, alpha=alpha, L=L)
        sub = max(nx.connected_components(res), key=len)
        res = SGraph(res).subgraph(sub)

        if clean:
            res.del_attrs(["pos"])
        return res

    @staticmethod
    def chunglu(seq):
        res = nx.expected_degree_graph(seq, selfloops=False)
        nodes = sorted(nx.connected_components(res), key=len, reverse=True)[0]
        return SGraph(res).subgraph(nodes)

    @staticmethod
    def power_law(n, sigma):
        inds = np.floor(1/powerlaw.rvs(sigma, size=n))
        if np.sum(inds) % 2 == 1:
            inds = np.append(inds, [1])

        res = nx.expected_degree_graph([int(u) for u in inds])
        nodes = sorted(nx.connected_components(res), key=len, reverse=True)[0]
        res.remove_edges_from(nx.selfloop_edges(res))
        return SGraph(res).subgraph(nodes)

    @staticmethod
    def load(path, typ=nx.Graph):
        return SGraph(typ(nx.read_graphml(path)))

    @staticmethod
    def load_adj(path, typ=nx.Graph):
        return SGraph(typ(nx.read_adjlist(path)))
