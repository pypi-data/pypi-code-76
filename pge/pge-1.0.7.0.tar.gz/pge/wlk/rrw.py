import numpy as np

from pge.wlk.walker import RandomWalk
from rd_pr.simple import uniform


class RandomReWalk(RandomWalk):
    def generate(self, n, st=None, c=0.15, end_start=False):
        steps = uniform(n)
        res = []

        if st is None:
            res.append(np.random.choice(self.gr.get_ids(), size=1))
        else:
            res.append(st)

        for i in np.arange(1, n):
            if self.gr.count_out_degree(res[i-1]) == 0:
                if end_start:
                    res.append(res[0])
                else:
                    if i >= 2:
                        res.append(res[-2])
                    else:
                        res.append(res[0])

            if steps[i] < c:
                res.append(res[0])
            else:
                res.append(np.random.choice(self.gr.get_out_degrees(res[-1])))
        return res
