#!/usr/bin/env python3

import copy
import glob
import io
import ipaddress
import json
import os
import platform
import pickle
import re
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.request
import uuid

class MergeGenerators:
    """
    permet d'iterer sur plusieur generateurs a la fois.
    Chaque generateur est independament excecuter sur un
    faux thread separe
    """
    class _AssyncGen(threading.Thread):
        def __init__(self, papa, gen):
            threading.Thread.__init__(self)
            self.papa = papa
            self.gen = gen
            self.queue = []
            self.lock = threading.Lock()
            self.start()

        def run(self):
            for element in self.gen:
                with self.lock:
                    self.queue.append(element)
                    try:
                        self.papa.lock.release()
                    except RuntimeError:
                        continue

    def __init__(self, *generators):
        """
        'generators' est un tuple contenant des iterables
        """
        self.lock = threading.Lock()
        self.generators = [MergeGenerators._AssyncGen(self, iter(g)) for g in generators]

    def __iter__(self):
        """
        cede jusqu'au bout le contenu desordonne
        de chaque sous generateur
        """
        while self.generators:  # tant que tout n'est pas termine
            self.lock.acquire() # on attend qu'il se passe quelque-chose
            for i, gen in enumerate(self.generators):
                if gen.queue:
                    with gen.lock:
                        yield from gen.queue
                        gen.queue = []
                if not gen.is_alive():
                    del self.generators[i]

