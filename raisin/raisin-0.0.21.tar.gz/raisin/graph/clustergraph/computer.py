#!/usr/bin/env python3

"""
|==========================|
| Les noeuds 'ordinateur'. |
|==========================|

* Dans un graphe qui represente un reseau internet, les noeuds
modelises ici sont les noeuds qui sont capable d'effectuer un calcul.
"""

from ..vertex import Vertex

class Computer(Vertex):
    """
    |===============================|
    | Un ordinateur dans un reseau. |
    |===============================|

    * C'est une entitee capable d'executer des taches.
    """
    def __init__(self, *, n=None):
        super().__init__(n=n)
        self.flags["edgecolor"] = "black"
        self.flags["facecolor"] = "#77c100" # Vert.

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
        return {
            "initializer": {"n": self.n},
            "internal": {}}

class MySelf(Vertex):
    """
    |==================================|
    | Votre ordinateur dans le reseau. |
    |==================================|

    * Plus specifiquement, un processus relier a l'ordinateur.
    """
    def __init__(self, n=None):
        super().__init__(name="MySelf", n=n)
        self.flags["edgecolor"] = "black"
        self.flags["facecolor"] = "#ff0000" # Rouge.

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
        return {
            "initializer": {"n": self.n},
            "internal": {}}
