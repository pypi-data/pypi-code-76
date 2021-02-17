#!/usr/bin/env python3

"""
|===================================|
| Manipulation d'un graphe complet. |
|===================================|
"""

import math

from .. import basegraph


class CompleteGraph(basegraph.FrozenGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_complete():
            raise ValueError("Le graphe n'est pas un graphe complet.")

    def _place(self):
        """
        Impose une coordonne aux noeuds.
        """
        if len(self) <= 4:
            return super()._place()

        for i, v in enumerate(self.get_vertices()):
            theta = 2*math.pi*i / len(self)
            v.x = math.cos(theta)
            v.y = math.sin(theta)

