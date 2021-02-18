

def per_node_estimation(i, gr, frm, to, templ, c, entity, st_pl, typ, view, crt, w, full=200):
    ids, exes, clust, bls = templ.get_ex(gr, i, frm, c, entity=entity, stab=st_pl, typ=typ, view=view, criterion=crt, w=w, full=full)

    if ids.size == 0:
        print("-")
        gr.set_attr(i, to, 1)
        gr.set_attr(i, to + "-cls", 1)
        gr.set_attr(i, to + "-blk", 1)
        gr.set_attr(i, to + "-sz", 1)
    else:
        gr.set_attr(i, to, exes[-1])
        print(i, ids.size-1, exes[-1], bls[-1])

        gr.set_attr(i, to + "-cls", clust[-1])
        gr.set_attr(i, to + "-blk", bls[-1])
        gr.set_attr(i, to + "-sz", ids.size)
    return ids


def ex_estimate(gr, frm, to, templ, c, entity, crt, st_pl=50, typ="sl", view=5, w=False):
    for n in gr.get_ids():
        per_node_estimation(n, gr, frm, to, templ, c, entity, st_pl, typ, view, crt, w)


class NodeExInfo:
    @staticmethod
    def get_ex(gr, roots, frm):
        return None

    @staticmethod
    def double_value():
        return False


class CommExInfo:
    @staticmethod
    def get_ex(gr, roots, frm):
        return None

    @staticmethod
    def double_value():
        return False
