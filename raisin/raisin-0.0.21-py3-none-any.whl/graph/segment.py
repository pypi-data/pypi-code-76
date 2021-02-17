#!/usr/bin/env python3

"""
|===============================|
| Represente une connection     |
| a travers le reseau ethernet. |
|===============================|

* C'est les arretes du graphe.
"""

import inspect

import numpy as np

from ..errors import *
from . import vertex

class Segment:
    """
    |=============================|
    | Representation d'un segment |
    | generique reliant 2 noeuds. |
    |=============================|

    * Classe de base qui represente a la fois un arc et une arete.
    """
    def __init__(self, vs, vd, *, name, weight, n):
        """
        :param vs: Vertex Source (Le depart de l'arette.)
        :type vs: vertex.Vertex
        :param vd: Vertex Destination (L'arrivee de l'arette.)
        :type vd: vertex.Vertex
        :param name: Nom de l'arette.
        :type name: str
        :param weight: Cout de l'arrette.
            -Soit int ou float.
            -Soit une fonction pour un cout plus subtil.
        :type weight: int, float, callable
        :param n: Identifiant de l'arette (gere tout seul)
        :type n: int
        """
        assert isinstance(vs, vertex.Vertex), \
            "'vs' have to be an instance of Vertex, not %s." \
            % type(vs).__name__
        assert isinstance(vd, vertex.Vertex), \
            "'vd' have to be an instance of Vertex, not %s." \
            % type(vd).__name__
        assert isinstance(name, str), \
            "'name' must be str. Not %s." % type(name).__name__
        assert isinstance(weight, (int, float)) \
            or hasattr(weight, "__call__"), "'weight' have to be " \
            "int, float or callable. Not %s." % type(weight).__name__
        assert n == None or isinstance(n, int), \
            "'n' have to be str. Not %s." % tye(n).__name__

        self.vs = vs
        self.vd = vd
        self.name = name
        self.weight = weight
        self.n = n if n != None else next(_counter)
        self.flags = {} # Informations pour cet arc.
    
    def __repr__(self):
        """
        Representation de cette arrette directement
        evaluable par python dans un contexte donne.
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
        Appelee par les membres de collection haches.
        """
        return hash((self.n, "segment"))

    def __call__(self, *args, **kwargs):
        """
        |=================================|
        | Evaluation du cout de l'arette. |
        |=================================|

        * Si le cout est un nombre. Ce nombre
        est retourne directement.
        * Si le cout est un callable, la fonction
        de cout est evaluee et la valeur de retour
        de cette fonction de cout est renvoyee.

        entree
        ------
        :arg args: Les arguments de la fonction
            de cout 'self.weight'.
        :key kwargs: Le dictionaire de la
            fonction de cout 'self.weight.'

        sortie
        ------
        :return: La valeur de la fonction de cout.
        """
        try:
            return self.weight(*args, **kwargs)
        except TypeError: # Cas d'une fonction de cout non callable.
            return self.weight

    def __neg__(self):
        """
        Change le sens de l'arc.
        N'affecte pas self.
        Une copie est renvoyee.
        Appelee par "-self".
        """
        new_segment = self.copy()
        if self.name:
            new_segment.name = "invert_" + new_segment.name
        new_segment.vs, new_segment.vd = new_segment.vd, new_segment.vs
        return new_segment

    def __and__(self, other):
        """
        |=================================|
        | Calcule le taux d'intersection. |
        |=================================|

        * self & other
        * Le taux d'intersection entre 2 sommets est une
        fonction polynomiale continue qui vaut:
            0 Quand il n'y a pas d'intersection.
            1 Quand l'intersection est au milieu des 2 segments.

        Parameters
        ----------
        :param other: Un autre segment.
        :type other: Segment

        Returns
        -------
        :return: Un reel entre 0 et 1.
        :rtype: float
        :raises AttributeError: Si les coordonees ne sont pas definies.
            ou qu'un segment est un point.
        :raises AmbiguousError: Si leur intersection est un segment.
        """
        assert isinstance(other, Segment), \
            "'other' has to be an instance of Segment, not %s." \
            % type(other).__name__

        if self.vs.x is None or self.vs.y is None \
                or other.vs.x is None or other.vs.y is None \
                or self.vd.x is None or self.vd.y is None \
                or other.vd.x is None or other.vd.y is None:
            raise AttributeError("One of the coordinate is not defined.")
        if (self.vs.x == self.vd.x and self.vs.y == self.vd.y) \
                or (other.vs.x == other.vd.x and other.vs.y == other.vd.y):
            raise AttributeError("One of the segment is a point.")
        
        # On cherche l'intersections des droites portee par les segments.
        # La droite d1 est donnee par l'equation: d1(l1) = v1*l1
        #   - v1 le vecteur directeur de la droite.
        #   - l1 le parametre.
        # La droite d2 est donnee par l'equation: d2(l2) = v2*l2 + c
        #   - v2 le vecteur directeur.
        #   - l2 le parametre.
        #   - c les coordonnes d'un point de la droite quand l2 = 0,
        #     en prenant comme origine d1(0).
        # Cela revient a resoudre A*l = c.
        #   - A la matrice (v1, -v2).
        #   - l le vecteur colonne ((l1,), (l2,)).

        A = np.matrix(
            [[self.vd.x - self.vs.x, other.vs.x - other.vd.x],
             [self.vd.y - self.vs.y, other.vs.y - other.vd.y]],
             dtype=float)
        c = np.matrix(
            [[other.vs.x - self.vs.x],
             [other.vs.y - self.vs.y]],
             dtype=float)
        try:
            l = A.I * c
        except np.linalg.LinAlgError as error: # Si les segments sont paralleles.
            # Pour tester si les segments sont portes par une meme droite,
            # On regarde si le parallelogramme (self.vs, self.vd, other.vd, other.vs)
            # Est plat. Pour cela, on regarde si c ^ self == 0.
            if c[0, 0]*A[1, 0] - c[1, 0]*A[0, 0]: # Si ils sont pas sur la meme droite.
                return 0
            
            if 2 == len({(self.vs.x, self.vs.y), (self.vd.x, self.vd.y),
                    (other.vs.x, other.vs.y), (other.vd.x, other.vd.y)}):
                raise AmbiguousError("%s et %s sont entierement confondus."
                    % (repr(self), repr(other))) from error

            # On cherche si l'une des extremitee de other est contenue dans self.
            #   - e l'extremiter de self projete sur la droite porteuse.
            #   - nc la norme de c.
            for i in range(2): # Si self dqns other et other dans self
                v1, v2 = A[:, 0], -A[:, 1]
                if i:
                    v1, v2, c = v2, v1, -c
                e = np.linalg.norm(v1) * np.sign(np.dot(c.T, v1))[0, 0]
                emin, emax = min(0, e), max(0, e)
                nc = np.linalg.norm(c)
                
                if emin < nc < emax or \
                        emin < nc + np.linalg.norm(v2)*np.sign(np.dot(c.T, v2))[0, 0] < emax: # Si ile se chevauchent.
                    raise AmbiguousError("%s et %s ont un segment en commun."
                        % (repr(self), repr(other))) from error
            return 0
        else: # Si les droites se coupent en 1 point.
            if (0 < l).all() and (l < 1).all(): # Si l'intersection des droites se trouve dans les segments.
                l1, l2 = l[0, 0], l[1, 0]
                return 16*(l1**2 - l1)*(l2**2 - l2)
            return 0

    def copy(self):
        """
        Retourne une copie de self.
        """
        return Edge(self.vs, self.vd, weight=self.weight, name=self.name)

