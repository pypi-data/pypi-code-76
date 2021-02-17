#!/usr/bin/env python3

"""
|===================================|
| Manipulation d'un arbre enracine. |
|===================================|
"""

import math

from .. import basegraph


class ArborescenceGraph(basegraph.FrozenGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_arborescence():
            raise ValueError("Le graphe n'est pas un arbre enracine.")

    def _place(self):
        """
        Impose une coordonne aux noeuds.
        """
        layer = {self.id2vertex[self.properties["root_id"]]: [0, 2*math.pi]}
        rayon = 0
        while layer:
            leaf = {} # La couche suivante
            for vertex, (thetamin, thetamax) in layer.items():
                vertex.x = rayon*math.cos(.5*(thetamin + thetamax))
                vertex.y = rayon*math.sin(.5*(thetamin + thetamax))

                successors = self.successors(vertex)
                if successors:
                    portion = (thetamax - thetamin)/len(successors)
                    for i, s in enumerate(successors):
                        leaf[s] = [thetamin + i*portion, thetamin + (i+1)*portion]

            layer = leaf.copy()
            rayon += 1
