import numpy as np
from scipy.stats import ks_2samp
import networkx as nx

from pge.init.classes.graph import SGraph
from pge.wlk.rnn import RandomNeighbourNode


def check(graph, attr, nm=20, rw=RandomNeighbourNode, iter=100, test=ks_2samp):
    step = int(graph.size()/nm)
    szes = np.arange(step, graph.size(), step=step)
    walker = rw(graph)
    smpls = graph.get_attributes(attr)

    res1, res2 = [], []
    for sz in szes:
        for _ in np.arange(iter):
            sub = graph.get_attributes(attr, walker.generate(sz, unique=True))
            res2.append(test(smpls, sub)[1])
            res1.append(sz)
    return np.array(res1), np.array(res2)


def check_mean(graph, attr, nm=20, rw=RandomNeighbourNode, iter=100, test=ks_2samp):
    res1, res2 = check(graph, attr, nm=nm, rw=rw, iter=iter, test=test)
    un = np.unique(res1)
    nw1, nw2, nw3 = [], [], []
    for u in un:
        nw1.append(np.max(res2[res1 == u]))
        nw2.append(np.mean(res2[res1 == u]))
        nw3.append(np.min(res2[res1 == u]))
    return nw1, nw2, nw3, un


def check2(graph, attr, test=ks_2samp):
    ids = graph.get_ids(stable=True)
    smpls = graph.get_attributes(attr)

    res1, res2 = [], []
    for r in np.arange(1, nx.diameter(graph.get_nx_graph())):
        for root in ids:
            #root = np.random.choice(ids)
            sub = SGraph(nx.ego_graph(graph.get_nx_graph(), root, r))
            sub = graph.get_attributes(attr, sub.get_ids())
            res2.append(test(smpls, sub)[1])
            res1.append(r)
    return np.array(res2), np.array(res1)


def check2_mean(graph, attr, test=ks_2samp):
    res1, res2 = check2(graph, attr, test=test)

    un = np.unique(res2)
    nw1, nw2, nw3 = [], [], []
    for u in un:
        nw1.append(np.max(res1[res2 == u]))
        nw2.append(np.mean(res1[res2 == u]))
        nw3.append(np.min(res1[res2 == u]))
    return nw1, nw2, nw3, un
