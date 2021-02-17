#!/usr/bin/env python3

"""
|=================================|
| Permet de representer un graphe |
| de facon graphique, visuelle.   |
|=================================|

* Interagit avec matplotlib.
* La classe a besoin d'etre initialisee par BaseGraph,
Elle ne s'auto-suffit pas.
"""

import os
import sys
import time

import numpy as np

from ..errors import *
from ..tools import temprep
from . import segment as mod_segment
from . import vertex as mod_vertex


class Display:
    """
    |===========================================|
    | Permet d'etendre BaseGraph pour y ajouter |
    | des methodes d'affichage.                 |
    |===========================================|
    """
    def _get_dot(self):
        """
        |====================================|
        | Genere une instance de graphe dot. |
        |====================================|

        * Utilise le module ``graphviz``.

        Returns
        -------
        :return: Une instance de graphe du module ``graphviz``.
        :rtype: graphviz.Graph or graphviz.Digraph
        :raises ImportError: Si le module ``graphviz`` n'est pas installe.
        """
        try:
            import graphviz
        except ImportError as e:
            raise ImportError("Please install 'graphviz'.",
                "$ sudo %s -m pip install graphviz" % sys.executable
                ) from e

        if self.directed == False:
            graph = graphviz.Graph(comment=self.comment)
        else:
            graph = graphviz.Digraph(comment=self.comment)
        del graphviz # Pour liberer de la memoire.

        for vertex in self.get_vertices():
            if "facecolor" in vertex.flags and "edgecolor" not in vertex.flags:
                graph.node(str(vertex.n),
                    label=vertex.name if vertex.name else None,
                    style="radial",
                    fillcolor=vertex.flags["facecolor"])
            elif "facecolor" not in vertex.flags and "edgecolor" in vertex.flags:
                graph.node(str(vertex.n),
                    label=vertex.name if vertex.name else None,
                    color=vertex.flags["edgecolor"])
            elif "facecolor" in vertex.flags and "edgecolor" in vertex.flags:
                graph.node(str(vertex.n),
                    label=vertex.name if vertex.name else None,
                    style="filled",
                    fontcolor=vertex.flags["edgecolor"], # Couleur du text
                    color=vertex.flags["facecolor"])
            else:
                graph.node(str(vertex.n),
                    label=vertex.name if vertex.name else None)

        for segment in self.get_segments():
            graph.edge(str(segment.vs.n), str(segment.vd.n),
                label=segment.name if segment.name else None,
                color=segment.flags.get("color", None))

        return graph

    def __str__(self):
        """
        |==============================|
        | Affichage lisible du graphe. |
        |==============================|
        """
        try:
            graph = self._get_dot()
        except ImportError:
            import pprint
            string = pprint.pformat(self.__repr__(self))[2:-2]
            del pprint
            return string
        else:
            return graph.__str__()

    def save(self, filename, *, use_graphviz=False):
        """
        |==========================|
        | Enregistre le graphe     |
        | dans un format standard. |
        |==========================|

        Parameters
        ----------
        :param filename: Le nom du fichier avec son extension.
        :type filename: str
        :param use_graphviz: Permet de forcer l'utilisation de ``graphviz``.
            True: Utilise ``graphviz``, echoue si cela ne fonctionne pas.
            False: Utilise d'abord ``graphviz`` puis utilise
                ``matplotlib`` en cas d'echec.
        :type use_graphviz: boolean

        Returns
        -------
        :return: The (possibly relative) path of the rendered file.
        :rtype: str
        :raises ImportError: Si le module ``graphviz`` n'est pas installe.
        :raises ValueError: If the format extension is not known.
        :raises graphviz.ExecutableNotFound: If the Graphviz executable is not found.
        :raises subprocess.CalledProcessError: If the exit status is non-zero.
        """
        assert isinstance(use_graphviz, bool), \
            "'use_graphviz' has to be a boolean, not a %s." \
            % type(use_graphviz).__name__
        assert isinstance(filename, str), \
            "'filename' has to be of str type; not %s." \
            % type(filename).__name__
        assert "." in filename, "Missing the filename extension."
        extension = filename.split(".")[-1].lower()
        basename = os.path.basename(filename)[:-len(extension)-1]
        directory = os.path.dirname(filename) if os.path.dirname(filename) else None
        assert directory is None or os.path.exists(directory), \
            "Le repertoire %s n'existe pas." % repr(directory)

        if use_graphviz:
            graph = self._get_dot()
            graph.attr(dpi="600")
            import graphviz
            try:
                return graph.render(
                    filename=basename,
                    directory=directory,
                    view=False,
                    format=extension,
                    cleanup=True)
            except ValueError as e:
                raise ValueError("Les extensions supportees sont %s." \
                    % repr(graphviz.FORMATS)) from e
            except graphviz.backend.ExecutableNotFound as e:
                raise RuntimeError("veuillez installer graphviz "
                    "'$ sudo apt install graphviz'.") from e
            finally:
                del graphviz
        else:
            try:
                self.save(filename, use_graphviz=True)
            except Exception:
                import matplotlib.pyplot as plt
                self.plot(use_graphviz=False)
                plt.savefig(filename)
                plt.clf()
                return filename

    def _id2color(self, color_id):
        """
        Associe une couleur '#rvb' a chaque entier naturel.

        * Ne fait pas de verifications.
        """
        if color_id == 0:
            return "#ee0000"
        if color_id == 1:
            return "#00bb00"
        if color_id == 2:
            return "#0000ff"
        if color_id == 3:
            return "#ffff00"
        if color_id == 4:
            return "#ff00ff"
        if color_id == 5:
            return "#00ffff"
        return "#%06x" % (hash((color_id, )) % 16777216)

    def _place(self):
        """
        S'assure que chaque noeuds aient un couple de
        coordonees (x, y) definis.
        """
        DISP = 1 # Fraction de dispertion.
        CROS = 50 # Fraction de croisement
        
        # Recherche des coordonnees deja existantes.
        x_set = {v.x for v in self.get_vertices() if v.x is not None}
        y_set = {v.y for v in self.get_vertices() if v.y is not None}
        xmin = min(x_set) if x_set else 0
        xmax = max(x_set) if x_set else 1
        ymin = min(y_set) if y_set else 0
        ymax = max(y_set) if y_set else 1
        if xmin == xmax:
            xmin -= 1
            xmax += 1
        if ymin == ymax:
            ymin -= 1
            ymax += 1

        # Recencement des noeuds ayant un mouvement de liberte.
        x_mobile = {v for v in self.get_vertices() if v.x is None}
        y_mobile = {v for v in self.get_vertices() if v.y is None}

        # Placement des sommets sur des cercles concentriques.
        for r, (v, _) in enumerate(self.dsatur()):
            cross_min = DISP + CROS
            theta_best = 0
            phi = np.random.uniform(0, 2*np.pi)
            r_eq = np.log(1 + 3*r)
            for theta in np.linspace(phi, 2*np.pi + phi, num=64, endpoint=False):
                v.x = r_eq*np.cos(theta) if v in x_mobile else v.x
                v.y = r_eq*np.sin(theta) if v in y_mobile else v.y
                try:
                    cross = CROS*self.cross_density(v) + DISP*self.dispersion()
                except AmbiguousError:
                    continue
                if cross < cross_min:
                    cross_min = cross
                    theta_best = theta
                    if cross == 0:
                        break
            v.x = r_eq*np.cos(theta_best) if v in x_mobile else v.x
            v.y = r_eq*np.sin(theta_best) if v in y_mobile else v.y

    def _normalize(self):
        """
        Ramene les points dans l'intervalle [0, 1]*[0, 1].

        * Il faut que tous les points aients des coordonnes non nulles.
        * Ne fait aucune verification.
        * Ne fait pas de sauvegarde des ancienes coordonees.
        """
        # Cas particuliers.
        if len(self) == 0:
            return
        if len(self) == 1:
            self.get_vertices().pop().x = 0
            self.get_vertices().pop().y = 0

        # Recherche min max.
        x_set = {v.x for v in self.get_vertices()}
        y_set = {v.y for v in self.get_vertices()}
        xmin, xmax = min(x_set), max(x_set)
        ymin, ymax = min(y_set), max(y_set)

        # Deplacement afine des points (homotecie + translation).
        for v in self.get_vertices():
            if xmin == xmax:
                v.x = 0
            else:
                v.x = (v.x - xmin)/(xmax - xmin)
            if ymin == ymax:
                v.y = 0
            else:
                v.y = (v.y - ymin)/(ymax - ymin)

    def _plot_vertex(self, ax, plt, vertex, *,
        radius=None, edgecolor=None, facecolor=None, legend=True):
        """
        |===============================|
        | Ajoute le noeud au graphique. |
        |===============================|

        * Ne fait pas de verification.

        Parameters
        ----------
        :param ax: Figure matplotlib.
        :type ax: matplotlib.axes._subplots.AxesSubplot
        :param plt: C'est l'objet matplotlib.pyplot .
        :type plt: matplotlib.pyplot
        :param vertex: Le noeud a afficher, il doit etre positionne.
        :type vertex: Vertex
        :param radius: Rayon absolu. si None, tente de recuperer
            cette valeur dans vertex.flags["radius"]
        :type radius: float
        :param edgecolor: Couleur du contour. Si None, tente de recuperer
            cette valeur dans vertex.flags["edgecolor"]
        :type edgecolor: str
        :param facecolor: Couleur de remplissage. Si None, tente de recuperer
            cette valeur dans vertex.flags["facecolor"]
        :param legend: Gere l'affichage du nom / l'id du noeud.
            True: Ajoute le text dans le noeud.
            False: Laise le noeud vide
        :type legend: boolean
        """
        circle = plt.Circle(([vertex.x], [vertex.y]),
            radius=(radius if radius else vertex.flags.get("radius", 0.04)), # Rayon absolu.
            alpha=0.8,                                      # Niveau de transparence 1 -> opaque 0 -> transparent.
            edgecolor=(edgecolor if edgecolor else
                vertex.flags.get("edgecolor", "black")),    # Couleur du contour.
            facecolor=(facecolor if facecolor else
                vertex.flags.get("facecolor", "white")),    # Couleur de font.
            linewidth=1.5)                                  # Epaisseur du contour (en pxl)
        if legend:
            text = str(vertex.n)
            if vertex.name:
                text += "\n%s" % vertex.name
            plt.text(vertex.x, vertex.y,
                text,
                horizontalalignment="center",
                verticalalignment="center")
        ax.add_patch(circle)

    def _plot_segment(self, ax, segment, *, color=None, legend=True):
        """
        |=====================================|
        | Ajoute un arc / arete au graphique. |
        |=====================================|

        * Ne fait pas de verifications.

        Parameters
        ----------
        :param ax: Figure matplotlib.
        :type ax: matplotlib.axes._subplots.AxesSubplot
        :param segment: L'arete ou l'arc a afficher,
            ces noeuds doivent etre positiones.
        :type segment: Arrow ou Edge
        :param color: Couleur du segment. Si None, tente de recuperer
            cette valeur dans segment.flags["color"]
        :type color: str
        :param legend: Gere l'affichage du nom / l'id du noeud.
            True: Ajoute le text dans le noeud.
            False: Laise le noeud vide
        :type legend: boolean
        """
        r_vs = segment.vs.flags.get("radius", 0.04)
        r_vd = segment.vd.flags.get("radius", 0.04)

        # Calcul des vrais points d'atache.
        p_s = np.matrix([[segment.vs.x],
                         [segment.vs.y]],
                         dtype=float) # Centre du noeud de depart.
        p_d = np.matrix([[segment.vd.x],
                         [segment.vd.y]],
                         dtype=float) # Centre du noeud d'arrive.
        v = p_d - p_s # Vecteur directeur du segment.
        v /= np.linalg.norm(v) # On norme le vecteur.
        p_a_s = p_s + v*r_vs # Point d'attache source.
        p_a_d = p_d - v*r_vd # Point d'attache destination.

        # Affichage du segment.
        color = color if color else segment.flags.get("color", "black")
        ax.plot([p_a_s[0, 0], p_a_d[0, 0]], [p_a_s[1, 0], p_a_d[1, 0]],
            color=color, alpha=0.8)

        # Affichage de la pointe.
        if type(segment) == mod_segment.Arrow:
            rot = np.matrix([[v[0, 0], -v[1, 0]],
                             [v[1, 0],  v[0, 0]]],
                             dtype=float)
            fleche1 = 0.02*np.matrix([[-np.sqrt(3)/2],
                                      [ 0.5         ]],
                                      dtype=float)
            fleche2 = 0.02*np.matrix([[-np.sqrt(3)/2],
                                      [-0.5         ]],
                                      dtype=float)
            fleche1 = p_a_d + rot*fleche1
            fleche2 = p_a_d + rot*fleche2
            x = [fleche1[0, 0], p_a_d[0, 0], fleche2[0, 0]]
            y = [fleche1[1, 0], p_a_d[1, 0], fleche2[1, 0]]
            ax.plot(x, y, color=color, alpha=0.8)

        # Affichage du texte.
        if legend:
            if segment.name:
                position = .5*(p_a_s + p_a_d)
                theta = 180/np.pi * np.arccos(v[0, 0]) * (1 - 2*(v[1, 0] < 0))
                ax.text(position[0, 0], position[1, 0],
                    segment.name,
                    rotation=theta,
                    rotation_mode="anchor",
                    horizontalalignment="center",
                    verticalalignment="baseline",
                    color=color)

    def cross_density(self, mobile_vertex=None):
        """
        |==============================================================|
        | Estime le taux de croisement d'une representation du graphe. |
        |==============================================================|

        * Estime a quel point les segments du graphe s'intersectent.
        * Seul les noeuds dons les coordonnees sont fixees sont pris en compte.

        Parameters
        ----------
        :param mobile_vertex: Le noeud en cour d'etude.
            Si il est specifie, seul les intersections des
            aretes de ce noeud sont priss en compte.
        :type mobile_vertex: Vertex

        Returns
        -------
        :return: La densite de croisement du graphe normalisee.
            1 -> Completement entremele.
            0 -> Graphe deplie.
        :rtype: float
        """
        def cost(e1, e2):
            try:
                return e1 & e2
            except AmbiguousError:
                return 1
            except AttributeError:
                return 0

        assert mobile_vertex is None \
            or isinstance(mobile_vertex, mod_vertex.Vertex), \
            "'mobile_vertex' has to be an instance of Vertex, not %s." \
            % type(mobile_vertex).__name__

        segments = [s for s in self.get_segments() if 
            None not in [s.vs.x, s.vs.y, s.vd.x, s.vd.y]]
        
        if mobile_vertex is None: # Intersections du graph complet.
            if len(segments) <= 1:
                return 0
            return 2 * sum(cost(e1, e2)
                for i, e1 in enumerate(segments[:-1])
                for e2 in segments[i+1:]
                ) / (len(segments)*(len(segments)-1))

        # Les intersections avec un seul noeud.
        mobile_vertex = self.__getitem__(mobile_vertex, is_vertex=True)
        degree = (self.degree(mobile_vertex) if self.directed == False
             else sum(self.degree(mobile_vertex)))
        if not self.degree(mobile_vertex):
            return 0
        segments = [s for s in segments
            if s.vs is not mobile_vertex and s.vd is not mobile_vertex]
        if not segments:
            return 0
        return sum(cost(e1, e2)
            for e1 in self.get_segments(mobile_vertex)
            for e2 in segments) / (len(segments)*degree)

    def dispersion(self):
        """
        |===================================================|
        | Retourne une image de la dispertions des sommets. |
        |===================================================|

        * Ne prend en compte que des noeuds positiones.

        Returns
        -------
        :return: 0 si la dispertion est grande, 1 si les points sont mal places.
        :rtype: float
        """
        # Cas particuliers
        vertices = [v for v in self.get_vertices()
            if v.x is not None and v.y is not None]
        if len(vertices) <= 2:
            return 0

        # # Correlation spaciale.
        # x = [v.x for v in vertices]
        # y = [v.y for v in vertices]
        # ((_, correl), _) = np.corrcoef(x, y)
        # return abs(correl)

        distances = np.array(
            [(v1.x - v2.x)**2 + (v1.y - v2.y)**2
             for i, v1 in enumerate(vertices[:-1])
             for v2 in vertices[i+1:]],
            dtype=float)
        
        # # Ecart type des distance entre sommets.
        # return 2 * np.std(distances) / (distances.max() - distances.min())

        # Distance minimum.
        # return 1 / (distances.min() + 1)
        # return (distances.max() - distances.min()) / distances.max()
        return 1 - (distances.min() / np.median(distances))

    def plot(self, *, existing=False, coloring=True, legend=True, use_graphviz=True):
        """
        |================================================|
        | Prepare l'affichage du graphe avec matplotlib. |
        |================================================|

        * Apres l'apel de cette methode, il suffit de faire 'plt.show()'.

        Parameters
        ----------
        :param existing: Permet de ne pas ecraser une ficgure existante.
            True: Une figure est deja existante.
            False: Cree une nouvelle figure.
        :type existing: boolean
        :param coloring: Cherche a ajouter des couleur si elles n'y sont pas.
            True -> Colorie les objets sans couleurs.
            False -> Ne met que les couleurs definis dans les objets.
        :type coloring: boolean
        :param legend: Gere l'affichage du nom / l'id du noeud.
            True: Ajoute le text dans le noeud.
            False: Laise le noeud vide
        :type legend: boolean
        :param use_graphviz: Permet d'essayer d'afficher avec un otil exterieur.
            True: Tente d'abord d'afficher a l'aide de ``graphviz``.
            False: Dessine le graphe plus basiquement sans outils exterieur.
        :type use_graphviz: boolean

        Returns
        -------
        :return: La figure matplotlib.
        :rtype: matplotlib.figure.Figure
        """
        def manual_plot():
            """
            Affichage du graph a la main, sans
            outils exterieurs comme graphviz.
            """
            # Placement et affichage des sommets.
            self._place()
            self._normalize()
            for vertex in self.get_vertices():
                self._plot_vertex(ax, plt, vertex, legend=legend) 

            # Affichage des arcs / aretes.
            for segment in self.get_segments():
                self._plot_segment(ax, segment)

        def graphviz_plot():
            """
            Affichage du graph avec 'graphviz'.
            """
            filename = os.path.join(temprep, "graph.png")
            self.save(filename, use_graphviz=True)
            import matplotlib.image as img
            ax.imshow(img.imread(filename))
            os.remove(filename)
            del img

        assert isinstance(existing, bool), \
            "'existing' has to be a boolean, not a %s." \
            % type(existing).__name__
        assert isinstance(coloring, bool), \
            "'coloring' has to be a boolean, not a %s." \
            % type(coloring).__name__
        assert isinstance(legend, bool), \
            "'legend' has to be a boolean, not a %s." \
            % type(legend).__name__
        assert isinstance(use_graphviz, bool), \
            "'use_graphviz' has to be a boolean, not a %s." \
            % type(use_graphviz).__name__

        # Preparation de la figure.
        import matplotlib.pyplot as plt
        if existing:
            fig = plt.gcf()
            ax = fig.gca()
        else:
            fig, ax = plt.subplots()

        # Sauvegarde.
        for v in self.get_vertices():
            v.flags["old_x"] = v.x
            v.flags["old_y"] = v.y
            if "edgecolor" in v.flags:
                v.flags["old_edgecolor"] = v.flags["edgecolor"]
            if "facecolor" in v.flags:
                v.flags["old_facecolor"] = v.flags["facecolor"]

        # Colorisation des sommets.
        if coloring:
            edgecolors = {v.flags["edgecolor"] for v in self.get_vertices() if "edgecolor" in v.flags}
            edgecolor, i = "#000000", 0
            while edgecolor in edgecolors:
                edgecolor = self._id2color(i)
                i += 1
            for vertex in self.get_vertices():
                vertex.flags["edgecolor"] = vertex.flags.get("edgecolor", edgecolor)
            facecolors = {v.flags["facecolor"] for v in self.get_vertices() if "facecolor" in v.flags}
            if not facecolors:
                for vertex, color_id in self.dsatur():
                    vertex.flags["facecolor"] = self._id2color(color_id)
        
        # Remplissage de la figure matplotlib.
        if use_graphviz:
            try: # On tente d'abord d'utiliser 'graphviz' avant de la faire a la main.
                graphviz_plot()
            except Exception:  # Si l'affichage avec 'graphviz' a achouee.
                manual_plot()
        else:
            manual_plot()

        # Restauration de la sauvegarde.
        for v in self.get_vertices():
            v.x, v.y = v.flags["old_x"], v.flags["old_y"]
            del v.flags["old_x"], v.flags["old_y"]
            if "old_edgecolor" in v.flags:
                v.flags["edgecolor"] = v.flags["old_edgecolor"]
                del v.flags["old_edgecolor"]
            else:
                del v.flags["edgecolor"]
            if "old_facecolor" in v.flags:
                v.flags["facecolor"] = v.flags["old_facecolor"]
                del v.flags["old_facecolor"]
            else:
                del v.flags["facecolor"]

        ax.axis("equal")
        return fig

    def show(self, *args, **kwargs):
        """
        |==============================|
        | Affiche le graphe a l'ecran. |
        |==============================|

        :seealso: 'self.plot'.
        
        Parameters
        ----------
        :param args: Same as 'self.plot'.
        :param kwargs: Same as 'self.plot'.
        """
        import matplotlib.pyplot as plt
        self.plot(*args, **kwargs)
        plt.show()
