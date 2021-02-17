#!/usr/bin/env python3

"""
|=========================|
| Les connections reseau. |
|=========================|

* Dans un graphe qui represente un reseau internet, les arcs
relient les machines aux boxes et aux routeurs.
* Modelise un debit variable, le ping ...
"""

from ..segment import Arrow

class Connection(Arrow):
    """
    |====================================|
    | Un cable RJ45 et une carte reseau. |
    |====================================|
    """
    def __init__(self, vs, vd, ping=None, flow=None):
        super().__init__(vs, vd)
        self.ping = ping
        self.flow = flow
        self.flags["color"] = "black"

    def get_attr(self):
        """
        |===================================|
        | Recupere les arguments suffisants |
        | a la reconstitution de self.      |
        |===================================|

        Returns
        -------
        :return: Les clefs et les valeurs a passer a l'initialisateur
            de facon a instancier un nouvel objet de contenu identique a self.
        :rtype: dict
        """
        return {"vs": self.vs.n, "vd": self.vd.n, "attr": {}}
