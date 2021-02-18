import numpy as np

from mcg.extreme.estimator.nonopt.blocks import BlocksEstimate
from pge.ranks.extrem_onl import NodeExInfo
from pge.ranks.onlcore.criterion.rcriterion import pgr


def back(graph, chosen, wr):
    return graph.get_out_degrees(chosen, w=wr)


def str_(graph, chosen, wr):
    if graph.directed():
        return graph.get_in_degrees(chosen, w=wr)
    if hasattr(chosen, "__iter__"):
        res = []
        for chosen_ in chosen:
            res = np.append(res, graph.get_degrees(chosen_, wr))
        return np.unique(res)
    return graph.get_degrees(chosen, wr)


class DepNodeEx(NodeExInfo):
    @staticmethod
    def get_ex(gr, root, frm, c=0.85, stab=30, entity=BlocksEstimate,
               full=None, frm_stub=True, view=5, part=True, criterion=pgr, typ="sl", w=False, way=str_):
        if full is None:
            full = gr.size()

        if w:
            wr = frm+"w"
        else:
            wr = None

        exes = np.array([])
        ids = np.array([])
        nxt = [np.array([]), np.array([])]
        rank = gr.get_attr(root, frm)

        if rank == 0:
            return np.array([]), np.array([]), np.array([]), np.array([])

        choosen = [root, 1]
        bls = np.array([])
        clust = np.array([])

        count = 0
        count_ = 0
        while choosen is not None:
            ids = np.append(ids, choosen[0])
            k = way(gr, choosen[0], wr)
            if part:
                k = np.setdiff1d(k, ids)
                k = np.setdiff1d(k, nxt[0])

            if k.size > 0:
                other = criterion(gr, c, (k, choosen[0], root), (frm, choosen[1]))

                nxt[0] = np.append(nxt[0], k)
                nxt[1] = np.append(nxt[1], other)

            if nxt[0].size == 0:
                choosen = None
            else:
                ind = np.argmax(nxt[1])
                choosen = [nxt[0][ind], nxt[1][ind]]
                nxt[0] = np.delete(nxt[0], ind)
                nxt[1] = np.delete(nxt[1], ind)

            if frm_stub and ids.size <= stab and choosen is not None:
                continue

            ranks, blks = gr.get_blk_attrs(frm, ids, typ)
            clust = np.append(clust, entity.get_avg_blk(blks))

            if clust[-1] == 1:
                exes = np.append(exes, 1)
                bls = np.append(bls, 1)
            else:
                ex, u = entity.mse((ranks, blks))
                exes = np.append(exes, ex)
                bls = np.append(bls, entity.back((ranks, blks), u))

            if ids.size >= full:
                break

            if np.abs((exes[-1] - 1 / clust[-1])) < 0.01 or np.abs(1 - exes[-1] - 1 / clust[-1]) < 0.01:
                count += 1
            else:
                if count != 0:
                    count_ += 1
                count = 0

            if count_ == view:
                exes = exes[:exes.size-1]
                clust = clust[:clust.size-1]
                bls = bls[:bls.size-1]
                ids = ids[:ids.size-1]
                break

        return ids, exes, bls, clust
