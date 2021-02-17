#!/usr/bin/env python3

"""
|===========================|
| Represente un processus,  |
| un routeur ou un serveur. |
|===========================|

* Modelise un noeud dans le graphe.
"""

import inspect


class Vertex:
    """
    |=========================|
    | Noeud abstrait de base. |
    |=========================|

    * C'est la classe de base pour
    representer un noeud quelquonque.

    Example
    -------
    >>> from raisin.graph.vertex import Vertex
    >>> Vertex()
    Vertex(n=0)
    >>> Vertex(name="noeud", y=1, x=0)
    Vertex(name='noeud', n=1, x=0, y=1)
    >>>
    """
    def __init__(self, *, name="", n=None, x=None, y=None, z=None):
        """
        :param name: Nom du noeud.
        :type name: str
        :param n: Identifiant du noeud.
        :type n: int
        :param x: Coordonnee en x.
        :type x: int, float
        :param y: Coordonnee en y.
        :type y: int, float
        :param z: Coordonnee en z.
        :type z: int, float
        """
        assert n == None or isinstance(n, int), \
            "'n' have to be str. Not %s." % tye(n).__name__
        assert isinstance(name, str), \
            "'name' must be str. Not %s." % type(name).__name__
        assert x == None or isinstance(x, int) or isinstance(x, float), \
            "'x' must to be a number, not a %s." % type(x).__name__
        assert y == None or isinstance(y, int) or isinstance(y, float), \
            "'y' must to be a number, not a %s." % type(y).__name__
        assert z == None or isinstance(z, int) or isinstance(z, float), \
            "'z' must to be a number, not a %s." % type(z).__name__
        
        self.n = n if n != None else next(_counter)
        self.name = name
        self.x, self.y, self.z = x, y, z
        self.flags = {} # Informations pour ce noeud.

    def __repr__(self):
        """
        Representation de l'objet directement evaluable
        par python dans un contexte donne.
        Toutes les informations y sont pour un debaugage
        precis.
        """
        return "%s(%s)" % (type(self).__name__, ", ".join(
            (
            repr(getattr(self, s.name))
            if s.kind == inspect.Parameter.POSITIONAL_ONLY
            or s.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            else "%s=%s" % (s.name, repr(getattr(self, s.name)))
            )
            for s in list(inspect.signature(self.__init__).parameters.values())
            if s.default != getattr(self, s.name)))

    def __hash__(self):
        """
        Rend l'objet hachable pour pouvoir le
        metre dans un dictionaire ou un enssemble.
        """
        return hash((self.n, "vertex"))

    def __eq__(self, other):
        """
        Regarde si self et other sont le meme sommet.
        """
        if isinstance(other, Vertex):
            return self.n == other.n
        return False

class _Counter:
    """
    Incremente un compteur global.
    """
    def __init__(self):
        self.i = -1
        self.excluded = set()

    def __next__(self):
        self.i += 1
        while self.i in self.excluded:
            self.i += 1
        return self.i

    def append(self, i):
        self.excluded.add(i)
       
_counter = _Counter()
