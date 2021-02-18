import numpy as np
import networkx as nx


def phi(gr, nodes, other=None):
    if gr.directed():
        ind_i = np.arange(gr.size())[[node in nodes for node in gr.get_ids()]]
        if other is not None:
            ind_j = np.arange(gr.size())[[node in other for node in gr.get_ids()]]
        else:
            ind_j = np.arange(gr.size())[[node not in nodes for node in gr.get_ids()]]
        pi = gr.get_stat_dist()
        c = np.sum(pi[ind_i])
        v = np.sum(pi[ind_j])

        p = gr.get_prob_matrix()
        w = np.multiply(p, pi)

        p1 = np.sum(w[np.ix_(ind_j, ind_i)])
        p2 = np.sum(w[np.ix_(ind_i, ind_j)])
        return np.max([p1 / c, p2 / v])
    else:
        try:
            return nx.algorithms.cuts.conductance(gr.get_nx_graph(), nodes, other)
        except:
            return 0


def conductance_speed(gr):
    if nx.is_connected(gr.get_nx_graph()):
        ls = np.sort(nx.normalized_laplacian_spectrum(gr.get_nx_graph()))[1]
        dg_mx = np.max([gr.count_in_degree(node) for node in gr.get_ids()])
        return np.mean([ls/(2*dg_mx), np.sqrt(ls*2/dg_mx)])
    else:
        return 0

def conductance(gr, start_node=None):
    if start_node is None:
        comp = sorted(
            nx.algorithms.community.greedy_modularity_communities(gr.get_nx_graph()),
            key=len,
            reverse=True,
        )
        return conductance_iter(gr, [(list(com), phi(gr, com)) for com in comp])
    else:
        return conductance_iter(gr, [([start_node], phi(gr, [start_node]))])


def conductance_iter(gr, com):
    fx = []

    while len(com) > 0:
        com_ = []
        for comm in com:
            if comm[1] == 0:
                return 0
            comm_ = []
            tst_ = []

            if len(comm[0]) + 1 <= gr.size() / 2:
                for node_out in gr.get_out_degrees(comm[0], un=True):
                    if node_out in comm[0]:
                        continue

                    try:
                        tst_.append(phi(gr, comm + [node_out]))
                        comm_.append(comm + [node_out])
                    except:
                        continue

            for node in comm[0]:
                nw_comm = comm[0].copy()
                nw_comm.remove(node)
                if len(nw_comm) == 0:
                    continue

                gr_ = gr.subgraph(nw_comm)
                if nx.number_connected_components(gr_.get_nx_graph()) != 1:
                    continue

                try:
                    tst_.append(phi(gr, nw_comm))
                    comm_.append(nw_comm)
                except:
                    continue

            if len(tst_) == 0:
                fx.append(comm)
                continue

            if np.min(tst_) < comm[1]:
                rs = np.min(tst_)
                for i in np.arange(len(tst_)):
                    if rs == tst_[i]:
                        com_.append((comm_[i], rs))
            else:
                fx.append(comm)
        com = com_

    return np.min([fx_[1] for fx_ in fx])


def weak_conductance(gr, attr):  # todo вложение
    nx.set_node_attributes(gr.get_nx_graph(), 0, attr)
    comms = sorted(
        nx.algorithms.community.greedy_modularity_communities(gr.get_nx_graph()),
        key=len,
        reverse=True,
    )

    updatable = True
    while updatable:
        comms_ = []
        updatable = False
        for comm in comms:
            ph = phi(gr, comm)
            if ph == 0:
                comms_.append(comm)
                continue

            vars = []
            vars_comm = []
            for node_out in gr.get_out_degrees(comm, un=True):
                if node_out in comm:
                    continue

                try:
                    vars.append(phi(gr, [node_out] + comm))
                    vars_comm.append([node_out] + comm)
                except:
                    continue

            if len(vars) == 0:
                comms_.append(comm)
                updatable = updatable or False
                continue

            mn = np.min(vars)
            if mn <= ph:
                for i in np.arange(len(vars)):
                    if vars[i] == mn:
                        comms_.append(vars_comm[i])
                        updatable = updatable or True
            else:
                comms_.append(comm)
                updatable = updatable or False
        comms = comms_

    for com in comms:
        if len(com) == 1:
            gr.set_attr(list(com)[0], attr, 0)
            continue
        ph = conductance(gr.subgraph(com))
        for node in com:
            gr.set_attr(node, attr, max(gr.get_attr(node, attr), ph))