class Arrow(Segment):
    """
    |==================================|
    | Representation d'un arc oriante. |
    |==================================|

    :seealso: ``Segment``

    Example
    -------
    >>> from raisin.graph import *
    >>> vs = vertex.Vertex()
    >>> vd = vertex.Vertex()
    >>> segment.Arrow(vs, vd)
    Arrow(Vertex(n=0), Vertex(n=1), n=0)
    >>> segment.Arrow(vs, vd, name="arc", weight=0.5)
    Arrow(Vertex(n=0), Vertex(n=1), name='arc', weight=0.5, n=1)
    >>>
    """
    def __init__(self, vs, vd, *, name="", weight=1, n=None):
        super().__init__(vs, vd, name=name, weight=weight, n=n)
        self.directed = True

class Edge(Segment):
    """
    |==========================================|
    | Representation d'une arrete non oriante. |
    |==========================================|

    :seealso: ``Segment``

    Example
    -------
    >>> from raisin.graph import *
    >>> vs = vertex.Vertex()
    >>> vd = vertex.Vertex()
    >>> segment.Edge(vs, vd)
    Edge(Vertex(n=0), Vertex(n=1), n=0)
    >>> segment.Edge(vs, vd, name="arc", weight=0.5)
    Edge(Vertex(n=0), Vertex(n=1), name='arete', weight=0.5, n=1)
    >>>
    """
    def __init__(self, vs, vd, *, name="", weight=1, n=None):
        super().__init__(vs, vd, name=name, weight=weight, n=n)
        self.directed = False

_counter = vertex._Counter()
