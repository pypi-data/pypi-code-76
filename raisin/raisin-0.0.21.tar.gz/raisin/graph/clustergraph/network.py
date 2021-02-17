#!/usr/bin/env python3

"""
|==============================================|
| Graphe qui represente un cluster de travail. |
|==============================================|

* C'est l'element de base qui permet pour un ordinateur
d'avoir une vision fine de ces voisins.

* Le graphe doit etre lance par le serveur local qui tourne sur ce PC.
"""

import os
import queue
import random
import re
import socket
import subprocess
import sys
import threading
import time

import raisin
from raisin.tools import Printer, identity
from raisin.application.settings import settings
import raisin.communication as communication
from .. import basegraph
from . import computer, router, connection
from raisin.communication.constants import RESERVED_PORTS


class Network(basegraph.BaseGraph):
    """
    |======================================|
    | Specialisation d'un graphe abstrait. |
    |======================================|

    * Ce graphe represente precisement l'etat actuel
    du cluster de travail.
    * Il doit etre initialisé
    """
    def __init__(self, network_data=None):
        """
        |================================================|
        | Initialise le graphe qui represente le reseau. |
        |================================================|

        * Tente d'abord de charger le graphe depuis le fichier
        de d'enregistrement si il existe.
        * S'assure que le graphe soit coherent par raport au parametres.
        Cette verification a pour but d'eviter les melanges entre reseaux.
        * Si le graphe n'est pas celui du bon reseau ou bien qu'il n'existe
        pas, il est cree de toutes pieces.

        Parameters
        ----------
        :param network_data: Le reseau serialize.
            * Si il est omis (None), recherche si il se trouve
            dans le fichier "~.raisin.network.rsn".
            * Si  ce fichier n'existe pas, un reseau tout neuf est genere.
            * Si cet argument est specifie, il doit sortir tout droit de
            la methode ``serialize`` de la classe ``Network``.
        :type network_data: generator.

        Returns
        -------
        :return: Le graphe instancie, verifie et initialise.
        :rtype: Network
        """
        network_file = os.path.join(os.path.expanduser("~"), ".raisin", "network.rsn")
        super().__init__(directed=True, comment="Cluster")
        self.network_name = None # Doit etre initialise.
        
        # Remplissage.
        if os.path.exists(network_file) or network_data is not None:
            nodes = {
                "Computer": computer.Computer,
                "MySelf": computer.MySelf,
                "Internet": router.Internet,
                "InBoxing": router.InBoxing,
                "OutBoxing": router.OutBoxing}
            if network_data is None:
                with open(network_file, "rb") as f:
                    network_data = list(raisin.load(f)) # Le 'list' c'est pour eviter ValueError: read of closed file.
            for kind, attr in network_data: # Generateur des noeuds puis des arcs.
                if kind in nodes:
                    node = nodes[kind](**attr["initializer"])
                    self.add_vertex(node)
                    for key, value in attr["internal"].items():
                        setattr(node, key, value)
                elif kind == "Connection":
                    self.add_arrow(connection.Connection(
                        self.__getitem__(attr["vs"], is_vertex=True),
                        self.__getitem__(attr["vd"], is_vertex=True),
                        **attr["attr"]))
                elif kind == "properties":
                    for key, value in attr.items():
                        setattr(self, key, value)
                else:
                    raise TypeError("Le reseau ne possede pas de %s." % repr(kind))
        else:
            self.network_name = settings["server"]["network_name"]

        # Verifictation, construction.
        if not self or not self.verification():
            self.build()

    def verification(self):
        """
        |==================================================|
        | S'assure que le graphe est celui du bon cluster. |
        |==================================================|

        Returns
        ------
        :return: True si le graphe est OK, False sinon.
        :rype: boolean
        """
        return settings["server"]["network_name"] == self.network_name

    def build(self):
        """
        |=================================|
        | Etablie le tout premier graphe. |
        |=================================|

        * Supprime d'abord tous les elements du graphe existant
        avant d'en recreer un tout neuf.

        Il y a 4 possibilitees:
        1) Reseau mondial.
            -> Se connecte a un serveur pour recuperer les informations.
        2) Rejoindre un cluster specifique.
            -> Demande les informations a ce serveur.
        3) Administrer son propre reseau.
            -> Initialise les reseau minimal ou on est le seul.
        4) Scanner le reseau local.
            -> Scane le reseau local sur les ports 20001-20009
        """
        def scan(ip, client_queue, p):
            """
            Recherche si l'adresse ip existe.
            Si c'est le cas, recherche les ports ouverts.
            Si il y en a, et que c'est un port de serveur raisin,
            une connection est etablie, le client est pousse dans la file.
            """
            def scan_port(ip, port, client_queue, p):
                """
                Recherche si le port 'port' est ouvert
                pour l'ip 'ip'. Si c'est le cas, instancie un client
                et pousse le client dans la file.
                """
                if not client_queue.empty():
                    return
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if 0 == sock.connect_ex((ip, port)):
                    sock.close()
                    p.show("port %d for %s is open." % (port, repr(hostname)))
                    try:
                        client = communication.Client(ip, port)
                    except Exception:
                        return
                    else:
                        client_queue.put(client)
                        return
                sock.close()

            try:
                hostname, alias, addresslist = socket.gethostbyaddr(ip)
            except socket.herror: # Si ca echoue ca veut pas forcement dire qu'il n'y a pas un serveur.
                if subprocess.run("ping -c 1 %s" % ip,
                        shell=True, capture_output=True).returncode:
                    return
                hostname, addresslist = ip, [ip]

            p.show("%s found at the ip '%s'." % (repr(hostname), ", ".join(addresslist)))
            # linux: [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
            # windows: [135, 137, 138, 139, 445]
            # mac: [22, 445, 548, 631]
            # Registered Ports: 1024 through 49151.
            ports = set(range(20000, 20011, 1)) - RESERVED_PORTS
            
            threads_port = []
            for port in ports:
                if not client_queue.empty():
                    break
                while True:
                    if threading.active_count() < 256:
                        threads_port.append(threading.Thread(target=scan_port,
                            args=(ip, port, client_queue, p)))
                        threads_port[-1].start()
                        break
                    else:
                        time.sleep(0.1)
                        threads_port = [th for th in threads_port if th.is_alive()]
            for th in threads_port:
                th.join()
        
        def complete(client):
            """
            Recupere via le client, les informations du cluster.
            Ajoute a self, les noeuds et les arcs de ce cluster.
            """
            raise NotImplementedError

        with Printer("Initialization of the cluster graph...") as p:
            from raisin.application.hmi.checks import network_name_verification
            assert network_name_verification(network_name_verification), \
                "Le nom du reseau n'est pas conforme."
            del network_name_verification

            # Suppression des elements existants.
            for node in self.get_vertices():
                del self[node]

            # Creation du reseau minimaliste.
            internet = router.Internet()
            outboxing = router.OutBoxing()
            myself = computer.MySelf()
            self.add_vertex(internet) # Le noeud internet global.
            self.add_vertex(outboxing) # La boxe pour les requettes sortantes.
            self.add_vertex(myself) # Soit meme.
            self.add_arrow(connection.Connection(myself, outboxing))
            self.add_arrow(connection.Connection(outboxing, internet))

            self.add_arrow(connection.Connection(outboxing, myself))
            if settings["server"]["port_forwarding"]:
                inboxing = router.InBoxing(
                    table={(settings["server"]["port_forwarding"], identity["mac"]),},
                    ipv4=str(identity["ipv4_wan"]) if identity["ipv4_wan"] else "",
                    ipv6=str(identity["ipv6"]) if identity["ipv6"] else "",
                    dns_ipv4=settings["server"]["dns_ipv4"] if settings["server"]["dns_ipv4"] else "",
                    dns_ipv6=settings["server"]["dns_ipv6"] if settings["server"]["dns_ipv6"] else "")
                self.add_vertex(inboxing)
                self.add_arrow(connection.Connection(inboxing, myself))
                self.add_arrow(connection.Connection(internet, inboxing))

            # if network_name == "main":
            #     p.show("Connection to the mondial network.")
            #     with open(os.path.join(os.path.dirname(__file__), "servers.py"),
            #             "r", encoding="utf-8") as f:
            #         servers = [l.rstrip() for l in f.readlines() if "@" in l]
            #     random.shuffle(servers)
            #     for s in servers:
            #         try:
            #             self.initialization(s)
            #         except ConnectionError:
            #             continue
            #         else:
            #             return
            #     raise ConnectionError("Aucun serveur n'est accessible.")

            if re.search(r"^\d+@[a-zA-Z0-9_\.:]{5,}$", self.network_name):
                p.show("Connection to %s." % repr(self.network_name))
                port, ip = network_name.split("@")
                client = communication.Client(ip, int(port))
                complete(client)

            elif self.network_name == "":
                p.show("Local network scan.")
                client_queue = queue.Queue()
                ip_base = ".".join(str(identity["ipv4_lan"]).split(".")[:-1]) + ".%d"
                threads = []
                for addr in (ip_base % i for i in range(256)):
                    if not client_queue.empty():
                        break
                    while True:
                        if threading.active_count() < 128: # Nombre de thread simultane
                            threads.append(threading.Thread(target=scan, args=(addr, client_queue, p)))
                            threads[-1].start()
                            break
                        else:
                            time.sleep(1)
                            threads = [th for th in threads if th.is_alive()]
                for th in threads:
                    th.join()

                if not client_queue.empty():
                    complete(client_queue.get())

            else:
                ValueError("'%s' n'est pas reconnaissable pour initialiser le reseau."
                    % repr(self.network_name))

    def record(self):
        """
        |=========================================|
        | Met a jour le fichier d'etat du graphe. |
        |=========================================|

        * Le fichier mis a jour c'est '~/.raisin/network.rsn'.
        """
        import raisin

        root = os.path.join(os.path.expanduser("~"), ".raisin")
        if not os.path.exists(root):
            raise FileNotFoundError("'raisin' n'est pas installe. "
                "veuillez executer: '%s -m raisin install'" % sys.executable)
        
        with open(os.path.join(root, "network.rsn"), "wb") as f:
            raisin.dump(self.serialize(), f)

    def serialize(self):
        """
        |======================|
        | Serialize ce graphe. |
        |======================|

        * Fait pour etre utilise avec ``raisin.serialize(self.serialize())``.

        Returns
        -------
        :return: Un generateur de noeud puis d'arc.
        :rtype: generator
        """
        yield "properties", {
            "network_name": self.network_name}
        for node in self.get_vertices():
            yield type(node).__name__, node.get_attr()
        for conn in self.get_segments():
            yield type(conn).__name__, conn.get_attr()

    def merge(self, other):
        """
        |==================================|
        | Met a jour les valeurs du graphe |
        | a partir du graphe 'other'.      |
        |==================================|

        * Ne retourne rien, met juste le graphe a jour.

        Parameters
        ----------
        :param other: L'autre graphe dont on tire les informations.
        :type other: Network
        """
        def merge(obj1, obj2):
            """
            |=============================================|
            | Injecte les informations de obj2 dans obj1. |
            |=============================================|

            * Permet de recuperer et de combiner les informations
            les plus recentes de 2 objets.

            Parameters
            ----------
            :param obj1: Le routeur, l'ordinateur ou la connection a metre a jour.
            :param obj2: L'autre element du meme type dont on recupere les infos.
            """
            ok_class == {router.Internet, router.InBoxing, router.OutBoxing,
                computer.Computer, connection.Connection}
            assert type(obj1) in ok_class and type(obj2) in ok_class, \
                "Les classes d'entree possible sont seulement %s." \
                % ", ".join(c.__name__ for c in ok_class)
            assert type(obj1) == type(obj2), "Les 2 objets doivent etre de meme type."

            if type(obj1) == type(obj2) == router.Internet:
                return

            for attr, value in {**obj1.__dict__, **obj2.__dict__}.items(): # On parcous tous les parametres.
                if attr in obj1.history and attr in obj2.history: # Si ce parametre est present dans les 2 objets.
                    if obj1.history[attr] < obj2.history[attr]: # Et qu'il faut le metre a jour.
                        obj1.history[attr] = obj2.history[attr] # On met deja a jour l'historique,
                        setattr(obj1, attr, getattr(obj2, attr)) # Et la valeur de l'attribut.
                elif attr not in obj1.history and attr in obj2.history: # Si la variable est presente que chez l'autre objet.
                    obj1.history[attr] = obj2.history[attr] # On ajoute alors se parametre a l'historique.
                    setattr(obj1, attr, getattr(obj2, attr)) # Puis on met la bonne valeur du parametre.

        raise NotImplementedError
