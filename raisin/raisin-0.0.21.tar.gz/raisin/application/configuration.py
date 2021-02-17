#!/usr/bin/env python3

"""
|===================================|
| Permet de changer les parametres. |
|===================================|
"""

import shutil
import sys
import threading
import time

from . import settings, install, uninstall
from .hmi import tkinter, ttk, checks, dialog
from .hmi.theme import *
from .. import security
from ..tools import Printer, get_temperature, identity

class Config:
    """
    |================================|
    | Interface graphique permettant |
    | de configurer raisin.          |
    |================================|
    """
    def __init__(self, existing_window=None):
        """
        :param existing_window: Une fenetre tkinter presente par ailleur.
        """
        security.request_psw(force=True)
        self.settings = settings.settings
        if not tkinter:
            raise ImportError("La configuration n'est pas possible sans 'tkinter'.")
        if existing_window:             # si il y a deja une fenetre ouverte
            self.window = tkinter.Toplevel(existing_window) # on est oblige d'utiliser un toplevel sinon ca plante
            self.window.grab_set()      # on fige la fenetre parente
            self.window.protocol(
                "WM_DELETE_WINDOW",
                lambda: (self.window.destroy(), self.window.quit())) # il se trouve que ca semble fonctionner comme ca...
        else:                           # dans le cas ou aucune instance tkinter n'existe
            self.window = tkinter.Tk()  # et bien on en cre une tout simplement
        self.initializing_variables()   # on initialise les variables des widgets a partir de self.settings
        self.create_widgets()           # on rempli la fenetre avec les widget.configure()
        self.window.focus_force()       # on donne le focus a la nouvelle fenetre
        self.window.mainloop()          # on reste attentif aux actions de l'utilisateur
    
    def __del__(self):
        """
        Au moment de la destruction de la fenetre.
        """
        self.settings.flush()

    def initializing_variables(self):
        """
        Initialise toutes les variable et leur
        injecte la bonne valeur selon la configuration existante.
        """
        with Printer("Transfer of parameters to tkinter...") as p:
            p.show("Variable declaration")
            self.username_var = tkinter.StringVar()                 # variable qui comporte le username
            self.email_var = tkinter.StringVar()                    # variable qui comporte l'adresse email
            self.give_internet_activity_var = tkinter.IntVar()      # booleen concertant les statistiques d'internet, 0 => prive, 1 => publique
            self.give_activity_schedules_var = tkinter.IntVar()     # booleen concernant l'aliment ation du pc, 0 => prive, 1 => publique
            self.give_cpu_usage_var = tkinter.IntVar()              # booleen concernant les statistiques d'utilisation du CPU
            self.give_ram_usage_var = tkinter.IntVar()              # booleen concertant les statistique de remplissage de la RAM
            self.automatic_update_var = tkinter.IntVar()            # booleen qui dit si oui ou non, on fait les mises a jour

            self.limit_fan_noise_var = tkinter.IntVar()             # booleen qui dit si l'on regule ou non, le bruit du ventilateur
            self.maximum_temperature_var = tkinter.DoubleVar()      # c'est la temperature a partir de laquelle l'ordinateur devient bruyant
            self.limit_cpu_usage_var = tkinter.IntVar()             # booleen qui dit si on regule ou non l'utilisation du CPU
            self.low_cpu_usage_var = tkinter.IntVar()               # booleen qui dit si l'on met doit tenter de metre les rocessus en priorite basse
            self.limit_ram_usage_var = tkinter.IntVar()             # booleen qui dit si on regule ou non l'utilisation de la RAM
            self.limit_bandwidth_var = tkinter.IntVar()             # booleen qui dit si l'on doit ou non, limiter la bande passante
            self.recording_directory_var = tkinter.StringVar()      # repertoire d'enreigstrement des resultats
            self.free_size_var = tkinter.StringVar()                # espace memoire a laisser disponible dans le disque d'enregisrement des resultats
            self.restrict_access_var = tkinter.IntVar()             # booleen qui permet de savoir si on restreind les droits de cluster work

            self.port_var = tkinter.StringVar()                     # port d'ecoute du serveur
            self.listen_var = tkinter.StringVar()                   # nombre de connections maximum que le serveur accepte avant de rouspetter
            self.network_name_var = tkinter.StringVar()             # nom du reseau auquel on participe
            self.dns_ipv6_var = tkinter.StringVar()                 # nom de domaine ipv6
            self.dns_ipv4_var = tkinter.StringVar()                 # nom de domaine ipv4
            self.port_forwarding_var = tkinter.StringVar()          # port de redirection
            self.accept_new_client_var = tkinter.IntVar()           # booleen qui permet de dire si l'on demande ou non l'autorisation pour se connecter
            self.force_authentication_var = tkinter.IntVar()        # booleen qui permet de forcer l'authentification
            self.access_token_var = tkinter.StringVar()             # c'est l'access token pour dropbox

            p.show("Variable assignment")
            self.username_var.set(self.settings["account"]["username"]) # le username va apparaitre dans le Entry
            self.email_var.set(self.settings["account"]["email"])   # de meme, on fait apparaitre, l'email dans le entry
            self.give_internet_activity_var.set(self.settings["account"]["give_internet_activity"])# on met le bouton dans la bonne configuration
            self.give_activity_schedules_var.set(self.settings["account"]["give_activity_schedules"])
            self.give_cpu_usage_var.set(self.settings["account"]["give_cpu_usage"])
            self.give_ram_usage_var.set(self.settings["account"]["give_ram_usage"])
            self.automatic_update_var.set(self.settings["account"]["automatic_update"])

            self.limit_fan_noise_var.set(self.settings["cluster_work"]["limit_fan_noise"])
            self.maximum_temperature_var.set(self.settings["cluster_work"]["maximum_temperature"])
            self.limit_cpu_usage_var.set(self.settings["cluster_work"]["limit_cpu_usage"])
            self.low_cpu_usage_var.set(self.settings["cluster_work"]["low_cpu_usage"])
            self.limit_ram_usage_var.set(self.settings["cluster_work"]["limit_ram_usage"])
            self.limit_bandwidth_var.set(self.settings["cluster_work"]["limit_bandwidth"])
            self.recording_directory_var.set(self.settings["cluster_work"]["recording_directory"])
            self.free_size_var.set(str(self.settings["cluster_work"]["free_size"]) + " (Mio)")
            self.restrict_access_var.set(self.settings["cluster_work"]["restrict_access"])

            self.port_var.set(str(self.settings["server"]["port"]))
            self.listen_var.set(str(self.settings["server"]["listen"]))
            self.network_name_var.set(self.settings["server"]["network_name"])
            self.dns_ipv6_var.set(
                self.settings["server"]["dns_ipv6"]
                if self.settings["server"]["dns_ipv6"] else "")
            self.dns_ipv4_var.set(
                self.settings["server"]["dns_ipv4"]
                if self.settings["server"]["dns_ipv4"] else "")
            self.port_forwarding_var.set(
                str(self.settings["server"]["port_forwarding"])
                if self.settings["server"]["port_forwarding"] else "")
            self.accept_new_client_var.set(not self.settings["server"]["accept_new_client"]) # la question est tournee dans l'autre sens
            self.force_authentication_var.set(self.settings["server"]["force_authentication"])
            self.access_token_var.set(
                self.settings["server"]["access_token"]
                if self.settings["server"]["access_token"] else "")

    def create_widgets(self):
        """
        Mise en place du contenu des fenetres.
        """
        with Printer("Creation of wigets...") as p:
            with Printer("Main root..."):
                self.window.columnconfigure(0, weight=1)                # numero de colone, etirement relatif: On rend l'onglet redimenssionable sur la largeur
                self.window.rowconfigure(0, weight=1)                   # on rend le menu legerement etirable verticalement
                self.window.rowconfigure(1, weight=10)                  # mais tout de meme 10 fois moins que le reste
                self.window.title("Interface de configuration de raisin") # ajout d'un titre a la fenetre principale
                self.window.bind("<Escape>", lambda event: self.window.destroy()) # la fenetre est detruite avec la touche echappe
                notebook = theme(tkinter.ttk.Notebook(self.window))     # preparation des onglets
                notebook.grid(row=1, column=0, columnspan=5,            # on place les onglets sur une ligne en haut a gauche
                    sticky="ewsn")                                      # on fait en sorte que la fenetre prenne toute la place qu'elle peut                         
                self.window.event_add("<<update>>", "<Leave>", "<Return>")

            with Printer("Account tab..."):
                frame_account = theme(tkinter.Frame(notebook))          # creation d'un cadre pour deposer tous les widgets 'account'
                frame_account.columnconfigure(0, weight=1)              # la colone des operations en cours ne bougera pas trop
                frame_account.columnconfigure(1, weight=1)              # de meme, la colone des label ne change pas trop
                frame_account.columnconfigure(2, weight=30)             # par contre, celle qui comporte les champs de saisie s'etire le plus
                frame_account.columnconfigure(3, weight=1)              # la colone des infos et de l'aide ne bouge pas top non plus
                for i in range(1, 11):
                    frame_account.rowconfigure(i, weight=1)             # on va donner a chaque ligne le meme ration d'expension
                notebook.add(frame_account, text="Account")             # on ancre la fenetre dans le premier onglet
                
                p.show("Username")
                theme(tkinter.Label(frame_account, text="Username :")).grid(row=1, column=1, sticky="w") # il est plaque a gauche (w=west)
                username_widget = theme(tkinter.Entry(frame_account, textvariable=self.username_var)) # variable de la bare de saisie
                username_widget.bind("<<update>>", lambda event: self.username_set()) # on check des que l'on sort du champ
                username_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.username_canva))
                username_widget.grid(row=1, column=2, sticky="ew")      # prend toute la largeur
                theme(tkinter.Button(frame_account,
                    image=icons.info(),                               # icon affiche
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info username",
                        "Le 'username' permet de vous identifier plus facilement dans le reseau. "
                        "Des parametres comme l'adresse mac permetent déjà de vous identifier mais ce n'est pas très parlant.\n"
                        "Du point de vu crytographhique votre username sert de 'sel cryptographique'. "
                        "Ainsi, il est plus difficile de craquer votre mot de passe."),
                    )).grid(row=1, column=3)
                self.username_canva = theme(tkinter.Canvas(frame_account))
                self.username_canva.grid(row=1, column=0)

                p.show("Email")
                theme(tkinter.Label(frame_account, text="Email :")).grid(row=2, column=1, sticky="w")
                email_widget = theme(tkinter.Entry(frame_account, textvariable=self.email_var))
                email_widget.bind("<<update>>", lambda event: self.email_set())
                email_widget.bind("<KeyPress>", lambda event:
                    self.put_refresh(event, self.email_canva))
                email_widget.grid(row=2, column=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info email",
                        "Le fait de renseigner votre email permet de vous envoyer un nouveau mot de "
                        "passe si vous avez perdu l'ancien.\n"
                        "Du point de vu crytographique votre email sert de 'sel cryptographique'. "
                        "Ainsi, il est plus difficile de craquer votre mot de passe.")
                    )).grid(row=2, column=3)
                self.email_canva = theme(tkinter.Canvas(frame_account))
                self.email_canva.grid(row=2, column=0)

                p.show("Password")
                theme(tkinter.Button(frame_account,
                    text="Gerer le mot de passe",
                    command=self.security_set,
                    )).grid(row=3, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info mot de passe",
                        "Le mot de passe permet plusieur choses:\n"
                        " -Chiffrer les données.\n"
                        " -Empecher n'importe qui de tout casser facilement."),
                    )).grid(row=3, column=3)
                self.security_canva = theme(tkinter.Canvas(frame_account))
                self.security_canva.grid(row=3, column=0)

                p.show("Vie privee")
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_internet_activity_var,
                    text="Donner des informations concerant ma connection a internet",
                    command=self.give_internet_activity_set,            # action faite au moment de cocher et decocher la case
                    )).grid(row=4, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info internet",
                        "Si cette option est activee, les moments ou votre ordinateur "
                        "a accès à internet sont mémorisés. Ils sont en suite retransmis "
                        "au serveur principal.\nA quoi ça sert?\n"
                        "Cela permet d'optimiser la répartition des données pour tenter de "
                        "prédire les moments ou votre machine sera joingnable.")
                    )).grid(row=4, column=3)
                self.give_internet_activity_canva = theme(tkinter.Canvas(frame_account))
                self.give_internet_activity_canva.grid(row=4, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_activity_schedules_var,
                    text="Donner des informations concerant l'alimentation de mon ordinateur",
                    command=self.give_activity_schedules_set,
                    )).grid(row=5, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info alimentation",
                        "Si cette option est activee, les moments ou votre ordinateur "
                        "est allumé sont mémorisés. Ils sont en suite retransmis "
                        "au serveur principal.\nA quoi ça sert?\n"
                        "Cela permet d'optimiser la répartition des données pour éviter "
                        "de donner des tâches trop longues si il y a de forte chances "
                        "que votre ordinateur s'etaigne en cour de route.")
                    )).grid(row=5, column=3)
                self.give_activity_schedules_canva = theme(tkinter.Canvas(frame_account))
                self.give_activity_schedules_canva.grid(row=5, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_cpu_usage_var,
                    text="Donner des informations concerant la sollicitation du CPU",
                    command=self.give_cpu_usage_set,
                    )).grid(row=6, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info CPU",
                        "Si cette option est activee, Le taux d'utilisation du CPU est enrifistré."
                        "Cela permet d'anticiper les moments ou les resource de votre machines serons réduites."),
                    )).grid(row=6, column=3)
                self.give_cpu_usage_canva = theme(tkinter.Canvas(frame_account))
                self.give_cpu_usage_canva.grid(row=6, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.give_ram_usage_var,
                    text="Donner des informations concerant l'utilisation de la RAM",
                    command=self.give_ram_usage_set,
                    )).grid(row=7, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info RAM",
                        "Si cette option est activee, Le taux d'utilisation de la RAM est enrifistré."
                        "Cela permet de selectionner les taches a donner. En effet, si un calcul trop gourmand en RAM "
                        "est demandé, le processus est exterminé sur le champs. Prédire la disponibilité de la RAM permet "
                        "de limiter le génocide.")
                    )).grid(row=7, column=3)
                self.give_ram_usage_canva = theme(tkinter.Canvas(frame_account))
                self.give_ram_usage_canva.grid(row=7, column=0)
                theme(tkinter.Checkbutton(frame_account, 
                    variable=self.automatic_update_var,
                    text="Faire les mises a jours automatiquement",
                    command=self.automatic_update_set,
                    )).grid(row=8, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info upgrade",
                        "Faire les mises a jour automatiquement permet de bénéficier de nouvelles fonctionalitées, "
                        "de corriger des bugs, et d'en créer d'autres! A vous de voir!")
                    )).grid(row=8, column=3)
                self.automatic_update_canva = theme(tkinter.Canvas(frame_account))
                self.automatic_update_canva.grid(row=8, column=0)

                p.show("Padlock")
                theme(tkinter.Button(frame_account,
                    text="Gerer l'antivol",
                    command=self.padlock_set
                    )).grid(row=9, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(frame_account,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info padlock",
                        "Ce systeme de protection permet plusieures choses:\n"
                        " -Encrypter un dossier dès que l'ordi démare sur une nouvelle IP. "
                        "Des le chiffrage terminé, le mot de passe est demandé afin de tous décripter. "
                        "En cas de vol, cela empèche d'avoir acces aux données et à tous les sites qui demande un compte (facebook, zoom, discord...).\n"
                        " -Envoyer un couriel. Le couriel contient l'IP, la date et peut-être une image ou du son du potentiel voleur...")
                    )).grid(row=9, column=3)
                self.padlock_canvas = theme(tkinter.Canvas(frame_account))
                self.padlock_canvas.grid(row=9, column=0)

                p.show("Installation management")
                sous_frame_account = theme(tkinter.Frame(frame_account))
                sous_frame_account.grid(row=10, column=1, columnspan=2, sticky="ew")
                theme(tkinter.Button(sous_frame_account,
                    text="Reinstall",
                    command=lambda: (self.window.destroy(), # On ferme la fenetre de config avant d'en faire apparaitre d'atre.
                            icons.__init__(), # Evite des erreurs.
                            uninstall.main(), install.main())
                        if dialog.question_binaire(
                            "Etes vous certain de vouloir faire ça?",
                            default=True,
                            existing_window=self.window) else None
                    )).pack(side=tkinter.LEFT)
                theme(tkinter.Button(sous_frame_account,
                    text="Uninstall",
                    command=lambda: (uninstall.main(), self.window.quit())
                        if dialog.question_binaire(
                            "Etes vous certain de vouloir faire ça?",
                            default=True,
                            existing_window=self.window) else None
                    )).pack(side=tkinter.RIGHT)
                theme(tkinter.Button(sous_frame_account,
                    text="Purge",
                    command=lambda: sys.stderr.write("Not Implemented!\n")
                    )).pack()

            with Printer("Resource sharing tab..."):
                frame_cluster = theme(tkinter.Frame(notebook))         # creation de la fenetre pour la gestion du calcul parallele
                frame_cluster.columnconfigure(0, weight=1)              # la colone des operation en cours ne se deforme pas beaucoup
                frame_cluster.columnconfigure(1, weight=10)             # Les 3 colones cenrale
                frame_cluster.columnconfigure(2, weight=1)              # s'ecartenent toutes
                frame_cluster.columnconfigure(3, weight=10)             # de la meme maniere
                frame_cluster.columnconfigure(4, weight=1)              # enfin, la colone des infos ne bouge pas trop non plus
                frame_cluster.columnconfigure(5, weight=10)
                frame_cluster.columnconfigure(6, weight=1)
                for i in range(8):
                    frame_cluster.rowconfigure(i, weight=1)
                notebook.add(frame_cluster, text="Resource Sharing")        # on ancre cette fenetre
                
                p.show("Nose")
                state_fan_noise = "disable" if get_temperature() is None else "normal"
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_fan_noise_var,
                    text="Limiter le bruit du ventilateur",
                    command=self.limit_fan_noise_set,
                    state=state_fan_noise,
                    )).grid(row=1, column=1, sticky="ew")
                self.limit_fan_noise_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_fan_noise_canva.grid(row=1, column=0)
                self.schedules_fan_noise_button = theme(tkinter.Button(frame_cluster,
                    text="Horaires de limitation",
                    command=self.schedules_fan_noise_set,
                    state=state_fan_noise if self.settings["cluster_work"]["limit_fan_noise"] else "disable"
                   ))
                self.schedules_fan_noise_button.grid(row=1, column=3, sticky="ew")
                self.schedules_fan_noise_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_fan_noise_canva.grid(row=1, column=2)
                self.calibration_temperature_button = theme(tkinter.Button(frame_cluster,
                    text="Calibration",
                    command=self.maximum_temperature_set,
                    state=state_fan_noise if self.settings["cluster_work"]["limit_fan_noise"] else "disable"
                   ))
                self.calibration_temperature_button.grid(row=1, column=5, sticky="ew")
                self.maximum_temperature_canva = theme(tkinter.Canvas(frame_cluster))
                self.maximum_temperature_canva.grid(row=1, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info nose",
                        "Il arrive que les ordinateurs soient bruillant a cause du ventillateur. "
                        "Or la vitesse du ventillateur dépend essentiellement de la température des CPUs. "
                        "Cette option permet donc de calmer le processus dès que le CPU atteind une certaine température.")
                    )).grid(row=1, column=6)

                p.show("CPU")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_cpu_usage_var,
                    text="Limiter L'utilisation du CPU",
                    command=self.limit_cpu_usage_set
                    )).grid(row=2, column=1, sticky="ew")
                self.limit_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_cpu_usage_canva.grid(row=2, column=0)
                self.schedules_cpu_usage_button = theme(tkinter.Button(frame_cluster,
                    text="f: horaire -> limitation",
                    command=self.schedules_cpu_usage_set,
                    state="normal" if self.settings["cluster_work"]["limit_cpu_usage"] else "disable"
                   ))
                self.schedules_cpu_usage_button.grid(row=2, column=3, sticky="ew")
                self.schedules_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_cpu_usage_canva.grid(row=2, column=2)
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.low_cpu_usage_var,
                    text="Priorité basse",
                    command=self.low_cpu_usage_set
                    )).grid(row=2, column=5, sticky="ew")
                self.low_cpu_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.low_cpu_usage_canva.grid(row=2, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info CPU",
                        "Reguler l'utilisation du cpu permet de garantir une réactivité de l'ordinateur.")
                    )).grid(row=2, column=6)

                p.show("RAM")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_ram_usage_var,
                    text="Limiter L'utilisation de la RAM",
                    command=self.limit_ram_usage_set
                    )).grid(row=3, column=1, sticky="ew")
                self.limit_ram_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_ram_usage_canva.grid(row=3, column=0)
                self.schedules_ram_usage_button = theme(tkinter.Button(frame_cluster,
                    text="f: horaire -> limitation",
                    command=self.schedules_ram_usage_set,
                    state="normal" if self.settings["cluster_work"]["limit_ram_usage"] else "disable"
                   ))
                self.schedules_ram_usage_button.grid(row=3, column=3, sticky="ew")
                self.schedules_ram_usage_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_ram_usage_canva.grid(row=3, column=2)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info RAM",
                        "Reguler l'utilisation de la ram permet de garantir de ne pas figer l'ordinateur!")
                    )).grid(row=3, column=6)

                p.show("Bandwidth")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.limit_bandwidth_var,
                    text="Limiter la bande passante",
                    command=self.limit_bandwidth_set
                    )).grid(row=4, column=1, sticky="ew")
                self.limit_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.limit_bandwidth_canva.grid(row=4, column=0)
                self.schedules_verification_button = theme(tkinter.Button(frame_cluster,
                    text="Horaires de limitation",
                    command=self.schedules_bandwidth_set,
                    state="normal" if self.settings["cluster_work"]["limit_bandwidth"] else "disable"
                    ))
                self.schedules_verification_button.grid(row=4, column=3, sticky="ew")
                self.schedules_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.schedules_bandwidth_canva.grid(row=4, column=2)
                self.calibration_bandwidth_button = theme(tkinter.Button(frame_cluster,
                    text="Calibration",
                    command=self.maximum_bandwidth_set,
                    state="normal" if self.settings["cluster_work"]["limit_bandwidth"] else "disable"
                    ))
                self.calibration_bandwidth_button.grid(row=4, column=5, sticky="ew")
                self.maximum_bandwidth_canva = theme(tkinter.Canvas(frame_cluster))
                self.maximum_bandwidth_canva.grid(row=4, column=4)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info bandwidth",
                        "Limiter la bande passante permet d'assurer a l'utilisateur un debit minimum.")
                    )).grid(row=4, column=6)
               
                p.show("Recording")
                theme(tkinter.Label(frame_cluster, text="Repertoire d'enregistrement:")).grid(row=5, column=1, sticky="w")
                theme(tkinter.Label(frame_cluster, textvariable=self.recording_directory_var)).grid(row=5, column=3)
                self.recording_directory_canva = theme(tkinter.Canvas(frame_cluster))
                self.recording_directory_canva.grid(row=5, column=0)
                theme(tkinter.Button(frame_cluster,
                    text="Changer l'emplacement",
                    command=self.recording_directory_set
                    )).grid(row=5, column=5, sticky="ew")
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info recording",
                        "Ce repertoire est le repertoire dans lequel est enregistre tous les resultats.\n"
                        "Les resultats, c'est l'ensemble de toutes les donnees dont il faut se souvenir.")
                    )).grid(row=5, column=6)
                theme(tkinter.Label(frame_cluster, text="Espace disponible:")).grid(row=6, column=1, sticky="w")
                theme(tkinter.Label(frame_cluster, textvariable=self.free_size_var)).grid(row=6, column=3)
                theme(tkinter.Button(frame_cluster,
                    text="Changer l'espace",
                    command=self.free_size_set
                    )).grid(row=6, column=5, sticky="ew")
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info size",
                        "La valeur rentree la est la quantitee d'espace disque a ne pas depasser. "
                        "A force de stocker des resultats, cela pourrai finir par saturer le disque "
                        "dure. Mais grace a cette option, des que le disque dur atteint un niveau critique de remplissage, "
                        "raisin compresse les resultats, supprime ceux qui sont peu utilise... Bref il se debrouille "
                        "pour ne pas depasser le cota que vous lui permettez, meme si il doit en venir a tout supprimmer!")
                    )).grid(row=6, column=6)
                self.free_size_canva = theme(tkinter.Canvas(frame_cluster))
                self.free_size_canva.grid(row=6, column=0)

                p.show("Access")
                theme(tkinter.Checkbutton(frame_cluster,
                    variable=self.restrict_access_var,
                    text="Restreindre l'acces a ce repertoire",
                    command=self.restrict_access_set
                    )).grid(row=7, column=1, columnspan=5, sticky="ew")
                self.restrict_access_canva = theme(tkinter.Canvas(frame_cluster))
                self.restrict_access_canva.grid(row=7, column=0)
                theme(tkinter.Button(frame_cluster,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info acces",
                        "Quand cette option est cochée, La partie de raisin qui travail pour les autre "
                        "voit ces droits extremement reduit. En effet, il n'a acces en lecture et en ecriture que dans le repertoire "
                        "d'enregistrement des résultats, les droits d'excecution dans l'environement python "
                        "et les droits de lecture dans le repertoire .raisin. Partout ailleur, il n'a plus aucun droit.\n"
                        "Cela peut etre vu comme un avantage pour la securité, mais ça peut aussi etre embetant.")
                    )).grid(row=7, column=6)

            with Printer("Server tab..."):
                frame_server = tkinter.Frame(notebook, bg=JAUNE)        # creation de la fenetre pour la gestion de l'hebergement d'un serveur
                frame_server.columnconfigure(0, weight=1)
                frame_server.columnconfigure(1, weight=1)
                frame_server.columnconfigure(2, weight=30)
                frame_server.columnconfigure(3, weight=1)
                for i in range(9):
                    frame_server.rowconfigure(i, weight=1)
                notebook.add(frame_server, text="Server")               # on ancre cette fenetre

                p.show("Local port")
                theme(tkinter.Label(frame_server, text="Port local:")).grid(row=0, column=1, sticky="w")
                port_box = theme(tkinter.Spinbox(frame_server,
                    textvariable=self.port_var,
                    from_=1,
                    to=49151,
                    increment=1))
                port_box.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.port_canva))
                port_box.bind("<<update>>", lambda event: self.port_set())
                port_box.grid(row=0, column=2, sticky="ew")
                self.port_canva = theme(tkinter.Canvas(frame_server))
                self.port_canva.grid(row=0, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info port",
                        "Ce port la est le port d'ecoute sur le reseau local. Quand d'autre machines veulents "
                        "s'addresser a vous, elles cherchent a vous contacter par ce port la. Il faut donc vous assurer "
                        "que ce port est ouvert (pour que les autres puissent vous joindre). "
                        "Il faut aussi que vous choisissez un port qui ne soit pas pris par une autre application.")
                    )).grid(row=0, column=3)

                p.show("Listen")
                theme(tkinter.Label(frame_server, text="Nombre max de conections:")).grid(row=1, column=1, sticky="w")
                listen_box = theme(tkinter.Spinbox(frame_server,
                    textvariable=self.listen_var,
                    from_=1,
                    to=10000,
                    increment=1,
                    ))
                listen_box.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.listen_canva))
                listen_box.bind("<<update>>", lambda event: self.listen_set())
                listen_box.grid(row=1, column=2, sticky="ew")
                self.listen_canva = theme(tkinter.Canvas(frame_server))
                self.listen_canva.grid(row=1, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info listen",
                        "Ce nombre correpond au nombre de requette que le serveur acceptera avant de les refuser. "
                        "Par defaut, il en accepte 2 par coeurs dans la machine, soit %d." % (2*os.cpu_count()))
                    )).grid(row=1, column=3)

                p.show("Network name")
                theme(tkinter.Label(frame_server, text="Cluster identifier:")).grid(row=2, column=1, sticky="w")
                network_name_widget = theme(tkinter.Entry(frame_server, textvariable=self.network_name_var)) # variable de la bare de saisie
                network_name_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.network_name_canva))
                network_name_widget.bind("<<update>>", lambda event: self.network_name_set()) # on check des que l'on sort du champ
                network_name_widget.grid(row=2, column=2, sticky="ew")
                self.network_name_canva = theme(tkinter.Canvas(frame_server))
                self.network_name_canva.grid(row=2, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info cluster identifier",
                        "Ce champs de saisie permet de choisir avec quel "
                        "cluster vous shouaitez partager vos resources.\n"
                        "Il y a 4 possibilités:\n"
                        "1) Vous voulez etre lié avec le réseau mondial de base:\n"
                        "Vous devez alors entrer le mot 'main'.\n"
                        "2) Vous voulez rejoindre un cluster spécifique déjà existant:\n"
                        "Il vous faut alors chercher 2 informations, le port pour acceder "
                        "au server et l'adresse ip ou dns de ce serveur. "
                        "Dans la zonne de saisie, écrivez:\n"
                        "port@ip\n"
                        "en ramplacant 'port' par le numero de port et 'ip' par "
                        "l'adresse ip ou le dns.\n"
                        "3) Vous voulez administrer votre propre réseau:\n"
                        "Saisissez alors le nom que vous voulez donner a votre réseau.\n"
                        "4) Vous ne pigez rien a ce charabia:\n"
                        "Laissez cette case vide.")
                    )).grid(row=2, column=3)

                p.show("DNS")
                theme(tkinter.Label(frame_server, text="DNS ipv6:")).grid(row=3, column=1, sticky="w")
                dns_ipv6_widget = theme(tkinter.Entry(frame_server, textvariable=self.dns_ipv6_var))
                dns_ipv6_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.dns_ipv6_canva))
                dns_ipv6_widget.bind("<<update>>", lambda event: self.dns_ip_set(6))
                dns_ipv6_widget.grid(row=3, column=2, sticky="ew")
                self.dns_ipv6_canva = theme(tkinter.Canvas(frame_server))
                self.dns_ipv6_canva.grid(row=3, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info dns ipv6",
                        "Bien que les adresses ipv6 changent moin que l'ipv4, elles sont suceptible de bouger. "
                        "Si vous êtes suffisement geek pour vous creer un nom de domaine DNS, c'est de loin la meilleur "
                        "solution pour vous joindre n'importe quand depuis n'importe ou!")
                    )).grid(row=3, column=3)
                theme(tkinter.Label(frame_server, text="DNS ipv4:")).grid(row=4, column=1, sticky="w")
                dns_ipv4_widget = theme(tkinter.Entry(frame_server, textvariable=self.dns_ipv4_var))
                dns_ipv4_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.dns_ipv4_canva))
                dns_ipv4_widget.bind("<<update>>", lambda event: self.dns_ip_set(4))
                dns_ipv4_widget.grid(row=4, column=2, sticky="ew")
                self.dns_ipv4_canva = theme(tkinter.Canvas(frame_server))
                self.dns_ipv4_canva.grid(row=4, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info dns ipv4",
                        "Votre ipv4 est succeptible de changer! Du coup, les autres client/serveur de raisin "
                        "peuvent metre du temps a retrouver vorte adresse. Pour rendre cette tache très repide et efficace, "
                        "vous pouvez vous créer un nom de domaine DNS et le rentrer dans cette case.")
                    )).grid(row=4, column=3)

                p.show("Port forwarding")
                theme(tkinter.Label(frame_server, text="Port forwarding:")).grid(row=5, column=1, sticky="w")
                
                port_forwarding_bis = self.port_forwarding_var.get() # Car la spinbox change la valeur.
                port_forwarding_box = theme(tkinter.Spinbox(frame_server,
                    textvariable=self.port_forwarding_var,
                    from_=1,
                    to=49151,
                    increment=1))
                port_forwarding_box.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.port_forwarding_canva))
                port_forwarding_box.bind("<<update>>", lambda event: self.port_forwarding_set())
                port_forwarding_box.grid(row=5, column=2, sticky="ew")
                self.port_forwarding_canva = theme(tkinter.Canvas(frame_server))
                self.port_forwarding_canva.grid(row=5, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info redirection",
                        "Pour vous contacter, il faut au moin une ip et un port. Seulement votre port peut etre vu "
                        "que de chez vous. Si un client exterieur veux vous contacter, il faut que vous mettiez en place "
                        "une 'redirection de port'. Dans cette case, vous pouvez entrer le port publique exterieur de votre box.")
                    )).grid(row=5, column=3)
                self.port_forwarding_var.set(port_forwarding_bis)

                p.show("Preferences")
                theme(tkinter.Checkbutton(frame_server,
                    variable=self.accept_new_client_var,
                    text="Demander mon autorisation avant d'accepter les nouveaux clients",
                    command=self.accept_new_client_set
                    )).grid(row=6, column=1, columnspan=2, sticky="ew")
                self.accept_new_client_canva = theme(tkinter.Canvas(frame_server))
                self.accept_new_client_canva.grid(row=6, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info autorisation",
                        "Si cette option est cochee, toutes les personnes qui veulent "
                        "se connecter a votre serveur ne pourrons pas le faire tant que vous n'aurez pas donné "
                        "explicitement l'autorisation. Par contre, une fois le feu vert donné, "
                        "les personnes autorisée peuvent se connecter sans limites.")
                    )).grid(row=6, column=3)
                theme(tkinter.Checkbutton(frame_server,
                    variable=self.force_authentication_var,
                    text="Forcer les clients a prouver leur identité",
                    command=self.force_authentication_set
                    )).grid(row=7, column=1, columnspan=2, sticky="ew")
                self.force_authentication_canva = theme(tkinter.Canvas(frame_server))
                self.force_authentication_canva.grid(row=7, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info autentification",
                        "Si cette option est cochee, tous ce qui veulent vous contacter "
                        "doivent prouver que c'est bien eux. Cette methode d'autentification fonctionne a partir "
                        "des clefs RSA. Cela est bon pour la securité mais ralenti enormément la vitesse de votre serveur "
                        "car a chaque connection, vous envoyez un defit au client et vous attendez sa reponsse avant "
                        "d'établir la connection pour de bon.")
                    )).grid(row=7, column=3)

                p.show("Access token")
                theme(tkinter.Label(frame_server, text="Dropbox access token:")).grid(row=8, column=1, sticky="w")
                access_token_widget = theme(tkinter.Entry(frame_server, textvariable=self.access_token_var))
                access_token_widget.bind("<KeyPress>", lambda event: 
                    self.put_refresh(event, self.access_token_canva))
                access_token_widget.bind("<<update>>", lambda event: self.access_token_set())
                access_token_widget.grid(row=8, column=2, sticky="ew")
                self.access_token_canva = theme(tkinter.Canvas(frame_server))
                self.access_token_canva.grid(row=8, column=0)
                theme(tkinter.Button(frame_server,
                    image=icons.info(),
                    command=lambda: tkinter.messagebox.showinfo(
                        "Info acces token",
                        "Les access token dropbox sont des clefs d'acces pour un dossier particulier de votre compte dropbox. "
                        "Ceci permet de pouvoir assurer une liaison avec vorte machine dpuis l'exterieur meme si "
                        "vous n'avez pas de redirection de port. Cela permet aussi de remplacer le DNS.\n"
                        "Si vous ne savez pas comment faire, visitez ce lien: https://dropbox.tech/developers/"
                        "generate-an-access-token-for-your-own-account\n"
                        "cela ressemble à ça: 'iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x'.")
                    )).grid(row=8, column=3)

    def username_set(self):
        """
        Verifie que le username soit correcte.
        Affiche une icone adequate.
        Pousse le changemement.
        """
        with Printer("Username update...") as p:
            username = self.username_var.get()
            if self.settings["account"]["username"] != username:
                if not checks.username_verification(username):
                    p.show("Invalid username '%s'" % username)
                    self.username_canva.delete("all")
                    self.username_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["account"]["username"] = username
                    self.username_canva.delete("all")
                    self.username_canva.create_image(8, 8, image=icons.ok())
            if self.settings.get_original("account", "username") == username:
                self.username_canva.delete("all")

    def email_set(self):
        """
        Verifie que l'adresse email soit correcte.
        Affiche une icone adequat.
        Pousse les modifications si il y en a.
        """
        with Printer("Email update...") as p:
            email = self.email_var.get()
            if self.settings["account"]["email"] != email:
                if not checks.email_verification(email):
                    p.show("Invalid email address")
                    self.email_canva.delete("all")
                    self.email_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["account"]["email"] = email
                    self.email_canva.delete("all")
                    self.email_canva.create_image(8, 8, image=icons.ok())
            if self.settings.get_original("account", "email") == email:
                self.email_canva.delete("all")

    def security_set(self):
        """
        Alias vers raisin.security.change_psw().
        """
        with Printer("Psw update...") as p:
            self.security_canva.delete("all")
            self.security_canva.create_image(8, 8, image=icons.refresh())
            import raisin.security as security
            try:
                security.change_psw(existing_window=self.window)
            except KeyboardInterrupt as e:
                self.security_canva.delete("all")
                self.security_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.security_canva.delete("all")
            self.security_canva.create_image(8, 8, image=icons.ok())

    def give_internet_activity_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give internet activity update...") as p:
            self.give_internet_activity_canva.delete("all")
            self.give_internet_activity_canva.create_image(8, 8, image=icons.ok())
            self.settings["account"]["give_internet_activity"] = bool(self.give_internet_activity_var.get())

    def give_activity_schedules_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give activity schedules update...") as p:
            self.give_activity_schedules_canva.delete("all")
            self.give_activity_schedules_canva.create_image(8, 8, image=icons.ok())
            self.settings["account"]["give_activity_schedules"] = bool(self.give_activity_schedules_var.get())

    def give_cpu_usage_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give CPU usage update...") as p:
            self.give_cpu_usage_canva.delete("all")
            self.give_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            self.settings["account"]["give_cpu_usage"] = bool(self.give_cpu_usage_var.get())

    def give_ram_usage_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("Give RAM usage update...") as p:
            self.give_ram_usage_canva.delete("all")
            self.give_ram_usage_canva.create_image(8, 8, image=icons.ok())
            self.settings["account"]["give_ram_usage"] = bool(self.give_ram_usage_var.get())

    def automatic_update_set(self):
        """
        Change l'action du boutton.
        """
        with Printer("'automatic update' update...") as p:
            self.automatic_update_canva.delete("all")
            self.automatic_update_canva.create_image(8, 8, image=icons.refresh())
            self.settings["account"]["automatic_update"] = bool(self.automatic_update_var.get())
            if self.settings["account"]["automatic_update"]:
                import raisin.application.upgrade as upgrade
                try:
                    rep = upgrade.find_folder()
                except OSError as e:
                    self.automatic_update_canva.delete("all")
                    self.automatic_update_canva.create_image(8, 8, image=icons.error())
                    raise e from e
                if identity["has_admin"]:
                    for d, _, fs in os.walk(rep):
                        os.chmod(d, 0o777)
                        for f in fs:
                            os.chmod(os.path.join(d, f), 0o777)
                else:
                    try:
                        with open(os.path.join(rep, "temp"), "w"):
                            pass
                    except PermissionError:
                        self.automatic_update_canva.delete("all")
                        self.automatic_update_canva.create_image(8, 8, image=icons.error())
                        raise PermissionError(
                            "Impossible de modifier les droits d'ecriture "
                            "de %s." % repr(rep)) from None
                    else:
                        os.remove(os.path.join(rep, "temp"))
            self.automatic_update_canva.delete("all")
            self.automatic_update_canva.create_image(8, 8, image=icons.ok())
            

    def padlock_set(self):
        """
        Interagit avec l'utilisateur afin de recuperer ces volontees vis a vis de l'antivol.
        L'interaction se fait via self._padlock_change().
        Verifi que la saisie soit correcte grace a checks.padlock_verication(...).
        Si la saisie est bonne, les nouveaux parametres sont enregistres.
        """
        with Printer("Padlock update...") as p:
            self.padlock_canvas.delete("all")
            self.padlock_canvas.create_image(8, 8, image=icons.refresh())
            try:
                change_padlock(existing_window=self.window)
            except KeyboardInterrupt as e:
                self.padlock_canvas.delete("all")
                self.padlock_canvas.create_image(8, 8, image=icons.error())
                raise e from e
            self.padlock_canvas.delete("all")
            self.padlock_canvas.create_image(8, 8, image=icons.ok())

    def limit_fan_noise_set(self):
        """
        Applique le changement du boutton.
        """
        with Printer("Limit fan noise update...") as p:
            self.limit_fan_noise_canva.delete("all")
            self.limit_fan_noise_canva.create_image(8, 8, image=icons.ok())
            limit_fan_noise = bool(self.limit_fan_noise_var.get())
            self.settings["cluster_work"]["limit_fan_noise"] = limit_fan_noise
            self.schedules_fan_noise_button.configure(state="normal" if limit_fan_noise else "disable")
            self.calibration_temperature_button.configure(state="normal" if limit_fan_noise else "disable")

    def schedules_fan_noise_set(self):
        """
        Alias vers raisin.application.hmi.schedules.get_schedules().
        Avec des valeurs en tout ou rien.
        """
        def converter(chaine):
            if chaine == "True" or chaine == "1":
                return True
            elif chaine == "False" or chaine == "0":
                return False
            raise ValueError(
                "'True', '1', 'False' ou '0' est attendu, pas %s." \
                % repr(chaine))

        with Printer("Schedules fan noise update...") as p:
            self.schedules_fan_noise_canva.delete("all")
            self.schedules_fan_noise_canva.create_image(8, 8, image=icons.refresh())
            import raisin.application.hmi.schedules as schedules
            try:
                self.settings["cluster_work"]["schedules_fan_noise"] = schedules.get_schedules(
                    self.settings["cluster_work"]["schedules_fan_noise"],
                    ylabel="limitation (y/n)",
                    converter=converter,
                    existing_window=self.window)
            except KeyboardInterrupt as e:
                self.schedules_fan_noise_canva.delete("all")
                self.schedules_fan_noise_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.schedules_fan_noise_canva.delete("all")
            self.schedules_fan_noise_canva.create_image(8, 8, image=icons.ok())

    def maximum_temperature_set(self):
        """
        Applique le changement du boutton.
        """
        with Printer("Maximum temperature update...") as p:
            self.maximum_temperature_canva.delete("all")
            self.maximum_temperature_canva.create_image(8, 8, image=icons.refresh())
            temperature = self._temperature_change()
            if not checks.temperature_verification(temperature):
                p.show("Il y a eu un probleme pour la calibration de la temperature seuil.")
                self.maximum_temperature_canva.delete("all")
                self.maximum_temperature_canva.create_image(8, 8, image=icons.error())
                raise ValueError(
                    "Les donnees de la temperature sont foireuses, aucun changement n'est opere.")
            self.settings["cluster_work"]["maximum_temperature"] = temperature
            self.maximum_temperature_canva.delete("all")
            self.maximum_temperature_canva.create_image(8, 8, image=icons.ok())

    def _temperature_change(self):
        """
        retourne la valeur de la nouvelle temperature
        """
        def quit(fen):
            """
            detruit la fenetre
            """
            class Tueur(threading.Thread):
                def __init__(self, papa):
                    threading.Thread.__init__(self)
                    self.papa = papa
                def run(self):
                    temperature_reader.je_dois_me_butter = True
                    while temperature_reader.is_alive():
                        pass
                    temperature_reader.consigne_glob.value = -1
                    fen.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
                    if "window" in self.papa.__dict__:                                      # on applique ou non la methode destroy
                        fen.quit()
            
            t = Tueur(self)
            t.start()
            valider.configure(state="disable")

        def consigne_verification(string_var):
            try:
                temperature = int(string_var.get()) if string_var.get().isdigit() else float(string_var.get())
            except ValueError:
                string_var.set(string_var.get()[:-1])
            else:
                string_var.set(str(max(20, min(100, temperature))))

        class TemperatureReader(threading.Thread):
            """
            meusure la temperature en temp reel du processeur
            et l'ecrit dans meusure_var
            """
            def __init__(self, consigne_temp, meusuree_var, consigne_glob, meusuree_glob):
                threading.Thread.__init__(self)
                self.consigne_temp = consigne_temp
                self.meusuree_var = meusuree_var
                self.consigne_glob = consigne_glob
                self.meusuree_glob = meusuree_glob
                self.je_dois_me_butter = False
                self.signature = time.time()

            def run(self):
                """
                methode lancee au moment du .start()
                """
                while not self.je_dois_me_butter:
                    temp_moy = get_temperature(0.2)
                    self.meusuree_var.set(str(round(temp_moy, 1)))
                    self.meusuree_glob.value = temp_moy                                 # on donne l'etat courant
                    self.consigne_glob.value = float(consigne_temp.get())               # et la consigne a atteindre

        def temperature_increases(consigne_glob, meusuree_glob):
            """
            adapte l'utilisation du cpu affin de le faire
            chauffer jusqu'a la temperature de consigne
            """
            cons = 1                                                                    # valeur bidon pour pouvoir demarer
            alpha = 0                                                                   # taux de cpu entre 0 et 1
            while cons > 0:                                                             # tant que l'on ne doit pas ce succider
                cons = consigne_glob.get_obj().value                                    # on recupere la temperature a atteindre
                meus = meusuree_glob.get_obj().value                                    # et la temperature actuelle
                
                alpha = max(0, min(1, alpha + (cons - meus)/1000))
                for i in range(int(alpha*6e6)):
                    pass
                time.sleep(0.1*(1-alpha))

        import ctypes
        import multiprocessing

        # initialisation de la fenetre
        if "window" in self.__dict__:                                               # si il y a deja une fenetre ouverte
            window = tkinter.Toplevel(self.window)                                  # on est oblige d'utiliser un toplevel sinon ca plante
            window.grab_set()                                                       # on fige la fenetre parente
            window.protocol("WM_DELETE_WINDOW", lambda: quit(window))               # il se trouve que ca semble fonctionner comme ca...
        else:                                                                       # dans le cas ou aucune instance tkinter n'existe
            window = tkinter.Tk()                                                   # et bien on en cre une tout simplement
            self.get_icons()

        # configuration de la fenetre
        window.title("Calibration temperature")
        window.configure(background=JAUNE)
        window.columnconfigure(0, weight=2)
        window.columnconfigure(1, weight=30)
        window.columnconfigure(2, weight=1)
        for i in range(4):
            window.rowconfigure(i, weight=1)
        window.focus_force()
        window.bind("<Escape>", lambda event: quit(window))

        # initialisation des variables
        try:
            import psutil
            psutil = True
        except ImportError:
            psutil = False
        temperature_var = tkinter.StringVar()                                       # contient la representation str de la temperature
        temperature_var.set(float(self.settings["cluster_work"]["maximum_temperature"])) # dans laquelle on injecte la temperature courante
        consigne_temp = tkinter.StringVar()                                         # contient la formule de la consigne en temperature
        consigne_temp.set("60")
        meusuree_var = tkinter.StringVar()                                          # contient la valeur de la temperature meusuree
        consigne_glob = multiprocessing.Value(ctypes.c_double, 60.0)                # contient la consigne mais c'est une variable global, pour passer entre les processus
        meusuree_glob = multiprocessing.Value(ctypes.c_double)                      # cette variable permet de transmetre la temperature meusuree aux threads
        temperature_reader = TemperatureReader(consigne_temp, meusuree_var, consigne_glob, meusuree_glob)
        threads = [multiprocessing.Process(target=temperature_increases, args=(consigne_glob, meusuree_glob)) for i in range(os.cpu_count())]

        # remplissage de la fenetre
        theme(tkinter.Label(window, text="Température de consigne (°C):")).grid(row=0, column=0, sticky="w")
        consigne_box = theme(tkinter.Spinbox(window,
            textvariable = consigne_temp,
            from_ = 20,
            to = 100,
            increment = 1
            ))
        consigne_box.bind("<Return>", lambda event: consigne_verification(consigne_temp))
        consigne_box.bind("<KeyRelease>", lambda event: consigne_verification(consigne_temp))
        consigne_box.grid(row=0, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info consigne temperature",
                "Pour vous aider a trouver le seuil de temperature, vous pouvez essayer "
                "d'imposer une température au processeur en l'entrant dans ce champ de saisie.\n"
                "Aussitot, raisin va changer le taux d'utilisation du CPU afin d'emener l'ordinateur a "
                "la temperature demandee.")
            )).grid(row=0, column=2)
        theme(tkinter.Label(window, text="Température meusuree (°C):")).grid(row=1, column=0, sticky="w")
        theme(tkinter.Label(window, textvariable=meusuree_var)).grid(row=1, column=1)
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info temperature meusuree",
                ("La valeur affichee est la valeur de la temperature reel actuelle. "
                "Elle est le resultat de la moyenne des "
                "temperatures de chacun des %d CPUs." % os.cpu_count()) \
                if psutil else \
                "Il faut installer le module 'psutil'.")
            )).grid(row=1, column=2)
        theme(tkinter.Label(window, text="Temperature de seuil (°C):")).grid(row=2, column=0, sticky="w")
        temperature_box = theme(tkinter.Spinbox(window,
            textvariable = temperature_var,
            from_ = 20,
            to = 100,
            increment = 1
            ))
        temperature_box.bind("<Return>", lambda event: consigne_verification(temperature_var))
        temperature_box.bind("<KeyRelease>", lambda event: consigne_verification(temperature_var))
        temperature_box.grid(row=2, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info temperature seuil",
                "La temperature entree ici est la temperature limite a partir de laquelle le ventillateur "
                "commence a faire trop de bruit. Dans les moments ou la temperature est regulee (reglage depuis la fenetre parente), "
                "raisin fait son possible pour que l'ordinateur ne depasse pas cette temperature la.")
            )).grid(row=2, column=2)
        valider = theme(tkinter.Button(window, text="Valider", command=lambda: quit(window)))
        valider.grid(row=3, column=0, columnspan=2)

        temperature_reader.start()
        for p in threads:
            p.start()
        window.mainloop()

        return float(temperature_var.get())

    def limit_cpu_usage_set(self):
        """
        Applique le changement du boutton.
        """
        with Printer("Limit cpu usage update...") as p:
            self.limit_cpu_usage_canva.delete("all")
            self.limit_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            limit_cpu_usage = bool(self.limit_cpu_usage_var.get())
            self.settings["cluster_work"]["limit_cpu_usage"] = limit_cpu_usage
            self.schedules_cpu_usage_button.configure(state="normal" if limit_cpu_usage else "disable")

    def schedules_cpu_usage_set(self):
        """
        Alias vers raisin.application.hmi.schedules.get_schedules().
        Avec un taux de limitation du CPU.
        """
        def converter(chaine):
            if not chaine.isdigit():
                raise ValueError("Un entier est attendu.")
            entier = int(chaine)
            if entier < 0 or entier > 100:
                raise ValuError(
                    "Un pourcentage doit etre compris entre "
                    "0 et 100, pas %d." % entier)
            return entier

        with Printer("Schedules cpu usage restriction update") as p:
            self.schedules_cpu_usage_canva.delete("all")
            self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.refresh())
            import raisin.application.hmi.schedules as schedules
            try:
                self.settings["cluster_work"]["schedules_cpu_usage"] = schedules.get_schedules(
                    self.settings["cluster_work"]["schedules_cpu_usage"],
                    ylabel="maximum cpu admissible (%)",
                    converter=converter,
                    existing_window=self.window)
            except KeyboardInterrupt as e:
                self.schedules_cpu_usage_canva.delete("all")
                self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.schedules_cpu_usage_canva.delete("all")
            self.schedules_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            
    def low_cpu_usage_set(self):
        """
        Tente de metre les processus en priorite basse.
        """
        with Printer("Low priority cpu usage update...") as p:
            self.low_cpu_usage_canva.delete("all")
            self.low_cpu_usage_canva.create_image(8, 8, image=icons.ok())
            self.settings["cluster_work"]["low_cpu_usage"] = bool(self.low_cpu_usage_var.get())

    def limit_ram_usage_set(self):
        """
        Applique le changement du boutton.
        """
        with Printer("Limit ram usage update") as p:
            self.limit_ram_usage_canva.delete("all")
            self.limit_ram_usage_canva.create_image(8, 8, image=icons.ok())
            limit_ram_usage = bool(self.limit_ram_usage_var.get())
            self.settings["cluster_work"]["limit_ram_usage"] = limit_ram_usage
            self.schedules_ram_usage_button.configure(state="normal" if limit_ram_usage else "disable")

    def schedules_ram_usage_set(self):
        """
        Alias vers raisin.application.hmi.schedules.get_schedules().
        Avec la quantite de RAM maximum prise par le system
        a laisser disponible.
        """
        class Converter:
            def __init__(self):
                try:
                    import psutil
                except:
                    self.maximum = 8*2**20 # Si on a aucune info sur la ram, on fait la supposition qu'elle fait 8 Gio.
                else:
                    self.maximum = int((
                        psutil.swap_memory().total + psutil.virtual_memory().total
                        )/2**10) # Elle est en Kio, on la met en Mio
            def __call__(self, chaine):
                value = int(chaine)
                if value < 0 or value > self.maximum:
                    raise ValueError(
                        "Doit etre compris entre 0 Mio et %f Mio." \
                        % self.maximum)
                return value

        with Printer("Schedules ram usage restriction update...") as p:
            self.schedules_ram_usage_canva.delete("all")
            self.schedules_ram_usage_canva.create_image(8, 8, image=icons.refresh())
            import raisin.application.hmi.schedules as schedules
            try:
                self.settings["cluster_work"]["schedules_ram_usage"] = schedules.get_schedules(
                    self.settings["cluster_work"]["schedules_ram_usage"],
                    ylabel="maximum ram admissible (Mio)",
                    converter=Converter(),
                    existing_window=self.window)
            except KeyboardInterrupt as e:
                self.schedules_ram_usage_canva.delete("all")
                self.schedules_ram_usage_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.schedules_ram_usage_canva.delete("all")
            self.schedules_ram_usage_canva.create_image(8, 8, image=icons.ok())

    def limit_bandwidth_set(self):
        """
        Permet de limier la bande passante.
        """
        with Printer("Limit bandwidth update...") as p:
            self.limit_bandwidth_canva.delete("all")
            self.limit_bandwidth_canva.create_image(8, 8, image=icons.ok())
            limit_bandwidth = bool(self.limit_bandwidth_var.get())
            self.settings["cluster_work"]["limit_bandwidth"] = limit_bandwidth
            self.schedules_verification_button.configure(state="normal" if limit_bandwidth else "disable")
            self.calibration_bandwidth_button.configure(state="normal" if limit_bandwidth else "disable")

    def schedules_bandwidth_set(self):
        """
        Alias vers raisin.application.hmi.schedules.get_schedules().
        Avec une selection binaire.
        """
        def converter(chaine):
            if chaine == "True" or chaine == "1":
                return True
            elif chaine == "False" or chaine == "0":
                return False
            raise ValueError(
                "'True', '1', 'False' ou '0' est attendu, pas %s." \
                % repr(chaine))

        with Printer("Schedules bandwidth update...") as p:
            self.schedules_bandwidth_canva.delete("all")
            self.schedules_bandwidth_canva.create_image(8, 8, image=icons.refresh())
            import raisin.application.hmi.schedules as schedules
            try:
                self.settings["cluster_work"]["schedules_bandwidth"] = schedules.get_schedules(
                    self.settings["cluster_work"]["schedules_bandwidth"],
                    ylabel="limitation (y/n)",
                    converter=converter,
                    existing_window=self.window)
            except KeyboardInterrupt as e:
                self.schedules_bandwidth_canva.delete("all")
                self.schedules_bandwidth_canva.create_image(8, 8, image=icons.error())
                raise e from e
            self.schedules_bandwidth_canva.delete("all")
            self.schedules_bandwidth_canva.create_image(8, 8, image=icons.ok())

    def maximum_bandwidth_set(self):
        """
        Aide l'utilisateur a choisir la bonne bande passante.
        met a jour les debits de seuil a partir desquels les effets
        de la bande passante commencent a se faire sentir.
        """
        with Printer("Maximum bandwidth update...") as p:
            self.maximum_bandwidth_canva.delete("all")
            self.maximum_bandwidth_canva.create_image(8, 8, image=icons.refresh())
            downflow, rising_flow = self._bandwidth_change()
            if not checks.bandwidth_verification(downflow, rising_flow):
                p.show("Il y a un pepin pour la calibration des debits critiques.")
                self.maximum_bandwidth_canva.delete("all")
                self.maximum_bandwidth_canva.create_image(8, 8, image=icons.error())
            else:
                self.settings["cluster_work"]["downflow"] = downflow
                self.settings["cluster_work"]["rising_flow"] = rising_flow
                self.maximum_bandwidth_canva.delete("all")
                self.maximum_bandwidth_canva.create_image(8, 8, image=icons.ok())

    def _bandwidth_change(self):
        """
        interagit graphiquement avec l'utilisateur afin
        de recuperer les debits critique montant et descandant
        retourne les nouveaux debits (descendant, montant)
        """
        def quit(fen):
            """
            detruit la fenetre
            """
            fen.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if "window" in self.__dict__:                                           # on applique ou non la methode destroy
                fen.quit()  

        def verification(var):
            """
            s'assure que la variable contiene bien
            un nombre entre 0 et 125 avec 1 decimal au plus
            """
            content = var.get()
            try:
                value = float(content)
            except ValueError:
                value = 0
            value = round(min(125, max(0, value)), 1)
            if round(value) == value:
                var.set(str(round(value)))
            else:
                var.set(value)

        def down_test(dispo_down):
            """
            fait un test sur le debit descendant et affiche le resulat
            dans la variable 'dispo_down'
            """
            raise NotImplementedError("Pas de tests disponible pour le debit descendant.")

        def up_test(dispo_up):
            """
            fait un test sur le debit montant et affiche le resulat
            dans la variable 'dispo_up'
            """
            raise NotImplementedError("Pas de tests disponible pour le debit montant")

        # initialisation de la fenetre
        if "window" in self.__dict__:                                               # si il y a deja une fenetre ouverte
            window = tkinter.Toplevel(self.window)                                  # on est oblige d'utiliser un toplevel sinon ca plante
            window.grab_set()                                                       # on fige la fenetre parente
            window.protocol("WM_DELETE_WINDOW", lambda: (window.destroy(), window.quit()))# il se trouve que ca semble fonctionner comme ca...
        else:                                                                       # dans le cas ou aucune instance tkinter n'existe
            window = tkinter.Tk()                                                   # et bien on en cre une tout simplement
            self.get_icons()

        # configuration de la fenetre
        window.title("Calibration bandwidth")
        window.configure(background=JAUNE)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=31)
        window.columnconfigure(2, weight=1)
        for i in range(5):
            window.rowconfigure(i, weight=1)
        window.focus_force()
        window.bind("<Escape>", lambda event: quit(window))

        # initialisation des variables
        downflow_var = tkinter.StringVar()                                          # debit descendant maximum
        downflow_var.set(str(self.settings["cluster_work"]["downflow"]))
        rising_flow_var = tkinter.StringVar()                                       # debit ascendant maximum
        rising_flow_var.set(str(self.settings["cluster_work"]["rising_flow"]))
        dispo_down = tkinter.StringVar()                                            # phrase qui indique le resultat du test du debit descendant
        dispo_down.set("Débit descendant disponible inconu")
        dispo_up = tkinter.StringVar()                                              # phrase qui indique le resultat du test du debit montant
        dispo_up.set("Débit montant disponible inconu")

        # remplissage de la fenetre
        theme(tkinter.Label(window, textvariable=dispo_down)).grid(row=0, column=0, sticky="w")
        theme(tkinter.Button(window,
            text="Lancer le test",
            command=lambda: down_test(dispo_down))).grid(row=0, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info Debit",
                "Ce boutton lance un test de débit qui vous permet de vous faire une idée des ressource dons vous diposez.")
            )).grid(row=0, column=2)
        theme(tkinter.Label(window, text="Débit descendant admissible (Mio/s):")).grid(row=1, column=0, sticky="w")
        down_box = theme(tkinter.Spinbox(window,
            textvariable=downflow_var,
            from_=0,
            to=125,
            increment=0.1))
        down_box.bind("<Return>", lambda event: verification(downflow_var))
        down_box.bind("<KeyRelease>", lambda event: verification(downflow_var))
        down_box.grid(row=1, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info Debit",
                "La valeur entree ici permet de restreindre le debit descendant maximum absulu par cette valeur.\n"
                "Dans les moments ou le debit est regulé (configurer les horaires dans la fenetre parente), toute les "
                "activitees concernées par le partage des ressources 'cluster work' verrons leur debit internet asservi "
                "par cette valeur.")
            )).grid(row=1, column=2)
        theme(tkinter.Label(window, textvariable=dispo_up)).grid(row=2, column=0, sticky="w")
        theme(tkinter.Button(window,
            text="Lancer le test",
            command=lambda: up_test(dispo_up))).grid(row=2, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info Debit",
                "Ce boutton lance un test de débit qui vous permet de vous faire une idée des ressource dons vous diposez.")
            )).grid(row=2, column=2)
        theme(tkinter.Label(window, text="Débit montant admissible (Mio/s):")).grid(row=3, column=0, sticky="w")
        up_box = theme(tkinter.Spinbox(window,
            textvariable=rising_flow_var,
            from_=0,
            to=125,
            increment=0.1))
        up_box.bind("<Return>", lambda event: verification(rising_flow_var))
        up_box.bind("<KeyRelease>", lambda event: verification(rising_flow_var))
        up_box.grid(row=3, column=1, sticky="ew")
        theme(tkinter.Button(window,
            image=icons.info(),
            command=lambda: tkinter.messagebox.showinfo(
                "Info Debit",
                "La valeur entree ici permet de restreindre le debit montant maximum absulu par cette valeur.\n"
                "Dans les moments ou le debit est regulé (configurer les horaires dans la fenetre parente), toute les "
                "activitees concernées par le partage des ressources 'cluster work' verrons leur debit internet asservi "
                "par cette valeur.")
            )).grid(row=3, column=2)
        theme(tkinter.Button(window, text="Valider", command=lambda: quit(window))).grid(row=4, column=0, columnspan=3)

        window.mainloop()

        return float(downflow_var.get()), float(rising_flow_var.get())

    def recording_directory_set(self):
        """
        Deplace les repertoires ou sont enregistres les resultats.
        """
        with Printer("Recording directory update...") as p:
            self.recording_directory_canva.delete("all")
            self.recording_directory_canva.create_image(8, 8, image=icons.refresh())
            import tkinter.filedialog
            recording_directory = tkinter.filedialog.askdirectory(
                parent=self.window,
                title="Repertoire d'enregistrement",
                initialdir=self.settings["cluster_work"]["recording_directory"])
            if not checks.recording_directory_verification(recording_directory):
                p.show("Le repertoire \"%s\" n'est pas un repertoire "
                    "d'enregistrement valide." % recording_directory)
                self.recording_directory_canva.delete("all")
                self.recording_directory_canva.create_image(8, 8, image=icons.error())
                raise ValueError("Ca capote là! Aller on va rien changer et tous va bien se passer!")
            with Printer("Deplacement des elements en cours..."):
                src = os.path.join(self.settings["cluster_work"]["recording_directory"], "results")
                dst = os.path.join(recording_directory, "results")
                if os.path.isdir(src):
                    shutil.move(src, dst)
                else:
                    os.mkdir(dst)
                self.settings["cluster_work"]["recording_directory"] = recording_directory
                self.recording_directory_var.set(recording_directory)
                self.recording_directory_canva.delete("all")
                self.recording_directory_canva.create_image(8, 8, image=icons.ok())

    def free_size_set(self):
        """
        Change la quantite d'espace disponible a maintenir.
        """
        class Verif:
            def __init__(self, path):
                self.path = path
            def __call__(self, free_size):
                return checks.free_size_verification(free_size, self.path)
                
        with Printer("Free size update...") as p:
            self.free_size_canva.delete("all")
            self.free_size_canva.create_image(8, 8, image=icons.refresh())
            question = "Quel espace doit etre libre (Mio) ?"
            default = str(self.settings["cluster_work"]["free_size"])
            try:
                self.settings["cluster_work"]["free_size"] = int(dialog.question_reponse(
                    question,
                    default=default,
                    validatecommand=Verif(self.settings["cluster_work"]["recording_directory"]),
                    existing_window=self.window))
            except KeyboardInterrupt as e:
                self.free_size_canva.delete("all")
                self.free_size_canva.create_image(8, 8, image=icons.error())
                raise e from e
            else:
                self.free_size_var.set(str(self.settings["cluster_work"]["free_size"]) + " (Mio)")
                self.free_size_canva.delete("all")
                self.free_size_canva.create_image(8, 8, image=icons.ok())

    def restrict_access_set(self):
        """
        Applique le changement d'etat du boutton.
        """
        with Printer("Restrict access update...") as p:
            self.restrict_access_canva.delete("all")
            self.restrict_access_canva.create_image(8, 8, image=icons.ok())
            self.settings["cluster_work"]["restrict_access"] = bool(self.restrict_access_var.get())

    def port_set(self):
        """
        Met a jour le port si possible.
        """
        with Printer("Port update...") as p:
            port = self.port_var.get()
            if str(self.settings["server"]["port"]) != port:
                if not checks.port_verification(port):
                    p.show("Il y a un bins dans le port.")
                    self.port_canva.delete("all")
                    self.port_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["server"]["port"] = int(port)
                    self.port_canva.delete("all")
                    self.port_canva.create_image(8, 8, image=icons.ok())
            if str(self.settings.get_original("server", "port")) == port:
                self.port_canva.delete("all")

    def listen_set(self):
        """
        Met a jour le nombre de connections simultanees
        maximum acceptable par le serveur.
        """
        with Printer("Listen update...") as p :
            listen = self.listen_var.get()
            if str(self.settings["server"]["listen"]) != listen:
                if not checks.listen_verification(listen):
                    p.show("Le nombre de connection n'est pas valide.")
                    self.listen_canva.delete("all")
                    self.listen_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["server"]["listen"] = int(listen)
                    self.listen_canva.delete("all")
                    self.listen_canva.create_image(8, 8, image=icons.ok())
            if str(self.settings.get_original("server", "listen")) == listen:
                self.listen_canva.delete("all")

    def network_name_set(self):
        """
        Met a jour le nom de serveur si il est correcte.
        """
        with Printer("Netwok name update...") as p:
            network_name = self.network_name_var.get()
            if self.settings["server"]["network_name"] != network_name:
                if not checks.network_name_verification(network_name):
                    p.show("Le nom de reseau n'est pas correcte")
                    self.network_name_canva.delete("all")
                    self.network_name_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["server"]["network_name"] = network_name
                    self.network_name_canva.delete("all")
                    self.network_name_canva.create_image(8, 8, image=icons.ok())
            if self.settings.get_original("server", "network_name") == network_name:
                self.network_name_canva.delete("all")

    def dns_ip_set(self, version):
        """
        S'assure que le nom de de domaine donne poine bien vers ici.
        """
        assert version == 6 or version == 4, \
            "La version de protocole ip doit etre 6 ou 4, pas %s." % version # le %s c'est pas un erreur, au cas ou version ne soit pas int
        with Printer("DNS update...") as p:
            dns = self.dns_ipv6_var.get() if version == 6 else self.dns_ipv4_var.get()
            if self.settings["server"]["dns_ipv%d" % version] != (dns if dns else None):
                if (not dns) or checks.dns_ip_verification(dns, version):
                    self.settings["server"]["dns_ipv%d" % version] = dns if dns else None
                    exec("self.dns_ipv%d_canva.delete('all')" % version)
                    exec("self.dns_ipv%d_canva.create_image(8, 8, image=icons.ok())" % version)
                else:
                    p.show("Le nom de domaine donner n'est pas tout a fait bon.")
                    exec("self.dns_ipv%d_canva.delete('all')" % version)
                    exec("self.dns_ipv%d_canva.create_image(8, 8, image=icons.error())" % version)
            if self.settings.get_original("server", "dns_ipv%d" % version) == (dns if dns else None):
                exec("self.dns_ipv%d_canva.delete('all')" % version)
                    
    def port_forwarding_set(self):
        """
        Met a jour le port de redirection.
        """
        with Printer("Port forwarding update...") as p:
            port = self.port_forwarding_var.get()
            if str(self.settings["server"]["port_forwarding"]) != (port if port else "None"):
                if not checks.port_forwarding_verification(port):
                    p.show("La redirection de port actuelle ne fonctionne pas.")
                    self.port_forwarding_canva.delete("all")
                    self.port_forwarding_canva.create_image(8, 8, image=icons.error())
                else:
                    self.settings["server"]["port_forwarding"] = int(port) if port else None
                    self.port_forwarding_canva.delete("all")
                    self.port_forwarding_canva.create_image(8, 8, image=icons.ok())
            if str(self.settings.get_original("server", "port_forwarding")) == (port if port else "None"):
                self.port_forwarding_canva.delete("all")

    def accept_new_client_set(self):
        """
        Met a jour la variable pour accepeter les nouveaux clients ou pas.
        """
        with Printer("Accept new client update...") as p:
            self.accept_new_client_canva.delete("all")
            self.accept_new_client_canva.create_image(8, 8, image=icons.ok())
            self.settings["server"]["accept_new_client"] = not self.accept_new_client_var.get() # not car la question est tournee dans l'autre sens

    def force_authentication_set(self):
        """
        Met a jour la variable qui permet de forcer ou non l'authentification.
        """
        with Printer("Accept new client update...") as p:
            self.force_authentication_canva.delete("all")
            self.force_authentication_canva.create_image(8, 8, image=icons.ok())
            self.settings["server"]["force_authentication"] = bool(self.force_authentication_var.get())

    def access_token_set(self):
        """
        Enregistre le nouvel acces token si il est valide.
        """
        with Printer("Access token update...") as p:
            access_token = self.access_token_var.get()
            if self.settings["server"]["access_token"] != (access_token if access_token else None):
                if (not access_token) or checks.access_token_verification(access_token):
                    self.settings["server"]["access_token"] = access_token if access_token else None
                    self.access_token_canva.delete("all")
                    self.access_token_canva.create_image(8, 8, image=icons.ok())
                else:
                    p.show("L'access token specifier n'est pas correcte.")
                    self.access_token_canva.delete("all")
                    self.access_token_canva.create_image(8, 8, image=icons.error())
            if self.settings.get_original("server", "access_token") == (access_token if access_token else None):
                self.access_token_canva.delete("all")

    def put_refresh(self, event, canvas):
        """
        Met dans canvas l'icon refrech si
        event est une touche imprimable.
        """
        if event.keysym not in ("Tab", "Return", "Escape"):
            canvas.delete("all")
            canvas.create_image(8, 8, image=icons.refresh())

def change_padlock(*, existing_window=None):
    """
    Change l'antivol de raisin'.
    """
    with Printer("Change the raisin padlock parameters..."):
        import raisin.application.hmi.padlock as padlock
        break_time, cipher, notify_by_email, paths = padlock.get_new_padlock(existing_window=existing_window)
        settings.settings["account"]["padlock"]["break_time"] = break_time
        settings.settings["account"]["padlock"]["cipher"] = cipher
        settings.settings["account"]["padlock"]["notify_by_email"] = notify_by_email
        settings.settings["account"]["padlock"]["paths"] = paths
        settings.settings.flush()

if __name__ == "__main__":
    Config()
