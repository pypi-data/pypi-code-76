import numpy as np

from pge.wlk.walker import RandomWalk


class RandomNeighbourNode(RandomWalk):
    def generate(self, n, st=None, unique=False):
        if st is None:
            st = np.random.choice(self.gr.get_ids())
        res = [st]

        while True:
            if self.gr.count_out_degree(res[-1]) == 0:
                res.append(res[0])
            else:
                res.append(np.random.choice(self.gr.get_out_degrees(res[-1])))

            if (unique and np.unique(res).size == n) or (~unique and len(res) == n):
                break
        if unique:
            return np.unique(res)
        else:
            return np.array(res)