class Id:
    """
    Recupere l'identifiant de cet ordinateur.
    """
    class _Version:
        """
        Represente une version et permet des
        comparaisons entre les versions.
        """
        def __init__(self, version_str):
            self.version_str = version_str
            self.moi_list = self._simplify(list(map(int, self.version_str.split("."))))

        def _simplify(self, version_list):
            """
            Retourne une liste simplifiee (sans les 0 a la fin).
            """
            assert isinstance(version_list, list), \
                "'version_list' doit etre de type list, pas %s." \
                % type(version_list).__name__
            
            while True:
                if len(version_list):
                    if version_list[-1]:
                        break
                    else:
                        del version_list[-1]
                else:
                    break
            return version_list

        def __repr__(self):
            return self.version_str

        def __eq__(self, other_str):
            """
            Renvoi True si 'other_str' correspond a la meme version que self.
            """
            assert type(other_str) is str, "La variable 'other' doit etre de type str, non pas %s." % type(other_str)
            other_list = self._simplify(list(map(int, other_str.split("."))))
            return self.moi_list == other_list

        def __gt__(self, other_str):
            """
            Retourne True si 'other_str' est plus petit stricetement que self.
            """
            assert type(other_str) is str, "La variable 'other' doit etre de type str, non pas %s." % type(other_str)
            other_list = self._simplify(list(map(int, other_str.split("."))))
            for lui, moi in zip(other_list, self.moi_list):
                if lui < moi:
                    return True
                if lui > moi:
                    return False
            return len(other_list) < len(self.moi_list)

        def __lt__(self, other_str):
            return not self > other_str and not self == other_str

        def __ge__(self, other_str):
            return self > other_str or self == other_str

        def __le__(self, other_str):
            return self < other_str or self == other_str

    def __init__(self):
        self.hostname = None    # nom de l'ordinateur
        self.username = None    # nom de l'utilisateur
        self.mac = None         # adresse mac
        self.ipv4_lan = None    # adresse ipv4 du reseau local
        self.ipv4_wan = None    # adresse ipv4 du reseau exterieur
        self.ipv6 = None        # adresses ipv6 publique
        self.country = None     # initiale en minuscule du pays ex: "fr", "en"
        self.city = None        # c'est la ville ex: "grenoble"
        self.bus = None         # 64 ou 32 bits
        self.python_version = None # version de python
        self.os_version = None  # version de l'os qui interprete ce python
        self.system = None      # nom generique du system d'exploitation
        self.has_admin = None   # dit si l'utilisateur a les droits admin
        self._last_connection = {} # derniers acces

    def __getitem__(self, key):
        """
        Permet de recuperer les elements en y accedant comme pour un dictionaire.

        entree
        ------
        :param key: Nom du champ que l'on shouaite optenir.
        :type key: str

        sortie
        ------
        :return: L'element associe a la bonne clef.
        :raises KeyError: Si l'element n'existe pas
        """
        self.update(key)
        return getattr(self, key)

    def __iter__(self):
        """
        Iter sur les couples klef/valeur
        de sorte que l'on puisse faire dict(self).

        Les valeurs sont toutes converties en str.
        """
        for key in ["username", "hostname", "city", "country",
                "system", "python_version", "bus", "os_version",
                "mac", "ipv4_lan", "ipv4_wan", "ipv6"]:
            yield key, str(self[key])
        yield "has_admin", ("yes" if self["has_admin"] else "no")

    def __repr__(self):
        chaine = "{:<14s}".format("username") + ": " + self["username"] + "\n"    \
                 + "{:<14s}".format("hostname") + ": " + self["hostname"] + "\n"  \
                 + "{:<14s}".format("has admin") + ": " + ("yes" if self["has_admin"] else "no") + "\n" \
                 + "{:<14s}".format("city") + ": " + self["city"] + "\n"          \
                 + "{:<14s}".format("country") + ": " + self["country"] + "\n"    \
                 + "{:<14s}".format("system") + ": " + self["system"] + "\n"      \
                 + "{:<14s}".format("python version") + ": " + str(self["python_version"]) + "\n" \
                 + "{:<14s}".format("bus") + ": " + str(self["bus"]) + " bits\n"  \
                 + "{:<14s}".format("os") + ": " + self["os_version"]  + "\n"     \
                 + "{:<14s}".format("mac") + ": " + self["mac"] + "\n"            \
                 + "{:<14s}".format("ipv4 lan") + ": " + str(self["ipv4_lan"]) + "\n" \
                 + "{:<14s}".format("ipv4 wan") + ": " + str(self["ipv4_wan"]) + "\n" \
                 + "{:<14s}".format("ipv6") + ": " + str(self["ipv6"])
        return chaine

    def __str__(self):
        return repr(self)

    def update(self, key):
        """
        Met a jour la valeur associee a la clef demandee.

        entree
        ------
        :param key: Nom du champ que l'on shouaite optenir.
        :type key: str

        sortie
        ------
        :raises KeyError: Si l'element n'existe pas
        """
        assert isinstance(key, str), \
            "La clef doit etre en str, pas en %s." % type(key).__name__

        last_connection = self._last_connection.get(key, 0) # Date de la derniere connection.
        deltat_t = time.time() - last_connection
        if key == "hostname":
            if deltat_t > 3600: # Le hostname ne change pas souvent.
                nouv_hostname = self.get_hostname()
                self.hostname = nouv_hostname if nouv_hostname is not None else self.hostname
                self._last_connection[key] = time.time() if nouv_hostname is not None else last_connection
        elif key == "username":
            if deltat_t > 3600: # Le username ne change pas souvent non plus.
                nouv_username = self.get_username()
                self.username = nouv_username if nouv_username is not None else self.username
                self._last_connection[key] = time.time() if nouv_username is not None else last_connection
        elif key == "mac":
            if last_connection == 0: # Pour le coup, elle est pas cencee changer!
                self.mac = self.get_mac()
                self._last_connection[key] = time.time()
        elif key == "ipv4_lan":
            if deltat_t > 60: # Les adresses ip ca peu vite changer.
                nouv_ipv4_lan = self.get_ipv4_lan()
                self.ipv4_lan = nouv_ipv4_lan if nouv_ipv4_lan is not None else self.ipv4_lan
                self._last_connection[key] = time.time() if nouv_ipv4_lan is not None else last_connection
        elif key == "ipv4_wan":
            if deltat_t > 60: # Les adresses ip ca peu vite changer.
                nouv_ipv4_wan = self.get_ipv4_wan()
                self.ipv4_wan = nouv_ipv4_wan if nouv_ipv4_wan is not None else self.ipv4_wan
                self._last_connection[key] = time.time() if nouv_ipv4_wan is not None else last_connection
        elif key == "ipv6":
            if deltat_t > 60: # Les adresses ip ca peu vite changer.
                nouv_ipv6 = self.get_ipv6()
                self.ipv6 = nouv_ipv6 if nouv_ipv6 is not None else self.ipv6
                self._last_connection[key] = time.time() if nouv_ipv6 is not None else last_connection
        elif key == "country":
            if deltat_t > 3600: # On change pas de pays tous les 4 matins.
                nouv_country = self.get_country()
                self.country = nouv_country if nouv_country is not None else self.country
                self._last_connection[key] = time.time() if nouv_country is not None else last_connection
        elif key == "city":
            if deltat_t > 600: # Par contre en voyage on peu facilement changer de ville.
                nouv_city = self.get_city()
                self.city = nouv_city if nouv_city is not None else self.city
                self._last_connection[key] = time.time() if nouv_city is not None else last_connection
        elif key == "bus":
            if last_connection == 0: # Il doit etre difficile de changer de carte mere sans arreter le programe.
                self.bus = 64 if "64" in platform.machine() \
                    else 32 if "32" in platform.machine() or "86" in platform.machine() else None
                self._last_connection[key] = time.time()
        elif key == "python_version":
            if last_connection == 0: # On ne peut pas changer la version du python en cours d'execution.
                self.python_version = self.get_python_version()
                self._last_connection[key] = time.time()
        elif key == "os_version":
            if deltat_t > 600: # Il est possible de faire une mise a jour en arriere plan.
                nouv_os_version = platform.version()
                self.os_version = nouv_os_version if nouv_os_version is not None else self.os_version
                self._last_connection[key] = time.time() if nouv_os_version is not None else last_connection
        elif key == "system":
            if last_connection == 0: # L'OS ne change pas toute seule.
                self.system = platform.system().lower()
                self._last_connection[key] = time.time()
        elif key == "has_admin": # Dans le cas ou le programme change ces droits.
            self.has_admin = self.get_has_admin() # Il doit pourvoir le verifier sans latence.
        else:
            raise KeyError("%s n'esxiste pas." % repr(key))
        
    def get_hostname(self):
        """
        retourne l'identifiant de l'ordinateur
        """
        try:
            return socket.gethostname()
        except socket.error:
            return None

    def get_username(self):
        """
        retourne le nom d'utilisateur
        """
        try:
            return os.environ["USERNAME"]
        except:
            return os.path.basename(os.path.expanduser("~"))

    def get_mac(self):
        """
        retourne l'adress mac du pc
        """
        try:
            return ":".join(["{:02x}".format((uuid.getnode() >> i) & 0xff) for i in range(0, 8*6, 8)][::-1])
        except KeyboardInterrupt as e:
            raise e from e
        except:
            return None

    def get_ipv4_lan(self):
        """
        retourne l'ip sur le reseau local
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # un socket en mode UDP (DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # broadcast
            s.connect(("<broadcast>", 0))                               # le mot-cle python pour INADDR_BROADCAST
            ip_local, port = s.getsockname()                            # renvoi de l'adresse source
            return ipaddress.IPv4Address(ip_local)                      # on retourne donc la vrai adresse
        except socket.error:                                            # mais l'on est pas certain que cette methode fonctionne a tous les coups
            return None                                                 # c'est pour cela que l'on prend des precautions
    
    def get_ipv4_wan(self):
        """
        tente de retourner l'ip d'internet
        """
        @timeout_decorator(30)
        def get_ipify():
            dic = eval(urllib.request.urlopen("https://api.ipify.org/?format=json").read().decode())
            return ipaddress.IPv4Address(dic["ip"])

        @timeout_decorator(30)
        def get_ipinfo():
            dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
            return ipaddress.IPv4Address(dic["ip"])

        @timeout_decorator(30)
        def get_icanhazip():
            ip = eval(urllib.request.urlopen("http://icanhazip.com/").read().decode())
            return ipaddress.IPv4Address(ip)

        try:
            return get_ipify()
        except KeyboardInterrupt as e:
            raise e from e
        except:
            try:
                return get_ipinfo()
            except KeyboardInterrupt as e:
                raise e from e
            except:
                try:
                    return get_icanhazip()
                except KeyboardInterrupt as e:
                    raise e from e
                except:
                    return None
    
    def get_country(self):
        """
        retourne les initiales du pays dans lequel on est
        retourne None en cas d'echec de connection a internet
        """
        @timeout_decorator(30)
        def get_ipinfo():
            dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
            return dic["country"].lower()

        try:
            return get_ipinfo()
        except KeyboardInterrupt as e:
            raise e from e
        except:
            return None

    def get_city(self):
        """
        retourne les initiales du pays dans lequel on est
        retourne None en cas d'echec de connection a internet
        """
        @timeout_decorator(30)
        def get_ipinfo():
            dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
            return dic["city"].lower()

        try:
            return get_ipinfo()
        except KeyboardInterrupt as e:
            raise e from e
        except:
            return None

    def get_ipv6(self):
        """
        Tente de retourner l'ipv6 publique.
        """
        def get_local():
            result = socket.getaddrinfo(self.hostname, 0, socket.AF_INET6)
            return [ipaddress.IPv6Address(a[4][0]) for a in result]

        @timeout_decorator(30)
        def get_ipify():
            dic = eval(urllib.request.urlopen("https://api6.ipify.org?format=json").read().decode())
            return ipaddress.IPv6Address(dic["ip"])

        @timeout_decorator(30)
        def get_myip():
            ip = urllib.request.urlopen("http://v6.ipv6-test.com/api/myip.php").read().decode()
            return ipaddress.IPv6Address(ip)

        @timeout_decorator(30)
        def get_seeip():
            dic = eval(urllib.request.urlopen("https://ip6.seeip.org/json").read().decode())
            return ipaddress.IPv6Address(dic["ip"])

        try:
            return get_ipify()
        except KeyboardInterrupt as e:
            raise e from e
        except:
            try:
                return get_myip()
            except KeyboardInterrupt as e:
                raise e from e
            except:
                try:
                    return get_seeip()
                except KeyboardInterrupt as e:
                    raise e from e
                except:
                    return None
    
    def get_python_version(self):
        """
        Retourne la version de python sur laquelle on est entrain de travailler.
        """
        return Id._Version("%d.%d.%d" % (sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

    def get_has_admin(self):
        """
        Retourne True si l'utilisateur a les droits administrateur.
        """
        if os.name == "nt":
            try:
                # only windows users with admin privileges can read the C:\windows\temp
                temp = os.listdir(os.sep.join(
                    [os.environ.get("SystemRoot", "C:\\windows"),
                    "temp"]))
            except:
                return False
            else:
                return True
        else:
            if "SUDO_USER" in os.environ and os.geteuid() == 0:
                return True
            return False

class Lock:
    """
    permet de verouiller bloquer le reste du programe, ou a un autre processus
    """
    def __init__(self, id="default", timeout=60, priority=0, signature=None, display=True, locality_degrees=1):
        """
        'id' (STR) => est l'identifiant de ce verrou, c'est ce qui permet de le rendre independant des autres
        'timeout' (INT, FLOAT) => temps de validite du verrou en s
        'priority' (INT) => l'utilisateur 'n' est prioritaire devant [n-1, n-2, ..., 2, 1, 0] avec n < 1000
        'signature' (obj) => permet si voulu, d'informer l'utilisateur du processus appelant
        'display' (BOOL) => True pour afficher et False pour ne pas appeller afficher
        'locality_degrees (BOLL) => gere la portee de ce verrou:
            -0 => ultra local, visible seulement depuis cette instance du verrou
            -1 => local a ce processus, thread de threading, visible tout de meme depuis differentes instances
            -2 => local a la machine, multiprocessing et plusieur instance du programe
            -3 => visible par tout le LAN, global a tous les ordi present deriere ce meme routeur
            -4 => visible par tous ceux qui appartiennent au reseau de raisin WAN
        """
        self.id = id                                                                        # identifiant de ce verrou
        self.timeout = timeout                                                              # temps de validitee du verrou pose
        self.priority = priority                                                            # est un entier, plus il est elever, plus la prioritee est haute
        self.signature = signature                                                          # permet d'afficher le message au bon endroit
        self.display = display                                                              # True si il faut afficher le message
        self.local = True                                                                   # est True si ce verrou est seulement actif sur ce programe
        self.code = uuid.uuid4().hex                                                        # identifiant unique propre a ce verrou
        if self.local:                                                                      # si le verrou est local, propre a ce processus
            self.path_file = os.path.join(temprep, "lock_%s.txt" % self.id)                 # le chemin qui mene jusqu'au verrou
        else:                                                                               # si seul tout le monde doit pouvoir y avoir acces
            self.path_file = os.path.join(temprep, "lock_%s.txt" % self.id)                 # chemin bien visible par tous

    def acquire(self):
        """
        depose le verrou et retourne une fois qu'il est depose
        """
        while os.path.exists(self.path_file):                                               # tant que le fichier existe
            try:                                                                            # on va essayer de lire ce qu'il y a dedand
                with open(self.path_file, "r") as f:                                        # tentative d'ouverture
                    lock_priority, lock_code, lock_timeout = f.read().split(";")            # et de lecture du fichier
                    lock_priority, lock_code, lock_timeout = int(lock_priority), lock_code, float(lock_timeout) # convertion dans les bon types
                if (lock_code == self.code) and (lock_priority == 999):                     # si on en est plainement maitre
                    return None                                                             # on se sauve vite de la
                elif (lock_code == self.code) and (lock_priority != 999):                   # si personne ne semble se manifester
                    with open(self.path_file, "w") as f:                                    # on va tenter de s'en emparer vraiment
                        f.write("999;"+self.code+";"+str(time.time()+self.timeout))         # en y metant nos empreintes
                elif (lock_code != self.code) and (self.priority > lock_priority):          # si un autre processus depose timidement son verrou mais que l'on est plus fort que lui
                    with open(self.path_file, "w") as f:                                    # on va alors a notre tour tenter de le prendre timidement
                        f.write(str(self.priority)+";"+self.code+";"+str(time.time()+self.timeout)) # en y inscrivant notre volontee
                    if self.priority != 999:
                        time.sleep(0.02)                                                    # on est poli, on laisse la priorite au plus fort
                elif time.time() > lock_timeout:                                            # si le verrou est trop vieu pour avoir encore de la valeur
                    os.remove(self.path_file)                                               # on tente alors de le degomer
                else:                                                                       # dans le cas ou l'on est dans aucune des ces situation, c'est qu'il faut attendre
                    time.sleep(0.01)                                                        # on fait alors une petite pause qui soulage le resources
            except:
                time.sleep(0.3)

        try:                                                                                # si il n'y a pas de fichiers
            with open(self.path_file, "w") as f:                                            # c'est alors possible de prendre la main
                f.write(str(self.priority)+";"+self.code+";"+str(time.time()+self.timeout)) # on essai donc de le faire
            if self.priority != 999:
                pass # pff sinon ca lague trop!
                # time.sleep(0.02)                                                          # on laisse le temps au processus plus fort de se retourner
            return self.acquire()                                                           # on repart donc en haut
        except:                                                                             # si il y a eu une erreur quelqonque
            return self.acquire()                                                           # on retent notre chance une deuxieme fois

    def release(self):
        """
        tente de liberer l'acces
        """
        try:                                                                                #on essai de supprimer le fichier
            os.remove(self.path_file)
        except:
            pass
        return None

    def is_lock(self):
        """
        retourne False si l'acces est libre
        """
        if not os.path.exists(self.path_file):                                              #dans le cas ou il n'y a pas de fichier
            return False                                                                    #c'est que l'acces est libre
        try:                                                                                #dans le cas ou il y a un fichier
            with open(self.path_file, "r") as f:                                            #on va tenter de le lire
                lock_priority, lock_code, lock_timeout = f.read().split(";")                #et de lecture du fichier
                lock_priority, lock_code, lock_timeout = int(lock_priority), lock_code, float(lock_timeout)#convertion dans les bon types
            if time.time() > lock_timeout:                                                  #si le verrou date de gerusalem
                return False                                                                #alor on considere que l'acces est libre
            return True                                                                     #dans le cas contraire, la voix n'est pas libre
        except:                                                                             #si ca capote
            return True                                                                     #en cas d'erreur aussi, la voix n'est pas disponible

    def is_free(self):
        """
        reourne True si l'acces est libre
        """
        return not(self.is_lock())

    def __enter__(self):
        if self.display:
            with Printer("wait "+str(self.id)+" freedom...", signature=self.signature):     #attente de la cess libre
                self.acquire()
        else:
            self.acquire()
        return self

    def __exit__(self, *args):
        if self.display:
            with Printer("release %s..." % self.id, signature=self.signature):               #rendre a nouveau l'acces libre
                self.release()
        else:
            self.release()

class LockDecorator:
    """
    permet de gerer automatiquement un verou l'ors de l'appelle du fonction
    permet aussi de s'assurer que la fonction n'est excecutee qu'une seule fois
    """
    def __init__(self, id, *, timeout=60, priority=0, signature=None, locality_degrees=0, jump=False):
        """
        'jump' (BOOL) => est un boolen qui quand il est a True, fait squiser l'execution de la fonction si elle est verouillee
        """
        self.id = id                                # identifiant du verrou
        self.timeout = timeout                      # temps de validite du verrou en s
        self.priority = priority
        self.signature = signature
        self.locality_degrees = locality_degrees
        assert type(jump) is bool, "'jump' doit etre un booleen, pas un %s." % type(jump)
        self.jump = jump
        
    def __call__(self, func):
        """
        cette methode n'est appelle qu'une seul fois au moment de l'import du programe qui contient
        la fonction decoree
        retourne la fonction decoree
        """
        verrou = Lock(self.id, timeout=self.timeout, priority=self.priority, signature=self.signature, locality_degrees=self.locality_degrees)
        def change_func(*args, **kwargs):
            if self.jump:
                if verrou.is_lock():
                    raise ValueError("Le verrou est deja pris.")
            with verrou:
                return func(*args, **kwargs)

        return change_func

class Printer:
    """
    permet d'afficher joliment les choses dans le terminal
    """
    def __init__(self, text="", *, display=None, signature=None):
        """
        'display' est un entier:
            cet entier correspond au nombre d'indentation maximum
            si il vaut None, la derniere valeur donnee est prise
        'signature' est n'importe quel objet python hashable, il permet de differencier les diferents processus
        pour qu'il n'y ai pas de conflit avec les threads
        """
        assert display is None or type(display) is int, "'display' doit etre un entier ou None, pas %s." % display
        assert type(text) is str, "'text' doit etre une chaine de caractere, pas un %s." % type(text)
        self.text = text
        self.display = display                                                  # s'actualise a l'appel de self.get_indentation
        self.signature = signature if signature != None else os.getpid()

        self.path = os.path.join(temprep, "printer_infos.pk")
        self.nbr_colones = 1                                                    # s'actualise quand self.get_indentation est appelee, nbr de colone d'affichage dans le terminal
        self.ma_colone = None                                                   # s'actualise au meme moment que 'nbr_colones', rang de la colone en cours

    def get_indentation(self, ecart=0):
        """
        renvoi le nombre d'indentations actuel (sans 'ecart')
        en profite pour enregistrer la nouvelle indentation a venir (avec ecart)
        'ecart' est le nombre d'indentation a ajouter algebriquement dans le fichier,
        0 ne change donc rien
        met aussi en arriere plan, a jour le nbr de colones a venir
        """
        exists = os.path.exists(self.path)                                      # on stocke ce resultat dans une variable afin de gagner du temps
        if ecart == 0 and exists and self.ma_colone:                            # si l'on doit faire de la lecture seule du fichier
            with Lock(id="printer", timeout=5, display=False, locality_degrees=1): # on pose un verrou a part afin de minimiser le temps d'acces au verrou
                with open(self.path, "rb") as f:                                # une fois qu'on a acces au fichier
                    content = pickle.load(f)                                    # on se contente de lire son contenu
            self.display = content[self.signature]["display"]                   # puis on liber tout de suite le verrou
            self.nbr_colones = len(content)
            self.ma_colone = content[self.signature]["colone"]
            return content[self.signature]["indentation"]                       # en faisant la deserialisation et l'analyse hors du verrou
        
        else:                                                                   # si on ne doit pas seulment lire mais qu'on doit aussi mettre a jour l'indentation
            with Lock(id="printer", timeout=10, display=False, locality_degrees=1): # on pose un autre verrou
                if os.path.exists(self.path):                                   # si il y a deja un fichier
                    with open(self.path, "rb") as f:                            # alors on commence par extraire les informations qui s'y trouve
                        content = pickle.load(f)                                # la on fait tout dans le verrou car de toute facon il va faloir reecrir
                else:                                                           # si par contre il n'y a pas deja une configuration
                    content = {}                                                # on edite une dictionaire tout vide
                
                content[self.signature] = content.get(self.signature, {})       # bref, comme on sait pas ce qui y a dans le dico
                content[self.signature]["indentation"] = content[self.signature].get("indentation", 0) + ecart # on prend toutes les precautions qu'on puisse prendre
                self.ma_colone = content[self.signature].get("colone", self.nbr_colones - 1)
                content[self.signature]["colone"] = self.ma_colone
                self.display = content.get(self.signature, {}).get("display", self.display if self.display is not None else 5)
                content[self.signature]["display"] = self.display
                
                indentation = content[self.signature]["indentation"] - ecart
                self.nbr_colones = len(content)
                if not indentation + ecart:                                     # si on l'afficage suivant se fera a ras
                    del content[self.signature]                                 # alors on se supprime afin de laisser de la place aux nouveaux
                    content = {
                        sign:{
                            inf:(val - 1 if inf == "colone" and val > self.ma_colone else val) \
                            for inf,val in infs.items()}
                        for sign, infs in content.items()}                      # puis on met aussi a jour les colones des autres
                with open(self.path, "wb") as f:                                # bref, les donnees sont bien a jour dans la RAM
                    pickle.dump(content, f)                                     # mais il faut encore les ecrire dans le fichier
            return indentation

    def indent(self, text):
        """
        retourne le texte bien indente avec le minimum entre l'indentation courante
        et la valeur maximum d'intentation admissible
        """
        indentation = min(self.get_indentation(), self.display if self.display is not None else 5) # nbr d'indentation a ajouter au texte
        return "\n".join(("\t"*indentation + l for l in text.split("\n")))      # on indentate alors chaque ligne, en prenant en compte les retours a la ligne

    def pprint(self, expression):
        """
        retourne la representation de l'expression avec de beau caractere utf-8
        sur une seule ligne dans la meusure du possible
        en cas d'echec, retourne str(expression)
        """
        if type(expression) is not str and raisin.sympy is not None:
            s = sys.stdout
            with io.StringIO() as f:
                sys.stdout = f
                try:
                    raisin.sympy.pprint(expression)         # on utilise sympy pour ecrire joliment
                    message = f.getvalue()[:-1].split("\n") # ainsi on recupere se qui est ecrit (\n exclu)
                    sys.stdout = s                          # puis  avant qu'il ne se passe trop de chose, on remet tout comme avant
                    if len(message) == 1:                   # si le tout tient sur une ligne
                        return message[0]                   # c'est gagne
                    elif len(message) == 0:                 # si il c'est passe des trucs bresson
                        return str(expression)              # pas de panique, on ignore les magouilles de sympy
                    else:                                   # si le tout ne tien pas sur une seule ligne
                        if type(expression) is dict:        # on essai de moin bourriner
                            return str({self.pprint(c): self.pprint(v) for c, v in expression.items()})# on decompose allors les operations en operation plus simples
                        elif type(expression) is list:
                            return str([self.pprint(v) for v in expression])
                        elif type(expression) is tuple:
                            return str(tuple([self.pprint(v) for v in expression]))
                except KeyboardInterrupt as e:
                    raise e from e
                finally:
                    sys.stdout = s
        return str(expression)     
    
    def get_size(self):
        """
        retourne la largeur du terminal en nbr de caractere
        """
        return shutil.get_terminal_size((80, 20)).columns                       # avec un module python cette fois ci, pas besoin de protection car en cas d'echec, cette fonction renvoi 80

    def show(self, text, *, ecart=0, force=False):
        """
        affiche a l'ecran le message
        'ecart' est le nombre d'indentation a ajouter pour le prochain message, n'a pas d'effet dans l'affichage imediat
        'force' permet de forcer l'affichage meme si le nombre d'indentation maximum est atteind
        """
        assert type(text) is str, "'text' doit etre une chaine de caractere, pas un %s." % type(text)
        
        nbr_colones_avant = self.nbr_colones                                    # le nombre de colones avant l'affichage
        indentation = self.get_indentation(ecart=ecart)                         # le nombre d'indentation pour l'affichage la tout de suite
        nbr_colones_maintenant = self.nbr_colones                               # le nombre de colone au moment de l'affichage
        ma_colone = self.ma_colone                                              # le numero de la colone ou l'on doit affiher la tout de suite. Les numeros de colones partent de 0
        size = self.get_size()                                                  # largeur du terminal
        if indentation + min(0, ecart) <= self.display or force:                # si il faut afficher car la limite d'indentation n'est pas encore atteinte
            if nbr_colones_avant == 1:                                          # si il n'y a qu'une seule colone
                print("\n".join((("    "*indentation + l)[:size] for l in text.split("\n"))))# et bien on se gene pas
            else:                                                               # par contre, si il y a plusieurs colones
                for ligne in text.split("\n"):
                    debut = (" "*(size//nbr_colones_avant - 1)+"|")*ma_colone   # partie gauche du message
                    if ma_colone + 1 < nbr_colones_avant:
                        milieu = ("    "*indentation + ligne + " "*size)[:(size//nbr_colones_avant - 1)] # la partie centrale avec l'affichage
                        fin = ("|" + " "*(size//nbr_colones_avant-1))*(nbr_colones_avant-ma_colone-2) + "|"
                    else:
                        milieu = ""
                        fin = ("    "*indentation + ligne)[:(size//nbr_colones_avant - 1)]
                    print(debut + milieu + fin)
        
        if self.nbr_colones != nbr_colones_avant:
            return None
            raise NotImplementedError("La liaison et la suppression des colones n'est pas assuree")

    def __enter__(self):
        """
        permet de pouvoir etre appelle avec 'with'
        """
        self.show(self.text, ecart=1)
        return self

    def __exit__(self, type, value, traceback):
        """
        appelle l'orsque l'on sort du bloc 'with'
        """
        if (type, value, traceback) == (None, None, None):
            self.show("Success!", ecart=-1)
        else:
            erreur = str(value)
            if erreur:
                self.show("Failure! : %s" % erreur, ecart=-1)
            else:
                self.show("Failure!", ecart=-1)

class Str(str):
    """
    extension de l'objet 'str' primitatf a python
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self = str(*args, **kwargs)

    def indice(self):
        """
        retourne une chaine ou tous les caracteres sont en indices
        en cas d'echec, retourne la chaine telle quelle etait
        """
        correspondance = {" ":" ", "\t":"\t",
            "0":"₀", "1":"₁", "2":"₂", "3":"₃", "4":"₄", "5":"₅", "6":"₆", "7":"₇", "8":"₈", "9":"₉",
            "a":"ₐ", "b":"ɂ", "c":"ɂ", "d":"ɂ", "e":"ₑ", "f":"ɂ", "g":"ɂ", "h":"ₕ", "i":"ᵢ", "j":"ⱼ", "k":"ₖ", "l":"ₗ", "m":"ₘ", "n":"ₙ", "o":"ₒ", "p":"ₚ", "q":"ɂ", "r":"ᵣ", "s":"ₛ", "t":"ₜ", "u":"ᵤ", "v":"ᵥ", "w":"ɂ", "x":"ₓ", "y":"ɂ", "z":"ɂ",
            "A":"ɂ", "B":"ʙ", "C":"ϲ", "D":"ɂ", "E":"ɂ", "F":"ɍ", "G":"ɢ", "H":"ʜ", "I":"ɪ", "J":"ȷ", "K":"κ", "L":"ʟ", "M":"м", "N":"ɴ", "O":"ο", "P":"ɂ", "Q":"ǫ", "R":"ʀ", "S":"ɂ", "T":"ɂ", "U":"ɂ", "V":"ɂ", "W":"ɯ", "X":"х", "Y":"ʏ", "Z":"ƶ",
            "(":"₍", ")":"₎", "+":"₊", "-":"₋", "=":"₌",
            "°":"˳", "~":"˷", ",":"ˏ"
            }
        
        chaine_indice = ""              # la chaine qui va etre renvoyee
        ind = [i for n,i in correspondance.items()]# liste qui contient tous les caractere en indices

        for car in self:                # pour chaqun des caractere de la chaine a metre en indice
            if car in correspondance:   # si on sait le convertir
                chaine_indice += correspondance[car]# on converti le caractere affin d'en donner ca representation en indice
            elif car in ind:            # si le caractere est deja un caractere en indice
                chaine_indice += car    # on le laisse tel qu'elle
            else:                       # si ce n'est ni l'un ni l'autre
                return self             # alors on ne sait pas faire!
        return Str(chaine_indice)       # si on sort de la boucle, c'est que on a bien reussi la convertion

    def exposant(self):
        """
        retourne la chaine en metant les caracteres en exposants
        en cas d'echec, retourne la chaine de caractere telle qu'elle etait sans rien changer
        """
        correspondance = {" ":" ", "\t":"\t",
            "0":"⁰", "1":"¹", "2":"²", "3":"³", "4":"⁴", "5":"⁵", "6":"⁶", "7":"⁷", "8":"⁸", "9":"⁹",
            "a":"?", "b":"?", "c":"?", "d":"?", "e":"?", "f":"?", "g":"?", "h":"?", "i":"?", "j":"?", "k":"?", "l":"?", "m":"?", "n":"?", "o":"?", "p":"?", "q":"?", "r":"?", "s":"?", "t":"?", "u":"?", "v":"?", "w":"?", "x":"?", "y":"?", "z":"?",
            "A":"?", "B":"?", "C":"?", "D":"?", "E":"?", "F":"?", "G":"?", "H":"?", "I":"?", "J":"?", "K":"?", "L":"?", "M":"?", "N":"?", "O":"?", "P":"?", "Q":"?", "R":"?", "S":"?", "T":"?", "U":"?", "V":"?", "W":"?", "X":"?", "Y":"?", "Z":"?",
            }
        
        chaine_exposant = ""            # la chaine qui va etre renvoyee
        ind = [i for n,i in correspondance.items()]# liste qui contient tous les caracteres en exposant

        for car in self:                # pour chaqun des caractere de la chaine a metre en exposant
            if car in correspondance:   # si on sait le convertir
                chaine_exposant += correspondance[car]# on converti le caractere affin d'en donner ca representation en exposant
            elif car in ind:            # si le caractere est deja un caractere en exposant
                chaine_exposant += car  # on le laisse tel qu'elle
            else:                       # si ce n'est ni l'un ni l'autre
                return self             # alors on ne sait pas faire!
        return Str(chaine_exposant)     # si on sort de la boucle, c'est que on a bien reussi la convertion

