import pandas as pd
import numpy as np
import networkx as nx


class SGraph:
    def __init__(self, gr):
        self.gr = gr
        self.p = None
        self.pi = None

    def clean_copy(self):
        G = self.gr.__class__()
        G.add_edges_from(self.gr.edges())
        return SGraph(G)

    def directed(self):
        return nx.is_directed(self.get_nx_graph())

    def number_of_edges(self):
        return self.gr.number_of_edges()

    def clean(self):
        self.gr.clear()

    def subgraph(self, nodes):
        sub = self.gr.subgraph(nodes).copy()
        return SGraph(sub)

    def get_ids(self, stable=False):
        if stable:
            return np.array(list(self.gr.nodes()))
        else:
            return self.gr.nodes()

    def get_nodes_with(self, attr, value):
        ids = self.get_ids(stable=True)
        return ids[self.get_attributes(attr) == value]

    def get_edges(self, stable=False):
        if stable:
            return np.array(list(self.gr.edges(data=False)))
        else:
            return self.gr.edges(data=False)

    def has_node(self, node):
        return self.gr.has_node(node)

    def set_attr(self, ind, attr, value):
        self.gr.nodes[ind][attr] = convert(value)

    def set_attrs(self, attr, values):
        nx.set_node_attributes(self.gr, name=attr, values=values)

    def get_attr(self, ind, attr):
        if hasattr(ind, "__iter__") and not isinstance(ind, str):
            res = []
            for i in ind:
                try:
                    res.append(self.gr.nodes[i][attr])
                except:
                    res.append(0)
            return np.array(res)

        try:
            return self.gr.nodes[ind][attr]
        except:
            return 0

    def get_node_data(self, ind):
        return self.gr.nodes[ind]

    def add_node(self, id_n):
        self.gr.add_node(id_n)

    def add_nodes(self, ids):
        self.gr.add_nodes_from(ids)

    def del_node(self, id_n):
        self.gr.remove_node(id_n)

    def del_nodes(self, ids):
        self.gr.remove_nodes_from(ids)

    def copy(self):
        return SGraph(self.gr.copy())

    def get_attributes(self, attr, nodes=None, noneval=0):
        if nodes is None:
            nodes = self.gr.nodes()

        res = []
        for x in nodes:
            try:
                res.append(self.gr.nodes[x][attr])
            except:
                res.append(noneval)
        return np.array(res)

    def get_edge_attributes(self, attr, noneval=0):
        res = []
        for x in self.gr.edges(data=False):
            try:
                res.append(self.get_edge_data(x[0], x[1], attr))
            except:
                res.append(noneval)
        return np.array(res)

    def get_attrs_dict(self, attr):
        return nx.get_node_attributes(self.gr, attr)

    def get_nx_graph(self):
        return self.gr

    def get_prob_matrix(self):
        if self.p is None:
            p = nx.to_numpy_matrix(self.gr)
            self.p = np.divide(p, np.sum(p, axis=0))
        return self.p

    def get_stat_dist(self):
        if self.pi is None:
            A = np.subtract(
                np.transpose(self.get_prob_matrix()), np.diag(np.ones(self.size()))
            )
            A = np.vstack([A, np.ones(self.size())])

            b = np.zeros(self.size() + 1)
            b[-1] = 1

            try:
                self.pi = np.linalg.lstsq(A, b, rcond=None)[0]
            except:
                self.pi = np.ones(self.size())
        return self.pi

    def add_edge(self, u, v):
        self.gr.add_edge(u, v)

    def add_edges(self, edges):
        self.gr.add_edges_from(edges)

    def get_edge_data(self, u, v, frm, bsc=0):
        try:
            return self.gr[u][v][frm]
        except:
            return bsc

    def set_edge_data(self, u, v, to, value):
        self.gr[u][v][to] = value

    def del_edge(self, u, v):
        self.gr.remove_edge(u, v)

    def del_edges(self, edges):
        self.gr.remove_edges_from(edges)

    def add_path(self, path):
        self.gr.add_path(path)

    def size(self):
        return self.gr.number_of_nodes()

    def size_edge(self):
        return self.gr.number_of_edges()

    def count_in_degree(self, ind, w=None):
        if w is None:
            return self.get_in_degrees(ind).size
        res = self.get_in_degrees(ind, w=w, bsc=1)
        return np.sum(res)

    def count_out_degree(self, out, w=None,):
        if w is None:
            return self.get_out_degrees(out).size
        res = self.get_out_degrees(out, w=w, bsc=1)
        return np.sum(res)

    def get_count_edges(self):
        return self.gr.number_of_edges()

    def get_in_degrees(self, ind, w=None, un=True, bsc=0):
        if self.directed():
            res = [x[0] for x in self.gr.in_edges(ind)]
        else:
            res = [x[0] for x in self.gr.edges(ind) if x[0] != ind] + [
                x[1] for x in self.gr.edges(ind) if x[1] != ind
            ]

        if un:
            res = np.unique(res)
        if w is None:
            return np.array(res)
        else:
            return np.array([self.get_edge_data(res, ind, w, bsc=bsc)])

    def get_out_degrees(self, out, w=None, un=True, bsc=0):
        if self.directed():
            res = [x[1] for x in self.gr.out_edges(out)]
        else:
            res = [x[0] for x in self.gr.edges(out) if x[0] != out] + [
                x[1] for x in self.gr.edges(out) if x[1] != out
            ]

        if un:
            res = np.unique(res)
        if w is None:
            return np.array(res)
        else:
            return np.array([self.get_edge_data(out, res, w, bsc=bsc)])

    def get_data(self, attrs=None, nodes=None):
        if nodes is None:
            nodes = self.gr.nodes()

        if attrs is None:
            attrs = (self.gr.node[nodes[0]]).keys()

        data = []
        for attr in attrs:
            data.append((attr, []))
        ids = []

        for node in nodes:
            ids.append(node)
            for data_line in data:
                data_line[1].append(self.gr.node[node][data_line[0]])

        df = pd.DataFrame(ids, columns=["id"])
        for data_line in data:
            df[data_line[0]] = pd.Series(data_line[1], index=df.index)
        return df

    def save_attrs(self, path, sep=","):
        data = self.get_data()
        data.to_csv(path, sep=sep, index=False)

    def del_attrs(self, attrs):
        if not hasattr(attrs, "__iter__"):
            attrs = [attrs]

        for n in self.get_ids():
            for attr in attrs:
                del self.gr.nodes[n][attr]

    def get_blk_attrs(self, frm, nodes, typ, part=True):
        xs = np.array([])
        blks = np.array([])

        count = 0
        if typ == "sl" or typ == "sl-ext":
            for j in nodes:
                subs = self.get_in_degrees(j)
                if typ == "sl-ext":
                    subs = np.append(j, subs)
                if part:
                    subs = subs[np.isin(subs, nodes)]
                if subs.size == 0:
                    continue
                res = self.get_attributes(frm, subs)
                blks = np.append(blks, count * np.ones(res.size))
                xs = np.append(xs, res)
                count = count + 1

        if typ == "b-sl" or typ == "b-sl-ext":
            for j in nodes:
                subs = self.get_out_degrees(j)
                if typ == "b-sl-ext":
                    subs = np.append(j, subs)
                if part:
                    subs = subs[np.isin(subs, nodes)]
                if subs.size == 0:
                    continue
                res = self.get_attributes(frm, subs)
                blks = np.append(blks, count * np.ones(res.size))
                xs = np.append(xs, res)
                count = count + 1

        if typ == "dj":
            subs = []
            blk = []
            subs_ = np.array([])
            blk_ = []

            for j in nodes:
                sub = self.get_out_degrees(j)

                if sub.size > 1:
                    nad = True
                    for prt in np.arange(len(subs)):
                        if np.sum(np.isin(sub, subs[prt])) > 1:
                            nad = False
                            subs[prt] = np.unique(np.append(subs[prt], sub))
                            blks = np.append(blks, blk[prt])
                            break
                    if nad:
                        subs.append(sub)
                        blk.append(count)
                        blks = np.append(blks, count)
                        count += 1
                else:
                    nex = True
                    for prt in np.arange(subs_.size):
                        if subs_[prt] == sub[0]:
                            nex = False
                            blks = np.append(blks, blk_[prt])
                            break

                    if nex:
                        blks = np.append(blks, count)
                        subs_ = np.append(subs_, sub)
                        blk_.append(count)
                        count += 1
                xs = np.append(xs, self.get_attr(j, frm))
        return xs, blks

    def get_ln_attrs(self, frm, nodes, count=False):
        xs = []
        lv = np.array([])

        for node in nodes:
            xs.append(self.get_attributes(frm, node))
            lv = np.append(lv, self.get_attributes(frm, node))
        lv = np.unique(lv, return_counts=count)
        return np.array(xs), lv

    def get_all_short_pathes(self, nodes, plain=True):
        if len(nodes) < 2:
            return [], []

        pathes, ln = [], []

        for node in nodes:
            pathes_, ln_ = self.get_short_paths(node, nodes)
            pathes += pathes_
            if plain:
                ln += ln_
            else:
                if len(ln_) != 0:
                    ln += [ln_]
        return pathes, np.array(ln)

    def get_short_line_paths(self, root, nodes=None):
        if nodes is None:
            nodes = self.get_ids(stable=True)

        pathes, ln = [], []
        for node in nodes:
            if root == node:
                continue
            path = next(
                nx.all_shortest_paths(
                    self.gr, source=root, target=node, method="bellman-ford"
                )
            )
            if isinstance(path[0], list):
                for path_ in path:
                    pathes.append(np.array(path_))
                    ln.append(len(path_) - 1)
            else:
                pathes.append(np.array(path))
                ln.append(len(path) - 1)
        return pathes, ln

    def get_short_paths(self, root, nodes):
        if len(nodes) < 2:
            return [], []

        pathes, ln = [], []
        done = [root]
        step = [[root]]

        while len(step) != 0:
            if len(pathes) == len(nodes) - 1:
                break

            step_ = []
            for st in step:
                for res in self.get_in_degrees(st[-1]):
                    if res not in done:
                        done.append(res)
                        st_ = st.copy()
                        st_.append(res)

                        if res in nodes:
                            pathes.append(st_)
                            ln.append(len(st_) - 1)
                        else:
                            step_.append(st_)
            step = step_
        return pathes, ln

    def get_short_paths2(self, root, nodes):
        if len(nodes) < 2:
            return [], []

        pathes, ln = [], []
        done = [root]
        step = [[root]]

        while len(step) != 0:
            if len(pathes) == len(nodes) - 1:
                break

            step_ = []
            for st in step:
                for res in self.get_in_degrees(st[-1]):
                    if res not in done:
                        done.append(res)
                        st_ = st.copy()
                        st_.append(res)

                        if res in nodes:
                            pathes.append(st_)
                            ln.append(len(st_) - 1)
                        else:
                            step_.append(st_)
            step = step_
        return pathes, ln


def convert(value):
    try:
        return float(value)
    except:
        return str(value)
