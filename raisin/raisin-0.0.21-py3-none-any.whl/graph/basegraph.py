#!/usr/bin/env python3

"""
|===================================|
| Manipulation d'un graphe de base. |
|===================================|

* C'est un graphe abstrait mathematique
sans propriete particuliere.

* Vocabulaire base sur:
https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms
"""

import inspect
import queue
import random

import numpy as np

from ..errors import *
from . import segment as mod_segment
from . import vertex as mod_vertex
from . import plot, properties


class BaseGraph(plot.Display, properties.Properties):
    """
    |==========================|
    | Graphe abstrait de base. |
    |==========================|

    * C'est un graphe oriante de base qui n'a
    pas de propriete particuliere.

    * C'est un multi-graphe, c'est a dire qu'il peut
    y avoir plusieurs arcs qui relient 2 memes sommets.

    Example
    -------
    >>> from raisin.graph.basegraph import *
    >>> BaseGraph({(1, 0), (2, 0), (3, 0), (4, 0)})
    BaseGraph({
        Edge(Vertex(n=1), Vertex(n=0), n=0),
        Edge(Vertex(n=4), Vertex(n=0), n=1),
        Edge(Vertex(n=2), Vertex(n=0), n=2),
        Edge(Vertex(n=3), Vertex(n=0), n=3)})
    >>>
    """
    def __init__(self, content=None, *, directed=None, comment=""):
        """
        |===============================|
        | Remplissage du graphe.        |
        | Initialisation des attributs. |
        |===============================|

        * Ce graphe est construit comme un graphe oriante.

        entree
        ------
        :param content: Les elements qui permettent de construire le graphe.
            1) None -> Un graphe vide est cree.
            2) dict -> A chaque sommet, associ les sommets adjacents.
                (Si c'est pas precise, le graphe est oriante.)
                example: {0: [1, 2], 1: [2]}
                example: {"a": ["b", "c"], "b": ["c"]}
                example: {Vertex(n=0): [Vertex(n=1), Vertex(n=2)], Vertex(n=1): [Vertex(n=2)]}
            3) set, frozenset -> L'ensemble des arcs / aretes.
                (L'oriantation depend si c'est des aretes ou des arcs.)
                example: {(0, 1), (0, 2), (1, 2)}
                example: {('a', 'b'), ('a', 'c'), ('b', 'c')}
                example: {(Vertex(n=0), Vertex(n=1)), ..., (Vertex(n=1), Vertex(n=2))}
                example: {Edge(Vertex(n=0), Vertex(n=1)), ..., Edge(Vertex(n=1), Vertex(n=2))}
            4) list, np.ndarray -> La matrice d'adjacence.
                (L'oriantation depend de la symetrie de la matrice.)
                example: [[0, 1, 1], [0, 0, 1], [0, 0, 0]]
            5) BaseGraph -> Une instance d'un graphe.
                example: BaseGraph(BaseGraph())
        :param directed: Permet de forcer l'oriantation du graphe:
            True -> Le graphe est oriante.
            False -> Le graphe n'est pas oriante.
            None (default) -> L'oriantation est determinee automatiquement.
        :type directed: boolean
        :param comment: Le nom du graphe.
        :type comment: str
        """
        assert directed is None or isinstance(directed, bool), \
            "'directed' has to be a boolean, not a %s." \
            % type(directed).__name__
        # Initialisation.
        self.directed = directed
        self.comment = comment
        self.id2vertex = {} # A chaque id (n), associ l'objet noeud.
        self.id2segment = {} # A chaque id (n), associ l'objet arette.
        self.graph = {} # La clef represente le noeud d'id n.
            # Chaque valeur ressemble a ca:
            # [{arc1, arc2}, {arc3, arc4}] ou {arete1, arete2}
        self.properties = {} # Des resultats intermediaires evitant de refaire des calculs.

        # Remplissage.
        if content is None:
            return
        if isinstance(content, dict):
            self.directed = True if self.directed is None else self.directed
            for ver, adjs in content.items():
                self.add_segments(*[(ver, adj) if self.directed else {ver, adj} for adj in adjs])
            return
        if isinstance(content, (set, frozenset)):
            self.add_segments(*content)
            return
        if isinstance(content, list):
            content = np.array(content)
        if isinstance(content, BaseGraph):
            self.directed = content.directed
            self.comment = comment if comment else content.comment
            self.id2vertex = content.id2vertex
            self.id2segment = content.id2segment
            self.graph = content.graph
            self.properties = content.properties
            return
        if isinstance(content, np.ndarray):
            if content.ndim != 2:
                raise ValueError(
                    "Une matrice doit etre en 2 dimensions, pas %d." % content.ndim)
            if content.shape[0] != content.shape[1]:
                raise ValueError(
                    "Une matrice d'adjacence doit etre carre, el fait %dx%d."
                    % content.shape)
            if self.directed is None:
                self.directed = not (content == content.transpose()).all()
            for i, line in enumerate(content):
                for j, e in enumerate(line):
                    if not self.directed and j > i:
                        continue
                    if e == 1:
                        self.add_segment((i, j) if self.directed else {i, j})
                    elif e != 0:
                        raise ValueError(
                            "Une matrice d'adjacence doit contenir que des"
                            "0 ou des 1. Pas des %s.", repr(e))
            return
        raise TypeError("Impossible de construire un graphe a partir d'un %s."
            % type(content).__name__)

    def __contains__(self, element):
        """
        |========================================|
        | Recherche si other est dans le graphe. |
        |========================================|

        * Methode apellee par le mot clef 'in'.

        entree
        ------
        :param obj: Ce qui permet de designer un arc ou un noeud.

        sortie
        ------
        :return: True si obj est contenu dans self.
            False sinon.
        :rtype: boolean
        """
        try:
            self[element]
        except KeyError:
            return False
        except AmbiguousError:
            return True
        else:
            return True

    def __repr__(self):
        """
        |===========================|
        | Representation evaluable. |
        |===========================|

        * Appele par repr(self) ou print(self).

        sortie
        ------
        :return: Un representation de ce graphe evaluable
            par l'interpeteur python dans un contexte particulier.
        :rtype: str
        """
        name = type(self).__name__
        directed = "" if self.directed is None else "directed=%s" % self.directed
        if self:
            return "%s({%s}%s)" \
                % (name, ", ".join(map(repr, self.get_segments())),
                (", %s" % directed) if directed else "")
        return "%s(%s)" % (name, directed)

    def __bool__(self):
        """
        |=============================|
        | Vois si le graphe est vide. |
        |=============================|

        * Appele par bool(self) et donc par extension par 'if self'.
        * Un graphe et vide si il ne contient aucun noeuds.
        
        sortie
        ------
        :return:
            True si le graphe n'est pas vide.
            False si il n'y a ni noeud ni arc.
        :rtype: boolean
        """
        return bool(self.id2vertex)

    def __len__(self):
        """
        |=============================|
        | Renvoi la taille du graphe. |
        |=============================|

        * La taille d'un graphe est le nombre de sommets qu'il contient.

        sortie
        ------
        :return: Le nombre de sommets presents dans ce graphe.
        :rtype int
        """
        return len(self.id2vertex)

    def __getitem__(self, key, is_vertex=None):
        """
        |=======================================|
        | Cherche le noeud l'arete ou l'arc du  |
        | graphe qui corespond a la clef.       |
        |=======================================|

        * Appele par self[key].

        entree
        ------
        :param key: Element qui permet de retrouver le noeud ou l'arc.
            Il peut prendre differentes formes:
            1) type Vertex -> S'assure juste qu'il soit dans le graphe. O(1)
            2) type Edge, Arrow -> S'assure juste qu'il soit dans le graphe. O(1)
                                -> Prend en compte l'oriantation du graphe.
            3) type str -> Retourne le noeud l'arete ou l'arc ayant ce nom. O(n_vertex + n_segments)
                -> Pour lever l'ambiguite, fixer 'is_vertex'.
            4) type list, tuple -> Recherche un arc.
                4.1) (type int, type int) -> Retourne l'arc reliant ces 2 noeuds. O(1)
                4.2) (type Vertex, type Vertex) -> Retourne l'arc reliant ces 2 noeuds. O(1)
                4.3) (type str, type str) -> Retourne l'arc reliant ces 2 noeuds. O(n_vertex)
            5) type set, frozenset -> Recherche une arete.
                5.1) len(key) == 2 -> Comme 4)
                5.2) len(key) == 1 -> Retourne l'arete qui boucle sur ce noeud.
            6) type int -> Retourne le noeud, l'arete ou l'arc ayant cet id.
                -> Pour lever l'ambiguite, fixer 'is_vertex'.
        :param is_vertex: Permet de cibler la recherche.
            True -> Recherche parmis les noeuds seulement.
            False -> Recherche parmi les aretes et les arcs seulement.
            None -> S'adapte selon le contexte.
        :type is_vertex: boolean

        sortie
        ------
        :return: Le noeud, l'arete ou l'arc present dans ce graphe pouvant
            etre caracterise par la clef.
        :rtype: Vertex or Arrow or Edge
        :raises KeyError: Si l'element n'est pas trouvable.
        :raises TypeError: Si la clef n'est pas conforme.
        :raises AmbiguousError: Si plusieurs elements sont trouves.
        """
        assert is_vertex is None or isinstance(is_vertex, bool), \
            "'is_vertex' has to be a boolean, not a %s." \
            % type(is_vertex).__name__

        if not len(self):
            raise KeyError("Le graphe est vide. Il ne peut "
                "pas contenir %s." % repr(key))

        if isinstance(key, mod_vertex.Vertex): # Cas 1).
            if key.n not in self.id2vertex:
                raise KeyError("Le noeud %s n'est pas dans le graphe." % repr(key))
            return key
        
        elif isinstance(key, mod_segment.Arrow): # Cas 2.1)
            if not self.directed:
                raise KeyError("Le graphe contient seulement des aretes, pas d'arcs, "
                    "or %s est un arc." % repr(key))
            if key.n not in self.id2segment:
                raise KeyError("L'arc %s n'est pas dans le graphe." % repr(key))
            return key
        elif isinstance(key, mod_segment.Edge): # Cas 2.2)
            if self.directed:
                raise KeyError("Le graphe contient seulement des arcs, pas d'aretes, "
                    "or %s est une arete." % repr(key))
            if key.n not in self.id2segment:
                raise KeyError("L'arete %s n'est pas dans le graphe." % repr(key))
            return key
        
        elif isinstance(key, str): # Cas 3)
            if not key:
                raise KeyError("Pour recuperer un element par son nom, "
                    "il ne faut pas fournir un nom vide.")
            if is_vertex != False:
                vertices = {v.name: v for v in self.get_vertices()}
            if is_vertex != True:
                segments = {e.name: e for e in self.get_segments()}
            
            if key in vertices and is_vertex == True:
                return vertices[key]
            else:
                raise KeyError("Il n'y a pas de sommet nome %s." % repr(key))
            if key in segments and is_vertex == False:
                return segments[key]
            else:
                raise KeyError("Il n'y a pas d'arete ou d'arc nome %s." % repr(key))
            
            if key in vertices and key not in segments:
                return vertices[key]
            if key in segments and key not in vertices:
                return segments[key]
            if key in segments and key in vertices:
                raise AmbiguousError("Un arc/arete et un sommet ont le meme nom. "
                    "C'est donc ambigue pour le nom %s." % repr(key))
            raise KeyError("Aucun element du graphe n'a le nom %s." % repr(key))
        
        elif isinstance(key, (list, tuple)): # Cas 4)
            if not self.directed:
                raise KeyError(("Le graphe contient seulement des aretes, "
                    "pas d'arcs, or %s represente un arc, pas une arete. "
                    "Utiliser un type set ou frozenset.") % repr(key))
            if len(key) != 2:
                raise TypeError("Si la clef est une liste ou un tuple, "
                    "c'est qu'elle represente un arc. Elle doit donc "
                    "contenir 2 noeuds. Or elle en contient %d." % len(key))
            vs = self.__getitem__(key[0], is_vertex=True)
            vd = self.__getitem__(key[1], is_vertex=True)
            arrows_id = {arrow_id for arrow_id in self.graph[vs.n][0]
                if self.id2segment[arrow_id].vd.n == vd.n}
            if not arrows_id:
                raise KeyError("Il n'y a pas d'arc reliant le noeud "
                    "%s au noeud %s." % (repr(vs), repr(vd)))
            if len(arrows_id) > 1:
                raise AmbiguousError(("Il y a %d arcs qui relient le "
                    "noeud %s au noeud %s.")
                    % (len(arrows_id), repr(vs), repr(vd)))
            return self.id2segment[arrows_id.pop()]

        elif isinstance(key, (set, frozenset)): # Cas 5)
            if self.directed:
                raise KeyError(("Le graphe contient seulement des arcs, "
                    "pas d'aretes, or %s represente une arete, pas un arc. "
                    "Utilisez un type tuple ou list.") % repr(key))
            if len(key) == 1:
                key = [key.pop()]*2
            if len(key) != 2:
                raise TypeError("Si la clef est un ensemble, "
                    "c'est qu'elle represente une arete. Elle doit donc "
                    "contenir 2 ou 1 noeuds. Or elle en contient %d." % len(key))
            key = list(key)
            vs = self.__getitem__(key[0], is_vertex=True)
            vd = self.__getitem__(key[1], is_vertex=True)
            segments_id = {segment_id for segment_id in self.graph[vs.n]
                if self.id2segment[segment_id].vd.n == vd.n}
            if not segments_id:
                raise KeyError("Il n'y a pas d'arete reliant le noeud "
                    "%s au noeud %s." % (repr(vs), repr(vd)))
            if len(segments_id) > 1:
                raise AmbiguousError(("Il y a %d aretes qui relient le "
                    "noeud %s au noeud %s.")
                    % (len(segments_id), repr(vs), repr(vd)))
            return self.id2segment[segments_id.pop()]

        elif isinstance(key, int): # Cas 6)
            if key in self.id2vertex and is_vertex == True:
                return self.id2vertex[key]
            else:
                raise KeyError("Il n'y a pas de sommet d'id %d." % key)
            if key in self.id2segment and is_vertex == False:
                return self.id2segment[key]
            else:
                raise KeyError("Il n'y a pas d'arete ou d'arc d'id %d." % key)

            if key in self.id2vertex and key not in self.id2segment:
                return self.id2vertex[key]
            if key in self.id2segment and key not in self.id2vertex:
                return self.id2segment[key]
            if key in self.id2segment and key in self.id2vertex:
                raise AmbiguousError("Un arc/arete et un sommet ont le meme identifiant. "
                    "C'est donc ambigue pour l'id %d." % key)
            raise KeyError("Aucun element du graphe n'a l'identifiant %d." % key)

        raise TypeError("La clef doit etre de type str, list, tuple, set, "
            "frozenset ou int. Pas %s." % type(key).__name__)
    
    def __delitem__(self, key):
        """
        |================================|
        | Supprime un element du graphe. |
        |================================|

        entree
        ------
        :param key: Element qui permet de retrouver
            le noeud ou l'arc a supprimer.
        :seealso: self.__getitem__
        """
        element = self[key]
        if isinstance(element, mod_vertex.Vertex):
            self.del_vertex(element)
        elif isinstance(element, mod_segment.Segment):
            self.del_segment(element)
        else:
            raise TypeError("Impossible de supprimer %s." % repr(element))

    # Methodes de modification du graphe.
    
    def add_vertex(self, vertex):
        """
        |============================|
        | Ajoute un noeud au graphe. |
        |============================|

        * Le noeud ajoute n'est relie a rien d'autre.

        entree
        ------
        :param vertex: Le nouveau noeud a ajouter.
            Peut prendre 3 formes:
            1) Un objet derive de la classe Vertex. O(1)
            2) En entier correspondant a l'id du noeud. O(1)
            3) Un str representant le nom du noeud. O(n)
        :type vertex: vertex.Vertex

        sortie
        ------
        :return: None
        :raises KeyError: Si le sommet est deja present
            dans ce graphe.

        Example
        -------
        >>> from raisin.graph import *
        >>> gr = graph.BaseGraph()
        >>> gr.add_vertex(vertex.Vertex())
        >>> gr.add_vertex(1)
        >>> gr.add_vertex("noeud_2")
        >>> print(gr.get_vertices())
        [Vertex(n=0), Vertex(n=1), Vertex(name='noeud_2', n=2)]
        >>>
        """
        # Verifications.
        if isinstance(vertex, mod_vertex.Vertex):
            pass
        elif isinstance(vertex, int): # L'identifiant doit etre unique.
            vertex = mod_vertex.Vertex(n=vertex) # Le verfification de l'unicite
            mod_vertex._counter.append(vertex.n) # ce fait juste apres.
        elif isinstance(vertex, str): # Par contre on impose pas que le
            if vertex == "": # nom soit unique.
                raise ValueError("Si vous ajoutez un noeud par son nom. "
                    "Il ne doit pas etre une chaine vide.")
            vertex = mod_vertex.Vertex(name=vertex)
        else:
            raise TypeError("'vertex' have to an instance of Vertex, "
                "int or str. Not %s." % type(vertex).__name__)

        if vertex in self:
            raise KeyError("Le noeud %s est deja dans le graphe." % repr(vertex))

        # Mise a jour des proprietes du graphe.
        self.properties = {}

        # Ajout.
        self.id2vertex[vertex.n] = vertex
        self.graph[vertex.n] = set() if self.directed == False else [set(), set()]

    def add_vertices(self, *vertices):
        """
        |==================================|
        | Attach vertices VERTICES to the  |
        | graph while avoiding duplicates. |
        |==================================|

        :seealso: self.add_vertex
        """
        for v in vertices:
            self.add_vertex(v)

    def add_segment(self, segment):
        """
        |==============================|
        | Ajoute un segment au graphe. |
        |==============================|

        * Les noeuds relies par le segment sont deja
        contenus dans l'objet 'segment'

        entree
        ------
        :param segment: Nouvel arc ou arete a ajouter.
            'segment' peut prendre differentes formes:
            1) Un objet Arrow ou Edge
            2) Un iterable a 2 elements,
                le premier element etant le noeud de depart
                et le second etant le noeud d'arrive.
                Les elements peuvent independament etre de type
                Vertex, int ou str.
            3) Un iterable a 3 elements,
                Les 2 premiers elements sont les memes que pour
                un iterable a 2 elements.
                Le troisieme etant le poid du noeud.
        :type segment: Arrow ou Edge

        * Si l'oriantation du graphe est fixe, force
        a ce que l'entree soit coherente. Si elle n'est pas encore
        fixee, choisi l'orientation selon le type.
        * Un set ou un frozenset represente une arete, tout autre iterable
        represente un arc.

        sortie
        ------
        :return: None
        :raises KeyError: Si une arete ou un arc reliant ces 2 noeuds existe deja.
        :raises TypeError: Si l'orientation du graphe n'est pas coherente.

        Example
        -------
        >>> from raisin.graph import *
        >>> gr = graph.BaseGraph()
        >>> gr.add_segment(segment.Edge(vertex.Vertex(name="a"), vertex.Vertex()))
        >>> gr.add_segment([1, 2])
        >>> gr.add_segment([0, 2, 0.18])
        >>> gr.add_segment([1, "a"])
        >>> print(gr.get_segments())
        [Edge(Vertex(name='a', n=0), Vertex(n=1), n=0),
         Edge(Vertex(n=1), Vertex(n=2), n=1),
         Edge(Vertex(name='a', n=0), Vertex(n=2), cost=0.18, n=2),
         Edge(Vertex(n=1), Vertex(name='a', n=0), n=3)]
        >>>
        """
        # Creation de la nouvelle arete ou du nouvel arc.
        if isinstance(segment, mod_segment.Arrow): # Cas 1.1)
            if self.directed == False:
                raise TypeError("Le graphe n'est pas oriante. Or "
                    "%s est un arc et pas une arete." % repr(segment))
            if segment in self:
                raise KeyError("L'arc %s est deja dans present." % repr(segment))
            self.directed = True
        elif isinstance(segment, mod_segment.Edge): # Cas 1.2)
            if self.directed == True:
                raise TypeError("Le graphe est un graphe oriante. Or "
                    "%s est une arete et non pas un arc." % repr(segment))
            if segment in self:
                raise KeyError("L'arete %s est deja presente." % repr(segment))
            self.directed = False
        elif hasattr(segment, "__iter__"): # Cas 2 et 3, si il faut creer l'objet arete ou arc.
            # Verification de coherence d'oriantation.
            if isinstance(segment, (set, frozenset)):
                if self.directed == True:
                    raise TypeError(("Le graphe est oriante, Or "
                        "%s represente une arete, pas un arc. "
                        "Utilisez un type ordoner pour representer un arc.")
                        % repr(segment))
                self.directed = False
            else:
                if self.directed == False:
                    raise TypeError(("Le graphe n'est pas oriante, Or "
                        "%s represente un arc, pas une arete. "
                        "Utilisez set, frozenset ou Edge pour representer "
                        "une arete.") % repr(segment))
                self.directed = True

            # Verification de la longeur.
            segment = list(segment)
            if self.directed:
                assert 2 <= len(segment) <= 3, \
                    "La longueur d'un arc ne peut etre que 2 ou 3. Pas %d." % len(segment)
            else:
                if len(segment) == 1:
                    segment *= 2
                assert len(segment) == 2, \
                    "La longueur d'une arete ne peut etre que 2. Pas %d." % len(segment)

            # Recuperation les 2 noeuds qui constituent l'arc ou l'arete.
            for i in [0, 1]:
                if isinstance(segment[i], mod_vertex.Vertex):
                    pass
                elif isinstance(segment[i], int):
                    if segment[i] in self.id2vertex: # Si le noeud existe deja.
                        segment[i] = self.id2vertex[segment[i]] # On le recupere.
                    else: # Si le noeud n'existe pas.
                        segment[i] = mod_vertex.Vertex(n=segment[i]) # On le fabrique.
                        mod_vertex._counter.append(segment[i].n)
                elif isinstance(segment[i], str):
                    assert segment[i] != "", \
                        "On ne peut pas identifier un noeud par une chaine vide."
                    if any(segment[i] == v.name for v in self.get_vertices()): # Si le noeud existe deja
                        vertices = self.get_vertices()
                        if [v.name for v in vertices].count(segment[i]) > 1: # Si plusieurs noeuds ont ce nom,
                            raise AmbiguousError("Plusieur noeud ont le nom %s." # on echoue.
                                % repr(segment[i]))
                        segment[i] = vertices[[v.name for v in vertices].index(segment[i])]
                    else: # Si le noeud n'existe pas.
                        segment[i] = mod_vertex.Vertex(name=segment[i]) # On le cre.
                else:
                    raise TypeError("Les elements ne peuvent etre que Vertex, "
                        "int ou str. Pas %s." % type(segment[i]).__name__)

            # Creation de l'arc ou de l'arete.
            if len(segment) == 2:
                if self.directed:
                    segment = mod_segment.Arrow(segment[0], segment[1])
                else:
                    segment = mod_segment.Edge(segment[0], segment[1])
            else:
                if self.directed:
                    segment = mod_segment.Arrow(segment[0], segment[1], cost=segment[2])
                else:
                    segment = mod_segment.Edge(segment[0], segment[1], cost=segment[2])
        else:
            raise TypeError("'segment' has to of type Arrow, Edge, "
                "or to be iterable. Not %s." % type(segment).__name__)

        # Ajout des noeuds.
        if segment.vs not in self:
            self.add_vertex(segment.vs)
        if segment.vd not in self:
            self.add_vertex(segment.vd)
        
        # Mise a jour des proprietes du graphe.
        self.properties = {}
        
        # Ajout le l'arc / arete.
        self.id2segment[segment.n] = segment
        if self.directed:
            self.graph[segment.vs.n][0].add(segment.n)
            self.graph[segment.vd.n][1].add(segment.n)
        else:
            if type(self.graph[segment.vs.n]) == list:
                self.graph[segment.vs.n] = set()
            self.graph[segment.vs.n].add(segment.n)
            if type(self.graph[segment.vd.n]) == list:
                self.graph[segment.vd.n] = set()
            self.graph[segment.vd.n].add(segment.n)
    
    def add_arrow(self, arrow):
        """
        |==================================|
        | Ajoute un arc oriante au graphe. |
        |==================================|

        :seealso: Alias of ``self.add_segment``.
        """
        if self.directed == False:
            raise TypeError("Vous avez utilises la methode 'add_arrow' "
                "au lieu de 'add_edge'. Or %s est une arete et non un arc."
                % repr(arrow))
        self.directed = True
        return self.add_segment(arrow)

    def add_edge(self, edge):
        """
        |=========================================|
        | Ajoute une arete non oriante au graphe. |
        |=========================================|

        :seealso: Alias of ``self.add_segment``.
        """
        if self.directed == True:
            raise TypeError("Vous avez utilises la methode 'add_edge' "
                "au lieu de 'add_arrow'. Or %s est un arc et non une arete."
                % repr(edge))
        self.directed = False
        return self.add_segment(edge)
        
    def add_segments(self, *segments):
        """
        |==========================================|
        | Ajoute tous les arcs / aretes d'un coup. |
        |==========================================|

        :seealso: ``self.add_segment``
        """
        for s in segments:
            self.add_segment(s)

    def add_arrows(self, *arrows):
        """
        |=================================|
        | Ajoute tous les arcs d'un coup. |
        |=================================|

        :seealso: ``self.add_arrow``
        """
        for a in arrows:
            self.add_arrow(a)

    def add_adges(self, *adges):
        """
        |=====================================|
        | Ajoute toutes les aretes d'un coup. |
        |=====================================|

        :seealso: ``self.add_edge``
        """
        for e in edges:
            self.add_edge(e)

    def del_vertex(self, vertex):
        """
        |===============================|
        | Supprime le noeud et tous les |
        | segments qui y sont relie.    |
        |===============================|

        entree
        ------
        :param vertex: Le noeud a supprimer.
            Peut prendre 3 formes:
            1) Un objet derive de la classe Vertex.
            2) En entier correspondant a l'id du noeud.
            3) Un str representant le nom du noeud.
        :type vertex: Vertex
        """
        vertex = self.__getitem__(vertex, is_vertex=True)

        # Suppression des aretes / arcs reliees a ce sommet.
        if type(self.graph[vertex.n]) == list:
            for segment_id in self.graph[vertex.n][0].copy():
                self.del_segment(segment_id)
            for segment_id in self.graph[vertex.n][1].copy():
                self.del_segment(segment_id)
        else:
            for segment_id in self.graph[vertex.n].copy():
                self.del_segment(segment_id)
        
        # Mise a jour des proprietes du graphe.
        self.properties = {}

        # Suppression du noeud.
        del self.graph[vertex.n]
        del self.id2vertex[vertex.n]

    def del_segment(self, segment):
        """
        |=======================|
        | Supprime une liaison. |
        |=======================|

        entree
        ------
        :param segment: L'arete ou l'arc a supprimer.
        :type segment: Arrow or Edge
        """
        segment = self.__getitem__(segment, is_vertex=False)
           
        # Mise a jour des proprietes du graphe.
        self.properties = {}

        # Suppresion de l'arc
        if self.directed:
            self.graph[segment.vs.n][0].remove(segment.n)
            self.graph[segment.vd.n][1].remove(segment.n)
        else:
            self.graph[segment.vs.n].remove(segment.n)
            self.graph[segment.vd.n].remove(segment.n)
        del self.id2segment[segment.n]
    
    def del_arrow(self, arrow):
        """
        |==================|
        | Supprime un arc. |
        |==================|

        :seealso: ``self.del_segment``
        """
        if self.directed == False:
            raise TypeError("Vous avez utilises la methode 'del_arrow' "
                "au lieu de 'del_edge'. Or le graphe n'est pas oriante.")
        return self.del_segment(arrow)

    def del_edge(self, edge):
        """
        |=====================|
        | Supprime une arete. |
        |=====================|

        :seealso: ``self.del_segment``
        """
        if self.directed == True:
            raise TypeError("Vous avez utilises la methode 'del_edge' "
                "au lieu de 'del_arrow'. Or le graphe est oriante.")
        return self.del_segment(edge)

    # Methodes d'acces aux elements.

    def get_vertices(self):
        """
        |===================================|
        | Return all vertices in the graph. |
        |===================================|

        sortie
        ------
        :return: Toutes les sommets.
        :rtype: list
        """
        return list(self.id2vertex.values())

    def get_segments(self, vertex=None):
        """
        |=============================================|
        | Return all segments in the graph as a list. |
        |=============================================|

        Parameters
        ----------
        :param vertex: Si il est precise, seul
            les segments adjacents a ce noeud sont renvoyes.

        sortie
        ------
        :return: Tous les arcs / aretes.
        :rtype: list
        """
        if vertex is None:
            return list(self.id2segment.values())

        vertex = self.__getitem__(vertex, is_vertex=True)
        if self.directed == False:
            return [self.id2segment[a_id] for a_id in self.graph[vertex.n]]
        return [self.id2segment[e_id] for e_id in self.graph[vertex.n][0] | self.graph[vertex.n][1]]

    def predecessors(self, vertex):
        """
        |=============================|
        | Recherche les voisins qui   |
        | peuvent acceder a ce noeud. |
        |=============================|

        * Il n'y a pas de redondance dans les noeuds renvoyes.
        * Complexite en O(1).

        entree
        ------
        :param vertex: De quoi identifier le noeud concidere.

        sortie
        ------
        :return: Tous les noeuds ayant l'acces.
        :rtype: set
        """
        vertex = self.__getitem__(vertex, is_vertex=True)

        if self.directed:
            return {self.id2segment[a_id].vs for a_id in self.graph[vertex.n][1]}
        return {e.vs if e.vs != vertex else e.vd
            for e in (self.id2segment[e_id] for e_id in self.graph[vertex.n])}

    def successors(self, vertex):
        """
        |================================|
        | Recherche les voisins qui sont |
        | accessible par ce noeud.       |
        |================================|

        * Il n'y a pas de redondance dans les noeuds renvoyes.
        * Complexite en O(1).

        entree
        ------
        :param vertex: De quoi identifier le noeud concidere.

        sortie
        ------
        :return: Tous les noeuds accessibles.
        :rtype: set
        """
        vertex = self.__getitem__(vertex, is_vertex=True)

        if self.directed:
            return {self.id2segment[a_id].vd for a_id in self.graph[vertex.n][0]}
        return {e.vd if e.vd != vertex else e.vs
            for e in (self.id2segment[e_id] for e_id in self.graph[vertex.n])}

    def neighbors(self, vertex, dmin=-1, dmax=1):
        """
        |=============================|
        | Recherche tous les voisins. |
        |=============================|

        * C'est les noeuds que l'on peut atteindre
        et les noeuds qui peuvent nous atteindre.
        * dmin = 0 et dmax = 1 est equivalent a self.successors.
        * dmin = -1 et dmax = 0 est equivalent a self.predecessors.
        * dmin = 2 et dmax = 2 retroune les voisins des voisins...

        entree
        ------
        :param vertex: De quoi identifier le noeud concidere.
        :param dmin: Profondeur de recherche des predecesseurs.
            0 -> Ne recherche pas de predecesseurs.
            -1 -> Recherche les predecesseurs direct.
            -2 -> Recherche les predecesseurs direct
                et les predesesseurs des predesecceurs.
            -n -> Recherche les predesseseurs avec une profondeur de n.
        :type dmin: int
        :param dmax: Profondeur de recherche des successeurs.
            0 -> Ne recherche pas de successeurs.
            1 -> Recherche les noeuds directement accessible
            n -> Pareil recursivement n fois.
        :type dmax: int

        sortie
        ------
        :return: L'ensemble des voisins consideres.
        :rtype: set
        """
        assert isinstance(dmin, int), \
            "'dmin' doit etre int, pas %s." % type(dmin).__name__
        assert isinstance(dmax, int), \
            "'dmax' doit etre int, pas %s." % type(dmax).__name__
        assert dmin <= dmax, "'dmin' doit etre <= 'dmax'. " \
            "Les valeurs valent respectivement %d et %d." % (dmin, dmax)
        assert dmin != 0 or dmax != 0, \
            "Un voisin a une distance de 0 a peu d'interet."

        vertex = self.__getitem__(vertex, is_vertex=True)
        
        # Cas d'un graphe non oriante, avec des aretes.
        if self.directed == False:
            dmin, dmax = abs(dmin), abs(dmax)
            dmin, dmax = min(dmin, dmax), max(dmin, dmax)
            layers = [{vertex}]
            for _ in range(dmax):
                layers.append({
                    v2 for v1 in layers[-1]
                    for v2 in self.successors(v1)
                    if v2 not in layers[-1]})
                layers[-1] = layers[-1].union(layers[-2])
            return layers[dmax] - layers[max(0, dmin-1)]

        # Cas d'un graphe oriante, avec des arcs.
        if (dmin == 0 or dmin == 1) and dmax == 1:
            return self.successors(vertex)
        if dmin == -1 and (dmax == 0 or dmax == -1):
            return self.predecessors(vertex)
        if dmin > 1:
            return {node2 for node1 in self.successors(vertex)
                    for node2 in self.neighbors(node1, dmin=dmin-1, dmax=dmax-1)}
        if dmax < -1:
            return {node2 for node1 in self.predecessors(vertex)
                for node2 in self.neighbors(node1, dmin=dmin+1, dmax=dmax+1)}
        if (dmin == 0 or dmin == 1) and dmax > 1:
            return self.successors(vertex) | self.neighbors(vertex, dmin=2, dmax=dmax)
        if dmin < -1 and (dmax == 0 or dmax == -1):
            return self.predecessors(vertex) | self.neighbors(vertex, dmin=dmin, dmax=-2)
        if dmin <= -1 and dmax >= 1:
            return self.neighbors(vertex, dmin=dmin, dmax=0) \
                 | self.neighbors(vertex, dmin=0, dmax=dmax)

    def degree(self, vertex):
        """
        |============================|
        | Renvoi le degres du noeud. |
        |============================|

        * Prend en compte la multiplicite des aretes et des arcs.
        * Complexite en O(1).

        entree
        ------
        :param vertex: De quoi identifier le noeud concidere.

        sortie
        ------
        :return: 2 numbers, the first shows the in (enters),
            the second number shows the out (exits). in/out.
            1 numbers if the graph is not oriented.
        :rtype: (int, int) or int
        """
        vertex = self.__getitem__(vertex, is_vertex=True)

        # On utilise pas self.predecessors et self.successors
        # Car ces methodes ne prenent pas en compte la multiplicite.
        if self.directed:
            n_predec = len(self.graph[vertex.n][1])
            n_succes = len(self.graph[vertex.n][0])
            return n_predec, n_succes
        return len(self.graph[vertex.n])

    def adjacency_matrix(self):
        """
        |==================================|
        | Retourne la matrice d'adjacence. |
        |==================================|

        * Complexite en O(n), 'n' etant le nombre d'arcs dans le graphe.
        * Les indices ne sont pas directement l'id des noeuds mais la position
        des id dans la liste triee dans l'ordre.
        * Enregistre la matrice si il y a suffisement de RAM libre.

        sortie
        ------
        :return: It's the square matrix, if there's a
            connection between two vertices,
            we assign the value 1, else 0.
        :rtype: np.ndarray
        """
        # Verification preliminaire.
        if "adjacency_matrix" in self.properties:
            return self.properties["adjacency_matrix"]
        if not len(self):
            raise ValueError("La matrice d'adjacence ne peut pas"
                "etre calculee sur un graphe vide.")
        
        # Creation de la matrice.
        table = {v_id: i for i, v_id in enumerate(sorted(self.id2vertex.keys()))}
        matrix = np.zeros((len(self), len(self)), dtype=np.int8) # La matrice est vide
        for s in self.get_segments(): # Puis on la rempli au fur a mesure.
            matrix[table[s.vs.n], table[s.vd.n]] = 1

        # Enregistrement.
        try:
            import psutil
        except ImportError:
            pass
        else:
            if psutil.virtual_memory().available - matrix.nbytes > 1e9: # Si il reste plus de 1 Go de mamoire libre:
                self.properties["adjacency_matrix"] = matrix
            del psutil
        
        return matrix

    def chromatic_index(self):
        """
        |=====================================|
        | Majoration de l'indice chromatique. |
        |=====================================|
        
        * L'indice chromatique d'un graphe est le plus petit nombre k pour
        lequel il existe une k-coloration des aretes.

        * Colorie le graphe pour trouver l'indice, mais le coloriage
        n'est pas toujours parfait.

        :seealso: Base sur 'self.dsatur'.

        sortie
        ------
        :return: Le nombre de couleur differentes.
        :rtype: int
        """
        if "chromatic_index" not in self.properties:
            self.properties["chromatic_index"] = len({color for _, color in self.dsatur()})
        return self.properties["chromatic_index"]

    # Algorithmes.

    def bfs(self, vertex, *, kind="b"):
        """
        |====================================|
        | Algorithme de parcours en largeur. |
        |====================================|

        * Complexite en O(s + a), avec s le nombre de
        sommets et a le nombre d'arcs.

        entree
        ------
        :param vertex: De quoi identifier le noeud concidere.
        :param kind: Ne pas toucher, c'est pour eviter
            la redondance avec self.dfs

        sortie
        ------
        :return: Chaque sommet parcouru.
        :rtype: Vertex
        """
        if isinstance(vertex, int):
            s_init = self[(vertex, "vertex")]
        else:
            s_init = self[vertex]

        key = f"{kind}fs"
        if self.properties.get((key, s_init.n), [False])[0]:
            yield from (id2vertex[i] for i in self.properties[(key, s_init.n)][1:])
        else:
            # Preparation du terrain.
            for v in self.get_vertices():
                v.flags[key] = False
            self.properties[(key, s_init.n)] = [False] # Pour etre certain que l'algo aille jusqu'au bout.

            # C'est parti
            q = queue.Queue() if kind == "b" else queue.LifoQueue()
            q.put(s_init)
            s_init.flags[key] = True
            while not q.empty():
                s = q.get_nowait()
                self.properties[(key, s_init.n)].append(s)
                yield s
                for neighbor in self.successors(s):
                    if not neighbor.flags[key]: # Si le noeud n'est pas marque.
                        q.put(neighbor)
                        neighbor.flags[key] = True

            self.properties[(key, s_init.n)][0] = True

    def dfs(self, vertex):
        """
        |======================================|
        | Agorithme de parcours en profondeur. |
        |======================================|

        :seealso: self.bfd
        """
        yield from self.bfd(vertex, kind="d")

    def dsatur(self):
        """
        |====================|
        | Colorie le graphe. |
        |====================|

        * Attribu une couleur a chaque sommet.
        * tente de minimiser les nombre de couleurs.
        * Resultat exact pour le graphes pour les graphes suivants:
            - graphes bipartis
            - graphes-cycle
            - graphes monocycliques
            - graphes bicycliques
            - arbres
            - colliers
            - graphes-cactus
        * Base sur l'heuristique DSATUR.
        * Complexite polynomiale

        sortie
        ------
        :return: Cede les couples (sommet, couleur)
        :rtype: (Vertex, int)

        Example
        -------
        >>> from raisin.graph.basegraph import *
        >>> g = BaseGraph({(1, 0), (2, 0), (3, 0), (4, 0)})
        >>> [(v.n, c) for v, c in g.coloration()]
        [(0, 0), (1, 1), (2, 1), (3, 1), (4, 1)]
        >>> g.add_segments((1, 2), (2, 4), (4, 3), (3, 1))
        >>> list(g.coloration())
        [(Vertex(n=0), 0), (Vertex(n=1), 1), (Vertex(n=2), 2), (Vertex(n=3), 2), (Vertex(n=4), 1)]
        >>>
        """
        def choose(dsats, sorted_vertex):
            """
            Cherche un id de noeud present dans 'dsats' tel que:
            - dsat(noeud) maximum
            En cas d'egalite:
            - degre(noeud) maximum
            En cas d'egalie, un au pif.
            """
            dsat_max = max(dsats.values()) # La valeur maximale
            candidates = {v_id for v_id, dsat in dsats.items() if dsat == dsat_max}
            if len(candidates) == 1:
                return candidates.pop()
            for v_id in sorted_vertex:
                if v_id in candidates:
                    return v_id

        def update_dsats(v_id, colors, dsats):
            """
            Met a jour les valeurs de dsats pour les voisins de 'v_id'.
            """
            neighbors_id = {n.n for n in self.neighbors(v_id) if n.n in dsats} # Les voisins.
            for neighbor_id in neighbors_id:
                dsats[neighbor_id] = len({colors[n.n] for n in self.neighbors(neighbor_id) if n.n in colors})
            return dsats

        def find_color(v_id, colors):
            """
            Recherche la couleur la plus basse en considerant
            la couleur des voisins.
            """
            neighbors_colors = {colors[n.n]
                for n in self.neighbors(v_id) if n.n in colors} # Les voisins.
            color = 0
            while color in neighbors_colors:
                color += 1
            return color

        if self.properties.get("colors", [False])[0]:
            yield from self.properties["colors"][1:]
        else:
            self.properties["colors"] = [False] # Couple 'sommet', couleur.
            
            # Initialisation.
            sorted_vertex = sorted(self.id2vertex.keys(),
                key=lambda v_id: len(self.neighbors(v_id)),
                reverse=True)
            dsats = {v_id: 0 for v_id in self.id2vertex.keys()} # A chaque id de sommet, associ le DSAT.
            colors = {} # A chaque id de sommet, associ la couleur

            while dsats: # Tant que tous les noeuds n'ont pas une couleur.
                vertex_id = choose(dsats, sorted_vertex) # On choisi le meilleur noeud possible.
                colors[vertex_id] = find_color(vertex_id, colors) # On trouve la couleur minimum qu'il peut avoir.
                del dsats[vertex_id] # On retire ce noeud des noeuds a colorier.
                dsats = update_dsats(vertex_id, colors, dsats) # On met a jour le 'dsat' des voisins.
                
                self.properties["colors"].append((self.id2vertex[vertex_id], colors[vertex_id]))
                yield self.properties["colors"][-1]

            self.properties["colors"][0] = True # On marque le fait que l'algo est termine.

    def tsp(self):
        """
        |============================|
        | Traveling Salesman Problem |
        |============================|

        * Etant donne un graphe complet pondere, trouver un cycle
        hamiltonien de poids minimum.

        sortie
        ------
        :return: Le chemin.
        """
        raise NotImplementedError