class Temprep(str):
    """
    cree puis detruit un dossier temporaire
    la representation de cet objet est le chemin absolu de ce repertoire
    """
    def __new__(cls):
        return super(Temprep, cls).__new__(cls, tempfile.mkdtemp())

    def __init__(self, destroy=True):
        self.destroy = destroy # True imposse de supprimer le repertoire a la fin, False le laisse en vie

    def __del__(self):
        if self.destroy:
            try:
                shutil.rmtree(self)
            except KeyboardInterrupt as e:
                raise e from e
            except Exception as e:
                try:
                    import importlib
                    import shutil
                    importlib.reload(shutil)
                    shutil.rmtree(self)
                except Exception as e:
                    pass

class Translator:
    """
    permet de traduire du texte
    se base sur un dictionaire de la forme:
    {
    langue_source1:
        {
        message1:
            {
            langue_destination1: message_traduit1,
            langue_destination2: message_traduit2
            },
        message2:
            {
            langue_destination1: message_traduit1,
            langue_destination2: message_traduit2
            }
        },
    langue_source2:
        {
        message1:
            {
            langue_destination1: message_traduit1,
            langue_destination2: message_traduit2
            },
        message2:
            {
            langue_destination1: message_traduit1,
            langue_destination2: message_traduit2
            }
        }
    }
    """
    def __init__(self, src, dest):
        if os.path.exists(os.path.join(str(raisin.temprep), "translation_table.json")):# si on a un endroit ou stocker les resultats
            self.save = True                        # on retient qu'il faut les enregistrer pour la prochaine fois 
            with open(os.path.join(str(raisin.temprep), "translation_table.json"), "r") as f:# on recupere ceux qui sont deja stockee
                self.translation_table = json.load(f)# pour cela on utilise json qui est plus lisible
        else:                                       # si l'on a pas d'espace dedier
            self.save = False                       # on ne va pas se permetre d'en prendre un!
            self.translation_table = {}             # tous va rester dans la rame
        self.src = src                              # langue des messages a traduire
        if dest == "auto":                          # si on ne sait pas dans quelle langue traduire
            self.dest = self.get_local_language()   # on traduit dans la langue du pays ou l'on est
        else:                                       # si la langue de sortie est imposee
            self.dest = dest                        # on se pli aux voeux
        self.last = time.time()

    def __call__(self, message, src="default", dest="default"):
        """
        cette methode permet une traduction plus discrete
        """
        if src == "default":                        # si la source n'est pas imposee
            src = self.src                          # on prend la source par defautl
        if dest == "auto":                          # si la langue de destination doit etre adapte
            dest = self.get_local_language()        # on refait une requette
        elif dest == "default":                     # si par contre on demand de bien garder la meme langue de destination
            dest = self.dest                        # on ne fait pas le difficile
        return self.translate(message, src=src, dest=dest)

    def translate(self, message, src, dest):
        """
        traduit le message 'message'
        ce message est ecrit dans la langue 'src'
        ce message va etre traduit dans la langue 'dest'
        retourne le message traduit
        en cas d'echec, retourne le message d'origine
        """
        @timeout_decorator(5)
        def traduire_internet(message, src, dest):
            if googletrans:
                return googletrans.Translator().translate(message, src=src, dest=dest).text
            return message

        if src == "default":                        # si la source n'est pas imposee
            src = self.src                          # on prend la source par defautl
        if dest == "auto":                          # si la langue de destination doit etre adapte
            dest = self.get_local_language()        # on refait une requette
        elif dest == "default":                     # si par contre on demand de bien garder la meme langue de destination
            dest = self.dest                        # on ne fait pas le difficile

        if src == dest:                                                         # si le texte est deja dans la bonne langue
            return message                                                      # on ne fait pas vraiment d'effort
        if dest in self.translation_table.get(src, {}).get(message, {}):        # de meme, si il est deja traduit, on evite
            return self.translation_table[src][message][dest]                   # de le traduire a nouveau
        if not googletrans:                                                     # si googletrans n'est pas installe
            return message                                                      # on ne peut pas aller plus loin
        
        try:                                                                    # si il n'est pas traduit, on va le faire avec google traduction
            if src not in self.translation_table:                               # il faut donc d'abord preparer le terrain
                self.translation_table[src] = {}                                # en s'assurant que l'on puisse enregister le resultat au bon endroit
            if message not in self.translation_table[src]:                      # c'est pourquoi l'on verifie que
                self.translation_table[src][message] = {}                       # le chemin d'acces soit complet, on le cre si nesessaire
            self.translation_table[src][message][dest] = traduire_internet(message, src, dest)# c'est la qu'on peu enfin traduire le message
        except KeyboardInterrupt as e:                                          # si pandant la traduction, l'utilisateur en a marre
            raise e from e                                                      # on lui donne la prioritee
        except Exception as e:                                                  # si une autre erreur survient
            raise e from e
            return message                                                      # tant pis on abandonne la traduction

        self.save_ardware()                                                     # on enregistre ce changement affin de pouvoir en profiter la prochaine fois
        return self.translation_table[src][message][dest]                       # puis on retourne efin le message traduit

    def save_ardware(self):
        """
        ecrase le fichier json pour enregistrer un fichier plus recent
        """
        if not self.save:                           # si l'on a pas le droit d'enregistrer
            return None                             # on ne fait rien
        if time.time()-self.last < 10:              # si on a fait une mise a jour il y a moin de 10 secondes
            return None                             # on ne fait iren non plus
        self.last = time.time()                     # si il faut se metre au boulot, on le fait mais on s'aprette tout de meme a en faire le moin possible
        with open(os.path.join(str(raisin.temprep), "translation_table.json"), "w") as f:
            json.dump(f, self.translation_table)

    def get_local_language(self):
        """
        retourne les initiale de la langue locale
        """
        if "language" in self.translation_table:
            return self.translation_table["language"]
        if raisin.Id().country is not None:
            self.translation_table["language"] = raisin.Id().country
            return raisin.Id().country
        return "fr"

