import numpy as np
from random import choice, randint

from pge.model.spreading.spreader.basic import SpreadingModel


class UniformGossip(SpreadingModel):
    def iteration(self):
        ind = randint(0, self.ids.size - 1)
        node = self.ids[ind]

        if self.graph.directed():
            others = self.graph.get_in_degrees(node)
        else:
            others = self.graph.get_degrees(node)

        if others.size != 0:
            u = choice(others)
            old = list(self.status[node])
            self.status[node].update(self.status[u])

            if self.received[ind] != len(self.status[node]):
                self.received[ind] = len(self.status[node])
                nws = np.setdiff1d(list(self.status[node]), old)
                self.messes[np.isin(self.ids, nws)] += 1