class FrozenGraph(BaseGraph):
    """
    |==============================|
    | Graphe fige, non modifiable. |
    |==============================|
    """
    def __delitem__(self, key):
        """
        Method unusable, the graph is frozen! 
        """
        raise AttributeError("The graph is frozen.")

    def add_vertex(self, vertex):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_vertices(self, *vertices):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_segment(self, segment):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_arrow(self, arrow):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_edge(self, edge):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_segments(self, *segments):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_arrows(self, *arrows):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def add_edges(self, *edges):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def del_vertex(self, vertex):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def del_segment(self, segment):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def del_arrow(self, arrow):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

    def del_edge(self, edge):
        """
        Method unusable, the graph is frozen!
        """
        raise AttributeError("The graph is frozen.")

def random_graph(n_vertices=20, n_segments=30):
    """
    |=================================|
    | Genere un graphe aleatoirement. |
    |=================================|

    entree
    ------
    :param n_vertices: Nombre de noeud generes.
    :type n_vertices: int
    :param n_segment: Nombre de segment genere.
    :type n_segment: int

    sortie
    ------
    :return: Un graphe basique cree aleatoirement.
    :rtype: Graph
    """
    assert isinstance(n_vertices, int), \
        "'n_vertices' have to bet integer. Not %s." \
        % type(n_vertices).__name__
    assert isinstance(n_segments, int), \
        "'n_segments' have to bet integer. Not %s." \
        % type(n_segments).__name__
    assert n_vertices >= 0, \
        "Il ne peut pas y avoir %d sommets." % n_vertices
    assert n_segments >= 0, \
        "Il ne peut pas y avoir %d aretes." % n_segments

    vertices = [mod_vertex.Vertex() for _ in range(n_vertices)]
    segments = set()

    while len(segments) < n_segments:
        segments.add((
            random.choice(vertices),
            random.choice(vertices)))
    return BaseGraph(segments)
