import numpy as np

from mcg.extreme.estimator.nonopt.simpleblocks import SBlocksEstimate
from mcg.extreme.find.mse import boot
from pge.ranks.extrem_onl import NodeExInfo
from pge.ranks.rank import estimate_rank


class GravNodeEx(NodeExInfo):
    @staticmethod
    def get_ex(gr, root, frm, c, stab=30, entity=SBlocksEstimate,
               full=200, frm_stub=True, view=5, part=True, typ="sl"):

        exes = np.array([])
        ids = np.array([])
        nxt = [np.array([]), np.array([])]
        rank = gr.get_attr(root, frm)

        if rank == 0:
            return np.array([]), np.array([]), np.array([]), np.array([])

        chosen = [root, 0]
        bls = np.array([])
        clust = np.array([])

        count = 0
        count_ = 0
        while chosen is not None:
            ids = np.append(ids, chosen[0])
            k = gr.get_in_degrees(chosen[0])

            k = np.setdiff1d(k, ids)
            k = np.setdiff1d(k, nxt[0])

            if k.size > 0:
                subs = gr.copy()
                subs.delete_node(chosen[0])
                estimate_rank(subs, tp=frm, c=c)
                other = (rank - subs.get_attr(root, frm))/rank

                nxt[0] = np.append(nxt[0], k)
                nxt[1] = np.append(nxt[1], other)

            if nxt[0].size == 0:
                chosen = None
            else:
                ind = np.argmax(nxt[1])
                chosen = [nxt[0][ind], nxt[1][ind]]
                nxt[0] = np.delete(nxt[0], ind)
                nxt[1] = np.delete(nxt[1], ind)

            if frm_stub and ids.size <= stab and chosen is not None:
                continue

            ranks, blks = gr.get_blk_attrs(frm, ids, typ)

            clust = np.append(clust, entity.get_avg_blk(blks))
            us = np.unique(ranks)
            res = boot(entity, (ranks, blks), 1 / 3, 2 / 3, 100, us)
            mses = np.array([res[i][0] for i in np.arange(us.size)])
            ex = np.array([res[i][1] for i in np.arange(us.size)])

            i = np.argmin(mses)
            exes = np.append(exes, ex[i])
            bls = np.append(bls, entity.back((ranks, blks), us[i]))

            if ids.size > full:
                break

            if np.abs((exes[-1] - 1 / clust[-1])) < 0.01 or np.abs(1 - exes[-1] - 1 / clust[-1]) < 0.01:
                count += 1
            else:
                if count != 0:
                    count_ += 1

                count = 0

            if count_ == view:
                exes = exes[:exes.size - 1]
                clust = clust[:clust.size - 1]
                bls = bls[:bls.size - 1]
                ids = ids[:ids.size - 1]
                break

        return ids, exes, bls, clust
