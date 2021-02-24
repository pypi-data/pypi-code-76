import numpy as np

from pge.ranks.onlcore import DepNodeEx
from pge.ranks.onlcore import GravNodeEx


class SlideNodeEx(GravNodeEx, DepNodeEx):
    def __init__(self, eps, tree=True, quick=True):
        super().__init__(eps, quick)
        self.tree = tree

    def get_params(self, gr, c_d, frm, way):
        if self.tree:
            return DepNodeEx.get_params(self, gr, c_d, frm, way)
        else:
            return GravNodeEx.get_params(self, gr, c_d, frm, way)

    def get_ex_field(self, gr, root, frm, c):
        if self.tree:
            return DepNodeEx.get_ex_field(self, gr, root, frm, c)
        else:
            return GravNodeEx.get_ex_field(self, gr, root, frm, c)

    def get_ex(self, gr, frm, to):
        res = []

        for node in self.f:
            exc = gr.get_in_degrees(node)

            if exc.size == 0:
                continue

            nodes = gr.get_in_degrees(self.f, ex_i=gr.get_in_degrees(node), un=False)

            if nodes.size == 0:
                continue

            mx = np.max(gr.get_attributes(frm, exc))
            subs = np.where(gr.get_attributes(frm, nodes) <= mx, 1, 0)
            res.append(max([-exc.size*np.log(np.mean(subs)), 1]))

        if len(res) > 0:
            return 1/np.mean(res)
        else:
            return 0

    @staticmethod
    def save_param(gr, n, res, to):
        gr.set_attr(n, to, res)
