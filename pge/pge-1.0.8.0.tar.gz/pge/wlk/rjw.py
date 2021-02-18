import numpy as np

from pge.wlk.walker import RandomWalk
from rd_pr.simple import uniform


class RandomJumpingWalk(RandomWalk):
    def generate(self, n, st=None, c=0.15, end_start=False):
        steps = uniform(n)

        if st is None:
            news = np.random.choice(self.gr.get_ids(), size = np.sum(steps < c) + 1)
            res = [news[0]]
            news = news[1:]
        else:
            news = np.random.choice(self.gr.get_ids(), size= np.sum(steps < c))
            res = [st]

        count = 0
        for i in np.arange(1, n):
            if self.gr.count_out_degree(res[-1]) == 0:
                if end_start:
                    res.append(res[0])
                else:
                    if i >= 2:
                        res.append(res[-2])
                    else:
                        res.append(res[0])

            if c > steps[i]:
                res.append(news[count])
                count += 1
            else:
                res.append(np.random.choice(self.gr.get_out_degrees(res[-1])))

        return np.array(res)


