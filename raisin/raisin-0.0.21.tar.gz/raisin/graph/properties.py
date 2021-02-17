#!/usr/bin/env python3

"""
|=======================================|
| Recherche les proprietes d'un graphe. |
|=======================================|

* La classe a besoin d'etre initialisee par BaseGraph,
Elle ne s'auto-suffit pas.
"""

import queue

import numpy as np


class Properties:
    """
    |======================================================|
    | Permet d'etendre BaseGraph pour y ajouter des        |
    | methodes de reconaissance de proprietes specifiques. |
    |======================================================|
    """
    def is_acyclic(self):
        """
        |=========================================|
        | Regarde si le graphe contient un cycle. |
        |=========================================|

        * Cherche juste si il n'existe aucun chemins partant
        d'un noeud et se terminant sur le meme noeud.
        * Si un arc part d'un noeud et atteind le meme noeud,
        le graphe n'est pas considere comme acyclique.
        * Pour qu'on graphe soit acyclique, l faut qu'il posede au moin un noeud.

        sortie
        ------
        :return: False if contains a cycle in the path, False owever.
        :rtype: boolean

        Example
        -------
        >>> from raisin.graph.basegraph import *
        >>> g = BaseGraph({(1, 0), (2, 0), (3, 0), (4, 0)})
        >>> g.is_acyclic()
        True
        >>> g.add_segments((1, 2), (2, 4), (4, 3), (3, 1))
        >>> g.is_acyclic()
        False
        >>> 
        """
        if "is_acyclic" in self.properties:
            return self.properties["is_acyclic"]
        if not len(self):
            return False

        # Preparation du terrain.
        for v in self.get_vertices():
            v.flags["acyclic"] = 0
        q = queue.Queue()

        fathers = {} # Les parents pour eviter d'osciller sur une arete.
        for i, vertex in enumerate(self.id2vertex.values()): # Noeud de depart
            if vertex.flags["acyclic"]: # Si le noeud est deja marque,
                continue # on n'explore pas ces voisins.
            q.put(vertex)
            vertex.flags["acyclic"] = i + 1
            while not q.empty():
                vertex = q.get_nowait()
                for neighbor in self.successors(vertex):
                    fathers[neighbor] = vertex
                    if neighbor.flags["acyclic"] == i + 1: # Si le voisin est marque.
                        if self.directed == False and neighbor == fathers[vertex]:
                            continue
                        self.properties["is_cyclic"] = False # C'est qu'il y a un cycle.
                        return False
                    elif not neighbor.flags["acyclic"]:
                        q.put(neighbor)
                        neighbor.flags["acyclic"] = i + 1
        self.properties["is_cyclic"] = True
        return True

    def is_arborescence(self):
        """
        |============================|
        | Recherche si le graphe est |
        | un arbre avec une racine.  |
        |============================|

        * an arborescence is a directed graph in which, for a vertex u called
        the root and any other vertex v, there is exactly one directed path
        from u to v. An arborescence is thus the directed-graph form of a
        rooted tree, understood here as an undirected graph.
        * Il doit posseder au moin 2 noeuds.

        sortie
        ------
        :return: True si l'arbre est une arborescence, False sinon.
        :rtype: boolean
        """
        if "is_arborescence" in self.properties:
            return self.properties["is_arborescence"]

        if len(self) < 2 or self.directed == False:
            self.properties["is_arborescence"] = False
            return False
        
        root = None
        for vertex_id, (childs_id, fathers_id) in self.graph.items():
            if len(fathers_id) > 1: # Chaque noeud ne doit avoir qu'un pere.
                self.properties["is_arborescence"] = False
                return False
            if len(fathers_id) == 0: # Si on est a la racine.
                if root is not None: # Il ne doit y avoir qu'une racine.
                    self.properties["is_arborescence"] = False
                    return False
                root = vertex_id
        self.properties["root_id"] = root
        self.properties["is_arborescence"] = True
        return True

    def is_biclique(self):
        """
        |======================================|
        | Recherche si le graphe est biclique. |
        |======================================|

        * Synonym for complete bipartite graph.

        sortie
        ------
        :return: True si le graphe est biclique, False sinon.
        :rtype: boolean
        """
        if "is_biclique" in self.properties:
            return self.properties["is_biclique"]

        if not self.is_bipartite():
            self.properties["is_biclique"] = False
            return False

        if self.directed: # Pas certain ici.
            self.properties["is_biclique"] = False
            return False

        families = {}
        for vertex, color in self.dsatur():
            families[color] = families.get(color, set()).add(vertex)
        x, y = families.values() # On separe les noeuds en 2 familles.
        self.properties["is_biclique"] = (
            all(self.degree(v) == len(y) for v in x)
            and all(self.degree(v) == len(x) for v in y))
        return self.properties["is_biclique"]

    def is_bipartite(self):
        """
        |===============================================|
        | Recherche si le graphe est un graphe biparti. |
        |===============================================|

        * Un graphe est biparti si ses sommets peuvent etre divises en deux
        ensembles X et Y, de sorte que toutes les aretes du graphe relient un
        sommet dans X a un sommet dans Y.
        Les arbres sont des exemples des graphes bipartis.
        * Un graphe biparti est un graphe simple.

        sortie
        ------
        :return: True si l'arbre est biparti, False sinon.
        :rtype: boolean
        """
        if "is_bipartite" in self.properties:
            return self.properties["is_bipartite"]
        
        if len(self) < 2 or not self.is_simple():
            self.properties["is_bipartite"] = False
            return False
        
        self.properties["is_bipartite"] = (self.chromatic_index() == 2)
        return self.properties["is_bipartite"]

    def is_biregular(self):
        """
        |========================================|
        | Recherche si le graphe est biregulier. |
        |========================================|

        * A biregular graph is a bipartite graph in which there are only two
        different vertex degrees, one for each set of the vertex bipartition.

        sortie
        ------
        :return: True si le graphe est biregulier, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_cactus(self):
        """
        |==============================================|
        | Rechreche si le graphe est un graphe cactus. |
        |==============================================|

        * A cactus graph, cactus tree, cactus, or Husimi tree is a connected
        graph in which each edge belongs to at most one cycle. Its blocks are
        cycles or single edges. If, in addition, each vertex belongs to at
        most two blocks, then it is called a Christmas cactus.

        sortie
        ------
        :return: True si l'arbre est un cactus, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_caterpillar(self):
        """
        |========================================|
        | Recherche si le graphe est un collier. |
        |========================================|

        * A caterpillar tree or caterpillar is a tree in which the internal
        nodes induce a path.

        sortie
        ------
        :return: True si le graphe est un colier, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_chordal(self):
        """
        |=====================================|
        | Regarde si le graphe est triangule. |
        |=====================================|

        * Un graphe est triangule si tous ses cycles de plus de 3 sommets
        contiennent au moins une corde (arete reliant deux sommets non
        adjacents d'un cycle).

        sortie
        ------
        :return: True si le graphe est triangule, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_circle(self):
        """
        |=====================================|
        | Regarde si le graphe est un cercle. |
        |=====================================|

        * Un graphe est un graphe cercle si le degre des chaque
        sommet vaut 2 et que il y a un seul cycle.

        sortie
        ------
        :return: True si le graphe est cerle, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_complete(self):
        """
        |====================================|
        | Recherche si le graph est complet. |
        |====================================|

        * Un graphe est dit complet si pour toutes paire de sommets (x, y),
        il existe au moins un arc de la forme (x, y) ou (y, x).
        * Dans les pairs (x, y), x != y.
        * Il doit donc y avoir au moins 2 noeuds dans le graphe.
        * Pour etre complet, le graphe doit etre simple.

        sortie
        ------
        :return: True si le graphe est complet, False sinon.
        :rtype: boolean
        """
        if "is_complete" in self.properties:
            return self.properties["is_complete"]
        
        if len(self) < 2 or not self.is_simple():
            self.properties["is_complete"] = False
            return False
        
        adj_mat = self.adjacency_matrix()
        self.properties["is_complete"] = (
            adj_mat + adj_mat.transpose()
            + np.diag(np.ones(len(self)))
            ).all()
        return self.properties["is_complete"]

    def is_connected(self):
        """
        |=====================================|
        | Recherche si le graphe est connexe. |
        |=====================================|

        * Un graphe connexe est un graphe dans lequel chaque paire de sommets
        est reliee par une chaine.
        * Pour un graphe oriante on dit qu'il est fortement connexe si pour
        toute parie de sommet (x, y), il existe un chemin allant de x a y
        et de y a x. Il est faiblement connexe si il existe un chemin
        allant de x a y ou bien de y a x.

        sortie
        ------
        :return: True si le graphe est connexe, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_eulerian(self):
        """
        |====================================|
        | Cherche si le graphe est eulerien. |
        |====================================|

        * un graphe est eulerien (ou semi-eulerien) s'il est possible de dessiner
        le graphe sans lever le crayon et sans passer deuxfois sur la meme arete.

        sortie
        ------
        :return: True si le graphe est eulerien, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_forest(self):
        """
        |=====================================|
        | Cherche si le graphe est une foret. |
        |=====================================|

        * A forest is an undirected graph without cycles (a disjoint union of
        unrooted trees), or a directed graph formed as a disjoint union of
        rooted trees.

        sortie
        ------
        :return: True si le graphe est une foret, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_hamiltonian(self):
        """
        |=======================================|
        | Cherche si le graphe est hamiltonien. |
        |=======================================|

        * Un graphe est dit hamiltonien s'il possede un cycle hamiltonien.
        * On appelle cycle hamiltonien d'un graphe G un cycle passant une
        et une seule fois par chacun des sommets de G.

        sortie
        ------
        :return: True si le graphe est hamiltonien, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_multigraph(self):
        """
        |===============================================|
        | Cherche si il y a plusieurs arcs en paralele. |
        | Ou si un arc relie un sommet a lui-meme.      |
        |===============================================|

        * Un graphe est dit multigraph si un sommet est relie
        a lui-meme ou si plusieurs arcs relient les meme sommets.

        sortie
        ------
        :return: True si le graph est un multigraphe, False sinon.
        :rtype: boolean
        """
        if "is_multigraph" in self.properties:
            return self.properties["is_multigraph"]

        # On regarde tous les arcs qui partent pour chaque noeud.
        for node_id, (segments_id, _) in self.graph.items():
            nodes_id = [self.id2segment[segment_id].vd.n for segment_id in segments_id] # Tous les noeuds pointes.
            # Si un noeud de destination est atteind plusieurs fois.
            # C'est que c'est un multigraphe.
            set_nodes_id = set(nodes_id)
            if len(nodes_id) != len(set_nodes_id) or node_id in set_nodes_id: # Ou qu'un sommet est relie a lui-meme.
                self.properties["is_multigraph"] = True
                return True

        self.properties["is_multigraph"] = False
        return False

    def is_planar(self):
        """
        |======================================|
        | Recherche si le graphe est planaire. |
        |======================================|

        * Un graphe planaire est un graphe que l'on peut dessiner sur une
        surface plate sans que ses aretes se croisent. Les graphes que l'on
        ne peut pas dessinersans croisement sont dits nonplanaires.

        sortie
        ------
        :return: True si le graphe est planaire, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_regular(self):
        """
        |====================================|
        | Cherche si le graphe est regulier. |
        |====================================|

        * Un graphe est regulier si les degres des
        sommets sont tous egaux.

        sortie
        ------
        :return: True si le graphe est regulier, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_semi_eulerian(self):
        """
        |==========================================|
        | Recherche si le graphe est semi-eulerien.|
        |==========================================|

        * Un graphe est semi-eulerien s'il est possible de trouver une chaine
        passant une et une seule fois par toutes les aretes, et s'il n'est
        pas eulerien.

        sortie
        ------
        :return: True si le graphe est semi-eulerien, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_semi_hamiltonian(self):
        """
        |=============================================|
        | Recherche si le graphe est semi-hamiltonien.|
        |=============================================|

        * Un graphe est semi-hamiltonien s'il est possible de trouver une chaine
        passant une et une seule fois par tous les sommets, et s'il n'est
        pas hamiltonien.

        sortie
        ------
        :return: True si le graphe est semi-hamiltonien, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_simple(self):
        """
        |====================================|
        | Recherche si le graphe est simple. |
        |====================================|

        * Un graphe est dit simple, s'il ne contient pas de boucle et s'il n'y a
        pas plus d'une arete reliant deux memes sommets.

        :seealso: Negation of 'self.is_multigraph'.

        sortie
        ------
        :return: True si le graphe est simple, False sinon.
        :rtype: boolean
        """
        return not self.is_multigraph()

    def is_strongly_connected(self):
        """
        |===============================================|
        | Recherche si le graphe est fortement connexe. |
        |===============================================|
        
        * Un graphe oriente (digraphe) est fortement connexe s'il existe un
        chemin du sommet a au sommet b et du sommet b au sommet a, quels que
        soient les sommets representes par a et b dans le graphe.

        sortie
        ------
        :return: True si les graphe est fortement connexe, Fasle sinon.
        :rtype: boolean
        """
        raise NotImplementedError

    def is_tree(self):
        """
        |====================================|
        | Cherche si le graphe est un arbre. |
        |====================================|

        * On appelle arbre tout graphe connexe sans cycle.

        sortie
        ------
        :return: True si le graphe est un arbre, False sinon.
        :rtype: boolean
        """
        raise NotImplementedError