def timeout_decorator(timeout):
    """
    |=========================|
    | Ajoute un timeout a une |
    | fontion ou une methode. |
    |=========================|

    Controle le temps d'excecution d'une fonction.
    Attention, La fonction decoree doit s'executer dans le programe
    courant (pas de multiprocessing).

    entree
    ------
    :param timeout: Temps permis a la fonction pour s'executer.
    :type timeout: float, int

    sortie
    ------
    :return: Une fonction qui decore une fonction.
    :rtype: callable

    exemple
    -------
    :Example:
    >>> from raisin.tools import timeout_decorator
    >>> import time
    >>>
    >>> @timeout_decorator(30)
    ... def wait():
    ...     time.sleep(60)
    ...
    >>> wait()
    raisin.errors.TimeoutError
    >>>
    """
    def decorator(primary_func):
        """
        |=============================|
        | Modifie la fonction afin de |
        | lui ajouter un timeout.     |
        |=============================|

        entree
        ------
        :param primary_func: Fonction quelqonque que l'on shouaite decorer.
        :type primary_func: callable

        sortie
        ------
        :return: La fonction decoree.
        :rtype: callable
        """
        def modified_func(*args, **kwargs):
            """
            |========================|
            | Fonction avec timeout. |
            |========================|

            Cette fonction prend exactement les memes arguments
            que la fonction primaire.
            Cette fonction retourne exactement les memes choses
            que la fonction primaire, sauf si le temps d'execution
            de la fonction primaire depasse 'timeout.'

            :raises TimeoutError: En cas de temps trop long.
            """
            class Timeout(threading.Thread):
                def __init__(self, func, *args, **kwargs):
                    threading.Thread.__init__(self)
                    self.func = func                # Fonction a decorer.
                    self.args = args
                    self.kwargs = kwargs
                    self.value = None
                    self.fail = True                # False si un resultat a ete renvoye dans le temps imparti.
                    self.error = None              # L'erreur si il y en a une.
                
                def run(self):
                    try:
                        self.value = self.func(*self.args, **self.kwargs)
                    except Exception as e:
                        self.error = e
                    else:
                        self.fail = False

            encapsulation = Timeout(primary_func, *args, **kwargs) # On la met dans un thread.
            encapsulation.start() # On lance le thread.
            encapsulation.join(timeout=timeout) # On genere un timeout si besoin.
            if encapsulation.fail:
                if encapsulation.error:
                    raise encapsulation.error
                import raisin.errors as errors
                raise errors.TimeoutError
            return encapsulation.value
        
        assert hasattr(primary_func, "__call__"), \
            "Il faut decorer une fonction ou une methode. Pas un %s." \
            % type(primary_func).__name__

        return modified_func

    assert isinstance(timeout, int) or isinstance(timeout, float), \
        "'timeout' doit etre un nombre. Pas un %s." % type(timeout).__name__
    assert timeout > 0, "'timeout' doit etre strictement positif."

    return decorator

