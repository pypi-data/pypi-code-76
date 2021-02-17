#!/usr/bin/env python3

"""
|===================================|
| Manipulation d'un graphe biparti. |
|===================================|
"""

from .. import basegraph


class BipartiteGraph(basegraph.FrozenGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bipartite():
            raise ValueError("Le graphe n'est pas un graphe biparti.")

    def methode_bipartite(self):
        pass


