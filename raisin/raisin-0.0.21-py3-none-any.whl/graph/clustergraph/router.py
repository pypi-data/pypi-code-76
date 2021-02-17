#!/usr/bin/env python3

"""
|=======================================|
| Les noeuds d'interconnection routeur. |
|=======================================|

* Dans un graphe qui represente un reseau internet, les noeuds
modelises ici sont les noeuds qui n'effectuent pas de calcul mais
qui sont capable d'aiguiller des paquets.
"""

import time

from raisin.tools import identity
from raisin.application.settings import settings
from ..vertex import Vertex

class Internet(Vertex):
    """
    |=================|
    | Noeud internet. |
    |=================|

    * Les arcs qui partent de ce noeud pointent vers des
    noeuds de type 'InBoxing'.
    * Les arcs qui arrivent sur ce noeud provienent de
    noeuds de type 'OutBoxing'.
    """
    def __init__(self, n=None):
        super().__init__(name="Internet", n=n)
        self.flags["edgecolor"] = "black"
        self.flags["facecolor"] = "#aedbe7" # Bleu ciel.

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

class InBoxing(Vertex):
    """
    |============================|
    | La boxe d'un reseau local. |
    | WAN --> LAN                |
    |============================|

    * Tous les ordinateurs d'un reseau local sont
    connectes 'dans les 2 sens' a ce noeud.
    * Ce noeud a aussi un arc qui pointe vers 'Internet'.
    """
    def __init__(self, table, *, ipv6="", ipv4="", dns_ipv6="", dns_ipv4="", n=None):
        """
        |=========================================|
        | Initialisation du noeud de redirection. |
        |=========================================|

        Parameters
        ----------
        :param table: les couples de correspondance de redirections de ports.
            {(port_exterieur, mac_p), ...}
        :type table: set, frozenset, list, tuple
        :param ipv6: L'ipv6 publique si il y en a une.
        :type ipv6: str
        :param ipv4: L'ipv4 publique si il y en a une.
        :type ipv4: str
        :param dns_ipv6: Le nom de domaine associe a l'ipv6 publique.
        :type dns_ipv6: str
        :param dns_ipv4: Le nom de domaine associe a l'ipv4 publique.
        :type dns_ipv4: str
        """
        # Verications somaire, non approfondies.
        assert all(isinstance(t, (set, frozenset, list, tuple)) for t in table)
        assert all(isinstance(t[0], int) and t[0] > 0 for t in table), \
            "Les clefs doivent etre des ports entier."
        assert all(isinstance(t[1], str) for t in table), \
            "Les valeurs doivent etre des adresses mac en str."
        assert isinstance(ipv6, str), "Les ip doivent etre str, pas %s." \
            % type(ipv6).__name__
        assert isinstance(ipv4, str), "Les ip doivent etre str, pas %s." \
            % type(ipv4).__name__
        assert isinstance(dns_ipv6, str), "Les noms de domaines doivent etre str, pas %s." \
            % type(dns_ipv6).__name__
        assert isinstance(dns_ipv4, str), "Les noms de domaines doivent etre str, pas %s." \
            % type(dns_ipv4).__name__
        

        # Initialisation des attributs standards.
        self.table = set(table)
        self.ipv6 = ipv6
        self.ipv4 = ipv4
        self.dns_ipv6 = dns_ipv6
        self.dns_ipv4 = dns_ipv4

        # Heritage.
        if self.dns_ipv6:
            name = "Download Boxing\n%s" % self.dns_ipv6
        elif self.dns_ipv4:
            name = "Download Boxing\n%s" % self.dns_ipv4
        elif self.ipv6:
            name = "Download Boxing\n%s" % self.ipv6
        elif self.ipv4:
            name = "Download Boxing\n%s" % self.ipv4
        else:
            name = "Download Boxing"
        super().__init__(name=name, n=n)

        # Historique.
        self.history = {} # A chaque attribu, associ son etat et sa date de mise a jour.
        self.history["name"] = self.name
        if self.table:
            self.history["table"] = time.time()
        if self.ipv6:
            self.history["ipv6"] = time.time()
        if self.ipv4:
            self.history["ipv4"] = time.time()
        if self.dns_ipv6:
            self.history["dns_ipv6"] = time.time()
        if self.dns_ipv4:
            self.history["dns_ipv4"] = time.time()

        # Constantes.
        self.flags["edgecolor"] = "#960406" # Rouge sang.
        self.flags["facecolor"] = "#ffff66" # Jaune clair.

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
            "initializer": {
                "table": self.table,
                "ipv4": self.ipv4,
                "ipv6": self.ipv6,
                "dns_ipv4": self.dns_ipv4,
                "dns_ipv6": self.dns_ipv6,
                "n": self.n},
            "internal": {
                "history": self.history,
                }}

class OutBoxing(Vertex):
    """
    |============================|
    | La boxe d'un reseau local. |
    | LAN --> WAN                |
    |============================|
    """
    def __init__(self, *, name=None, n=None):
        """
        Parameters
        ----------
        :param name: Le nom du noeud, None si il faut le chercher.
        :type name: None, str
        """
        assert name is None or isinstance(name, str), \
            "'name' has to be str, not %s." % type(name).__name__
        
        # Heritage.
        if name is None:
            if settings["server"]["dns_ipv6"]:
                name = "Upload Boxing\n%s" % settings["server"]["dns_ipv6"]
            elif settings["server"]["dns_ipv4"]:
                name = "Upload Boxing\n%s" % settings["server"]["dns_ipv4"]
            elif identity["ipv6"]:
                name = "Upload Boxing\n%s" % identity["ipv6"]
            elif identity["ipv4"]:
                name = "Upload Boxing\n%s" % identity["ipv4"]
            else:
                name = "Upload Boxing"
        super().__init__(name=name, n=n)

        # Historique.
        self.history = {} # A chaque attribu, associ son etat et sa date de mise a jour.
        self.history["name"] = time.time()
        
        # Constantes.
        self.flags["edgecolor"] = "#01946d" # Vert / Bleu turquoise fonce.
        self.flags["facecolor"] = "#ffff55" # Jaune clair.

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
            "initializer": {
                "name": self.name,
                "n": self.n},
            "internal": {"history": self.history}}