def get_temperature(dt=0):
    """
    |=================================|
    | Recupere la temperature du CPU. |
    |=================================|

    En cas d'echec, retourne None.

    :platform: Unix, Mac

    Parameters
    ----------
    :param dt: Duree en seconde de la mesure.
    :type dt: float

    Returns
    -------
    :return: La temperature moyenne en °C.
    :rtype: float

    Example
    -------
    :Example:
    >>> from raisin.tools import get_temperature
    >>>
    >>> get_temperature()
    58.0
    >>>
    """
    def get():
        """
        Recupere la liste des temperature instentanement.
        """
        # Avec Psutil
        try:
            return [t.current for t in psutil.sensors_temperatures()["coretemp"]]
        except AttributeError:
            if os.name == "nt":
                p.show("Haha! t'as cru que microchiotte windaube sait lire la temperature! A ton avis, pourquoi tant de CPU grillent avec ce system?\n"\
                       "Plus serieusement, si tu tiens a cette option, passe sur un vrai systeme d'exploitation...")
                return None
            if psutil.__version__ < "5.1":
                p.show("Cette option est diponible a partir de la version 5.1, vous avez la %s. Vous pouvez taper: '%s -m pip install --upgrade psutil'." % (psutil.__version__, sys.executable))
            p.show("Cette option ne semble pas disponible, le module 'psutil' devrai avoir une fonction 'sensors_temperatures'. Or, ce n'est pas le cas.")
        
        # Sur raspberry
        try:
            with open("/opt/vc/bin/vcgencmd", "r") as ftemp:
                return [int(ftemp.read())/1000]
        except (FileNotFoundError, PermissionError):
            pass
        
        # Sur linux
        temp = []
        for file in glob.iglob("/sys/class/thermal/thermal_zone*/temp"):
            try:
                with open(file, "r") as ftemp:
                    temp.append(int(ftemp.read())/1000)
            except (FileNotFoundError, PermissionError):
                continue
        return temp if temp else None
    
    assert type(dt) in (float, int), \
        "'dt' doit etre un entier ou un flotant, pas un %s." % type(dt)
    with Printer("Get the CPU temperature...") as p:
        try:
            import psutil
        except ImportError:
            p.show("'psutil' est nessecaire pour pouvoir recuperer la temperature.")
            return None
        t_init = time.time()
        temperatures = get()
        if not temperatures:
            return None
        else:
            while t_init + dt > time.time():
                time.sleep(0.08)
                temperatures.extend(get())
            
            p.show("°C, ".join(map(str, temperatures[-16:])) + "°C")
            longueur = len(temperatures)
            if longueur % 2:
                temp = sorted(temperatures)[longueur//2]
            temperatures.sort()
            temp = (temperatures[longueur//2-1] + temperatures[longueur//2])/2
            return temp

def improve_recursion_decorateur(increment):
    """
    permet d'eviter les problemes de limites de recursion
    car si il y a un probleme, la limite est augmentee de 'increment'
    """
    assert type(increment) is int, "'increment' doit etre un entier, '%s' n'est pas un entier, c'est un %s." % (increment, type(increment))
    assert increment > 0, "'increment' doit etre strictement positif, ce n'est pas le cas de %d." % increment

    def decorateur(fonction_a_executer):

        def fonction_modifiee(*args, **kwargs):
            args_copie = copy.copy(args)
            kwargs_copie = copy.copy(kwargs)
            while 1:
                try:
                    return fonction_a_executer(*args_copie, **kwargs_copie)
                except RecursionError as e:
                    if sys.getrecursionlimit() >= 10000:                                    # si on a deja depasse une limite raisonable de recursion
                        raise e from e                                                      # on est surement dans une boucle infinie, donc on ne s'entete pas
                    try:
                        avant = sys.getrecursionlimit()
                        sys.setrecursionlimit(min(10000, avant + increment))                # si il y a trop de recursions par exemple a + b + c - g * 3 + ...
                    except Exception as e:
                        raise e from e
                    logging.warning("Recursion limit increased from %d to %d." % (avant, sys.getrecursionlimit()))
                    continue
                except Exception as e:
                    raise e from e
        return fonction_modifiee
    return decorateur

identity = Id()
temprep = Temprep()
