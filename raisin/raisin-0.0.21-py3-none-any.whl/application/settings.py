#!/usr/bin/env python3

"""
Gestion de la persistance des parametres de configuration
de l'application.
C'est ici que l'on enregistre les parametres et que
l'on va les extraire aussi.
"""

import copy
import os
import pprint
import re
import socket
import sys
import time

import psutil

from ..tools import Printer, identity, get_temperature
from .hmi import dialog
from .hmi import checks
from ..communication import constants

class Settings:
    """
    Permet d'acceder et de modifier les parametres.
    """
    def __init__(self, *, home=os.path.expanduser("~"), action="normal"):
        assert action in ("paranoiac", "normal", "altruistic", "custom"), \
            "Les actions ne peuvent que etre 'paranoiac', " \
            + "'normal', 'altruistic' ou 'custom'. Pas '%s'." % action
        
        self.home = home
        self.action = action # facon dont on doit choisir les parametre par defaut
        self.last_read = 0 # date de la derniere lecture sur le support physique.
        self.settings = {} # les parametres dictionaire
        self.original_settings = {} # les parametres initiaux

    def _load_settings(self):
        """
        Recupere le contenu du fichier 'settings.py'
        Retourne ce contenu deserialise
        ou bien renvoi {} si le fichier n'est pas existant ou corrompu.
        """
        if time.time() - self.last_read > 60*10:
            self.last_read = time.time()
            return load_settings(home=self.home)
        return self.settings
    
    def _dump_settings(self):
        """
        Enregistre les paramettres "self.settings".
        Attention, si self.settings n'est pas initalise,
        Tous les parametres sont perdus.
        """
        settings = copy.deepcopy(self.settings)
        if hasattr(self, "dns_ipv6") and self.dns_ipv6:
            settings["server"]["dns_ipv6"] = self.dns_ipv6
        if hasattr(self, "dns_ipv6") and self.dns_ipv4:
            settings["server"]["dns_ipv4"] = self.dns_ipv4
        dump_settings(settings, home=self.home)

    def _is_complete(self, settings, ref=None):
        """
        Retourne True si tous les champs sont presents.
        Retourne False si il y a un champ de trop ou qu'il en manque un.
        """
        model = {
         'account': {'automatic_update': None,
                     'email': None,
                     'give_activity_schedules': None,
                     'give_cpu_usage': None,
                     'give_internet_activity': None,
                     'give_ram_usage': None,
                     'padlock': {'break_time': None,
                                 'cipher': None,
                                 'notify_by_email': None,
                                 'paths': {'excluded_paths': None,
                                           'paths': None}},
                     'security': {'hash': None,
                                  'private_key': None,
                                  'psw': None,
                                  'sel': None,
                                  'public_key': None,
                                  'sentence_memory': None},
                     'username': None},
         'cluster_work': {'downflow': None,
                          'free_size': None,
                          'limit_bandwidth': None,
                          'limit_cpu_usage': None,
                          'limit_fan_noise': None,
                          'limit_ram_usage': None,
                          'low_cpu_usage': None,
                          'maximum_temperature': None,
                          'recording_directory': None,
                          'restrict_access': None,
                          'rising_flow': None,
                          'schedules_bandwidth': {'friday': None,
                                                  'monday': None,
                                                  'saturday': None,
                                                  'sunday': None,
                                                  'thursday': None,
                                                  'tuesday': None,
                                                  'wednesday': None},
                          'schedules_cpu_usage': {'friday': None,
                                                  'monday': None,
                                                  'saturday': None,
                                                  'sunday': None,
                                                  'thursday': None,
                                                  'tuesday': None,
                                                  'wednesday': None},
                          'schedules_fan_noise': {'friday': None,
                                                  'monday': None,
                                                  'saturday': None,
                                                  'sunday': None,
                                                  'thursday': None,
                                                  'tuesday': None,
                                                  'wednesday': None},
                          'schedules_ram_usage': {'friday': None,
                                                  'monday': None,
                                                  'saturday': None,
                                                  'sunday': None,
                                                  'thursday': None,
                                                  'tuesday': None,
                                                  'wednesday': None}},
         'server': {'accept_new_client': None,
                    'access_token': None,
                    'dns_ipv4': None,
                    'dns_ipv6': None,
                    'force_authentication': None,
                    'listen': None,
                    'network_name': None,
                    'port': None,
                    'port_forwarding': None}}
        if ref == None:
            ref = model

        for clef in ref:
            if clef not in settings:
                return False
            if ref[clef] != None:
                if not self._is_complete(settings[clef], ref=ref[clef]):
                    return False
        for clef in settings:
            if clef not in ref:
                return False
        return True

    def get_settings(self):
        """
        Si des parametres sont deja enregistres, il sont juste completes.
        Sinon, les parametres par defaut sont renvoyes.
        """
        settings = self._load_settings()                            # on recupere les parametres existants
        if not self._is_complete(settings):
            with Printer("Account settings...") as p:
                settings["account"] = settings.get("account", {})

                p.show("Load Username")
                settings["account"]["username"] = str(settings["account"].get("username", identity["username"]))
                if self.action == "custom":
                    settings["account"]["username"] = dialog.question_reponse(
                        "Username :",
                        default=settings["account"]["username"],
                        validatecommand=checks.username_verification)
                
                p.show("Load Email")
                if "email" not in settings["account"]:
                    import raisin
                    settings["account"]["email"] = str(settings["account"].get("email",
                        re.search(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}", raisin.__author__).group()))
                if self.action == "custom":
                    settings["account"]["email"] = dialog.question_reponse(
                        "Email :",
                        default=settings["account"]["email"],
                        validatecommand=checks.email_verification)
                
                p.show("Load Security")
                if "security" not in settings["account"]:             # si il n'y a pas de clef publique ou de clef privee
                    import raisin.security as security
                    private_key, public_key = security.rsa_keys()     # on commence par generer le couple de clef
                    settings["account"]["security"] = {
                        "private_key": private_key,
                        "public_key": public_key,
                        "hash": None,                                     # on ne va pas choisir un mot de passe
                        "psw": None,                                      # a la place de l'utilisateur
                        "sel": b"",                                        # donc on n'en met pas
                        "sentence_memory": ""}
                if self.action in ("custom", "paranoiac"):                 # si il faut tout de metre en metre un
                    import raisin.security as security
                    settings["account"]["security"] = security.change_psw(save_dico=settings)

                p.show("Load Vie privee")
                if self.action == "custom":
                    settings["account"]["give_internet_activity"] = dialog.question_binaire(
                        "Donner des informations concerant ma connection a internet ?")
                elif self.action == "paranoiac" or self.action == "normal":
                    settings["account"]["give_internet_activity"] = False
                elif self.action == "altruistic":
                    settings["account"]["give_internet_activity"] = True
                else:
                    settings["account"]["give_internet_activity"] = settings["account"].get("give_internet_activity", False)
                if self.action == "custom":
                    settings["account"]["give_activity_schedules"] = dialog.question_binaire(
                        "Donner des informations concerant l'alimentation de mon ordinateur ?")
                elif self.action == "paranoiac" or self.action == "normal":
                    settings["account"]["give_activity_schedules"] = False
                elif self.action == "altruistic":
                    settings["account"]["give_activity_schedules"] = True
                else:
                    settings["account"]["give_activity_schedules"] = settings["account"].get("give_activity_schedules", False)
                if self.action == "custom":
                    settings["account"]["give_cpu_usage"] = dialog.question_binaire(
                        "Donner des informations concerant la sollicitation du CPU ?")
                elif self.action == "paranoiac":
                    settings["account"]["give_cpu_usage"] = False
                elif self.action == "normal" or self.action == "altruistic":
                    settings["account"]["give_cpu_usage"] = True
                else:
                    settings["account"]["give_cpu_usage"] = settings["account"].get("give_cpu_usage", True)
                if self.action == "custom":
                    settings["account"]["give_ram_usage"] = dialog.question_binaire(
                        "Donner des informations concerant l'utilisation de la RAM ?")
                elif self.action == "paranoiac":
                    settings["account"]["give_ram_usage"] = False
                elif self.action == "normal" or self.action == "altruistic":
                    settings["account"]["give_ram_usage"] = True
                else:
                    settings["account"]["give_ram_usage"] = settings["account"].get("give_ram_usage", True)
                if self.action == "custom":
                    settings["account"]["automatic_update"] = dialog.question_binaire(
                        "Faire les mises a jours automatiquement ?")
                elif self.action == "paranoiac":
                    settings["account"]["automatic_update"] = False
                elif self.action == "normal" or self.action == "altruistic":
                    settings["account"]["automatic_update"] = True
                else:
                    settings["account"]["automatic_update"] = settings["account"].get("automatic_update", True)

                p.show("Load Padlock")
                if not "padlock" in settings["account"]:               # si il n'y a rien pour la gestion de l'antivol
                    settings["account"]["padlock"] = {
                        "cipher":False,                                     # chiffre les donnees personnelles et demande le mot de passe pour les remetres en clair
                        "paths":                                            # ce dictionaire contient les repertoire achiffrer et leur options
                            {
                            "paths": [],
                            "excluded_paths": [],
                            },
                        "break_time":3600,                                  # temps de pause ou l'on ne regarde pas l'ip
                        "notify_by_email":False,                            # m'envoyer un mail contenant l'ip, l'heure (le son et une image/video) l'orsque l'on chiffre les donnees perso
                    }

            with Printer("Cluster work settings...") as p:
                settings["cluster_work"] = settings.get("cluster_work", {})

                p.show("Load fan nose")
                if get_temperature() is None:    # si il n'est pas possible de recuperer la temperature
                    settings["cluster_work"]["limit_fan_noise"] = False
                else:
                    if self.action == "altruistic":
                        settings["cluster_work"]["limit_fan_noise"] = False
                    elif self.action == "custom":
                        settings["cluster_work"]["limit_fan_noise"] = dialog.question_binaire(
                            "Voulez-vous limiter le bruit du ventilateur?", default=True)
                    else:
                        settings["cluster_work"]["limit_fan_noise"] = settings["cluster_work"].get("limit_fan_noise", True)
                settings["cluster_work"]["schedules_fan_noise"] = settings["cluster_work"].get("schedules_fan_noise",
                    {
                    "monday" : {"8:00":False, "22:00":True},
                    "tuesday" : {"8:00":False, "22:00":True},
                    "wednesday" : {"8:00":False, "22:00":True},
                    "thursday" : {"8:00":False, "22:00":True},
                    "friday" : {"8:00":False, "22:00":True},
                    "saturday" : {"10:00":False, "23:00":True},
                    "sunday" : {"10:00":False, "23:00":True},
                    })
                settings["cluster_work"]["maximum_temperature"] = settings["cluster_work"].get("maximum_temperature", 60) # temperature qui rend l'ordinateur bruyant

                p.show("Load CPU restriction")
                if self.action == "altruistic":
                    settings["cluster_work"]["limit_cpu_usage"] = False
                elif self.action == "custom":
                    settings["cluster_work"]["limit_cpu_usage"] = dialog.question_binaire(
                        "Voulez-vous limiter le taux de CPU?", default=True)
                else:
                    settings["cluster_work"]["limit_cpu_usage"] = settings["cluster_work"].get("limit_cpu_usage", True)
                settings["cluster_work"]["low_cpu_usage"] = settings["cluster_work"].get("low_cpu_usage", False) # on ne peu pas juste le metre a True, car il a beaucoup de choses a faire
                taux = 50 if os.cpu_count() <= 1 else int(100*(os.cpu_count() - 1)/os.cpu_count()) # pour la regulation du CPU, on laisse 1 coeur libre
                settings["cluster_work"]["schedules_cpu_usage"] = settings["cluster_work"].get("schedules_cpu_usage",
                    {
                    "monday" : {"8:00":taux, "22:00":100},
                    "tuesday" : {"8:00":taux, "22:00":100},
                    "wednesday" : {"8:00":taux, "22:00":100},
                    "thursday" : {"8:00":taux, "22:00":100},
                    "friday" : {"8:00":taux, "22:00":100},
                    "saturday" : {"10:00":taux, "23:00":100},
                    "sunday" : {"10:00":taux, "23:00":100},
                    })

                p.show("Load RAM restriction")
                if self.action == "altruistic":
                    settings["cluster_work"]["limit_ram_usage"] = False
                elif self.action == "custom":
                    settings["cluster_work"]["limit_ram_usage"] = dialog.question_binaire(
                        "Voulez-vous limiter l'acces de la RAM?", default=True)
                else:
                    settings["cluster_work"]["limit_ram_usage"] = settings["cluster_work"].get("limit_ram_usage", True)
                maxi_virtual = 2*2**30 if not psutil else psutil.virtual_memory().total/2**20
                maxi_swap = 4*2**30 if not psutil else (psutil.swap_memory().total + psutil.virtual_memory().total)/2**20
                settings["cluster_work"]["schedules_ram_usage"] = settings["cluster_work"].get("schedules_ram_usage",
                    {
                    "monday" : {"8:00":int(maxi_virtual*0.75), "22:00":int(maxi_swap*0.9)},
                    "tuesday" : {"8:00":int(maxi_virtual*0.75), "22:00":int(maxi_swap*0.9)},
                    "wednesday" : {"8:00":int(maxi_virtual*0.75), "22:00":int(maxi_swap*0.9)},
                    "thursday" : {"8:00":int(maxi_virtual*0.75), "22:00":int(maxi_swap*0.9)},
                    "friday" : {"8:00":int(maxi_virtual*0.75), "22:00":int(maxi_swap*0.9)},
                    "saturday" : {"10:00":int(maxi_virtual*0.75), "23:00":int(maxi_swap*0.9)},
                    "sunday" : {"10:00":int(maxi_virtual*0.75), "23:00":int(maxi_swap*0.9)},
                    })

                p.show("Load bandwidth restriction")
                if self.action == "paranoiac":
                    settings["cluster_work"]["limit_bandwidth"] = True
                elif self.action == "custom":
                    settings["cluster_work"]["limit_bandwidth"] = dialog.question_binaire(
                        "Voulez-vous limiter la bande passante?", default=False)
                else:
                    settings["cluster_work"]["limit_bandwidth"] = settings["cluster_work"].get("limit_bandwidth", False)
                settings["cluster_work"]["schedules_bandwidth"] = settings["cluster_work"].get("schedules_bandwidth",
                    settings["cluster_work"]["schedules_fan_noise"])               # on met par defaut les memes horaires de limiation que celle du ventillateur
                settings["cluster_work"]["downflow"] = settings["cluster_work"].get("downflow", 0.5) # debit descendant en Mio/s
                settings["cluster_work"]["rising_flow"] = settings["cluster_work"].get("rising_flow", 0.1) # debit montant en Mio/s

                p.show("Load recording directory")
                settings["cluster_work"]["recording_directory"] = settings["cluster_work"].get("recording_directory",
                    os.path.join(self.home, ".raisin"))   # c'est le repertoire dans lequel on enregistre les resultats
                if self.action == "paranoiac":
                    settings["cluster_work"]["free_size"] = 50_000
                elif self.action == "altruistic":
                    settings["cluster_work"]["free_size"] = 1000
                else:
                    settings["cluster_work"]["free_size"] = settings["cluster_work"].get("free_size", 10_000) # place a laisser disponible en Mio

                p.show("Load restrict acces")
                if self.action == "paranoiac":
                    settings["cluster_work"]["restrict_access"] = True
                elif self.action == "custom":
                    settings["cluster_work"]["restrict_access"] = dialog.question_binaire(
                        "Voulez-vous restreindre les droits de l'application?", default=False)
                else:
                    settings["cluster_work"]["restrict_access"] = settings["cluster_work"].get("restrict_access", False)

            with Printer("Server settings...") as p:
                settings["server"] = settings.get("server", {})

                p.show("Load port information")
                if "port" not in settings["server"]:
                    with Printer("Search for an open local port..."):
                        for port in range(20000, 49152, 1): # range(1024, 49152, 1) mais c'est pour free
                            if port not in constants.RESERVED_PORTS and checks.port_verification(port):
                                settings["server"]["port"] = settings["server"]["port"] = port
                                break
                
                p.show("Load listen")
                settings["server"]["listen"] = settings["server"].get("listen", 2*os.cpu_count()) # par defaut, le serveur prend en charge 2 connection par thread

                p.show("Load network name")
                settings["server"]["network_name"] = settings["server"].get("network_name", "")

                p.show("Load DNS")
                settings["server"]["dns_ipv6"] = settings["server"].get("dns_ipv6", "")
                settings["server"]["dns_ipv4"] = settings["server"].get("dns_ipv4", "")
                self.dns_ipv6 = settings["server"]["dns_ipv6"] # sauvegarde pour ne pas
                self.dns_ipv4 = settings["server"]["dns_ipv4"] # les perdres a l'enregistrement
                if settings["server"]["dns_ipv6"]:
                    if not checks.dns_ip_verification(settings["server"]["dns_ipv6"], 6):
                        settings["server"]["dns_ipv6"] = None
                if settings["server"]["dns_ipv4"]:
                    if not checks.dns_ip_verification(settings["server"]["dns_ipv4"], 6):
                        settings["server"]["dns_ipv4"] = None
                print(self.dns_ipv6, self.dns_ipv4)
                if (not settings["server"]["dns_ipv6"]) or (not settings["server"]["dns_ipv4"]):
                    if identity["ipv6"] != None:
                        dns_ipv6 = socket.getfqdn(str(identity["ipv6"]))
                        if checks.dns_ip_verification(dns_ipv6, 6) and not settings["server"]["dns_ipv6"]:
                            settings["server"]["dns_ipv6"] = dns_ipv6
                    if identity["ipv4_wan"] != None:
                        dns_ipv4 = socket.getfqdn(str(identity["ipv4_wan"]))
                        if checks.dns_ip_verification(dns_ipv4, 4) and not settings["server"]["dns_ipv4"]:
                            settings["server"]["dns_ipv4"] = dns_ipv4

                p.show("Load port forwarding")
                settings["server"]["port_forwarding"] = settings["server"].get("port_forwarding", None)

                p.show("Load preferences")
                if self.action == "paranoiac":
                    settings["server"]["accept_new_client"] = False
                    settings["server"]["force_authentication"] = True
                elif self.action == "custom":
                    settings["server"]["accept_new_client"] = dialog.question_binaire(
                        "Demander mon autorisation avant d'accepter de nouveaux clients?", default=True)
                    settings["server"]["force_authentication"] = dialog.question_binaire(
                        "Forcer les clients a s'authentifier?", default=False)
                else:
                    settings["server"]["accept_new_client"] = settings["server"].get("accept_new_client", True)
                    settings["server"]["force_authentication"] = settings["server"].get("force_authentication", False)

                p.show("Load access token")
                settings["server"]["access_token"] = settings["server"].get("access_token", None)

        return settings

    def get_original(self, *clefs):
        """
        Recupere le parametre initial.
        """
        self.__call__()
        element = self.original_settings
        for clef in clefs:
            element = element[clef]
        return element

    def __call__(self):
        """
        Charge les paremetres pour les
        stocker dans l'attribut self.settings.
        """
        self.settings = self.get_settings()
        if not self.original_settings:
            self.original_settings = copy.deepcopy(self.settings)

    def __str__(self):
        self.__call__()
        return str(self.settings)

    def __repr__(self):
        self.__call__()
        return repr(self.settings)

    def __getitem__(self, clef):
        """
        Permet d'aller recuperer un parametre.
        """
        self.__call__()
        return self.settings[clef]

    def __setitem__(self, clef, item):
        """
        Permet d'aller modifier un parametre.
        Ne fait aucune verification.
        """
        self.__call__()
        self.settings[clef] = item
        self._dump_settings()
            
    def flush(self):
        """
        Force a ecrir l'etat actuel dans le disque.
        """
        if not self.settings:
            self.settings = self.get_settings()
        self._dump_settings()

def load_settings(*, home=os.path.expanduser("~")):
    """
    recupere le contenu du fichier 'settings.py'
    retourne ce contenu deserialise
    ou bien renvoi {} si le fichier n'est pas existant ou corrompu
    'home' est le repertoire courant de l'utilisateur.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with Printer(
            "Load settings for {}...".format(
            repr(os.path.basename(home)))) as p:
        rep = os.path.join(home, ".raisin")
        filename = "settings.py"
        if os.path.isdir(rep):
            if os.path.isfile(os.path.join(rep, filename)):
                try:
                    with open(os.path.join(rep, filename), "r", encoding="utf-8") as f:
                        return eval(f.read())
                except KeyboardInterrupt as e:
                    raise e from e
                except:
                    p.show("No valid file found")
                    return {}
        p.show("No valid file found")
        return {}

def dump_settings(settings, *, home=os.path.expanduser("~")):
    """
    enregistre les parametres
    ne fait aucune verification sur ces parametres
    'home' est le repertoire courant de l'utilisateur.
    """
    assert isinstance(home, str), \
        "'home' have to be 'str', not %s." % type(home).__name__
    assert os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with Printer("Save settings for {}...".format(
            repr(os.path.basename(home)))):
        os.makedirs(os.path.join(home, ".raisin"), exist_ok=True)
        os.makedirs(os.path.join(
            settings["cluster_work"]["recording_directory"], "results"),
            exist_ok=True)
        
        with open(os.path.join(home, ".raisin", "settings.py"),
                "w", encoding="utf-8") as f:
            stdcourant = sys.stdout
            sys.stdout = f
            try:
                pprint.pprint(settings)
            except Exception as e:
                raise e from e
            finally:
                sys.stdout = stdcourant

settings = Settings()
