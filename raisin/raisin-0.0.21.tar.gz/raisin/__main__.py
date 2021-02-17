#!/usr/bin/env python3
#PYTHON_ARGCOMPLETE_OK

"""
|=================================|
| Permet d'executer des fonctions |
| en ligne de commandes.          |
|=================================|

1) Installer/Desinstaller raisin ou un autre module.
    -Installer raisin:
        $ python3 -m raisin install
    -Desinstaller raisin:
        $ python3 -m raisin uninstall
    -Reinstaller raisin:
        $ python3 -m raisin reinstall
    -Metre a jour raisin:
        $ python3 -m raisin upgrade
        -Metre a jour sur la version instable:
            $ python3 -m raisin upgrade --unstable
        -Metre a jour sur la version stable (par defaut)
            $ python3 -m raisin upgrade --stable
2) Configurer raisin.
    -Configuration generale:
        $ python3 -m raisin configure
    -Changer le mot de passe:
        $ python3 -m raisin psw
        $ python3 -m raisin configure psw
    -Configurer l'antivol:
        $ python3 -m raisin padlock
        $ python3 -m raisin configure padlock
3) Lancer l'application:
    -Demarrer le serveur:
        $ python3 -m raisin start --server
    -Lancer les mises a jours automatiques:
        $ python3 -m raisin start --upgrade
    -Lancer l'antivole:
        $ python3 -m raisin start --padlock
4) Gerer les clients:
    -Accepter un client:
        $ python3 -m raisin client --accept 'mac_addr'
    -Interdire la connection a un client:
        $ python3 -m raisin client --exile 'mac_addr'
    -Supprimer un client de tous les fichiers:
        $ python3 -m raisin client --delete 'mac_addr'
"""

import argparse
import os
import sys


def parse_arguments():
    """
    Fait le parsing des arguments.
    """
    parser = argparse.ArgumentParser(description="Simple API pour raisin.")
    subparsers = parser.add_subparsers(dest="parser_name")

    # install
    parser_install = subparsers.add_parser("install", help="Installer un module python, possiblement raisin lui-meme.")
    parser_install.add_argument("module", type=str, nargs="?", default="raisin", help="Nom du module")
    parser_install.add_argument("-U", "--upgrade", action="store_true", default=False, help="Fait la mise a jour.")

    # uninstall
    parser_uninstall = subparsers.add_parser("uninstall", help="Desinstaller un module python, possiblement raisin lui-meme.")
    parser_uninstall.add_argument("module", type=str, nargs="?", default="raisin", help="Nom du module.")

    # reinstall
    parser_reinstall = subparsers.add_parser("reinstall", help="Reinstaller l'application de raisin.")

    # upgrade
    parser_upgrade = subparsers.add_parser("upgrade", help="Met a jour raisin depuis le depos git.")
    parser_upgrade.add_argument("-U", "--unstable", action="store_true", default=False, help="Mise a jour sur la version instable.")
    parser_upgrade.add_argument("--stable", action="store_true", default=False, help="Mise a jour sur la version stable.")

    # configuration
    parser_configure = subparsers.add_parser("configure", help="Personnaliser l'installation de raisin.")
    parser_configure.add_argument("category", type=str, nargs="?", choices=["all", "psw", "padlock"], default="all", help="Specifiez l'element a configurer.")

    # psw
    parser_psw = subparsers.add_parser("psw", help="Ajouter/Changer/Supprimer le mot de passe de raisin.")

    # padlock
    parser_padlock = subparsers.add_parser("padlock", help="Ajouter/Changer/Desactiver l'antivol de raisin.")

    # start
    parser_start = subparsers.add_parser("start", help="Executer l'application de raisin.")
    parser_start.add_argument("-S", "--serv", "--server", action="store_true", default=False, help="Demmare le serveur raisin pour partager les resources.")
    parser_start.add_argument("-U", "--upgrade", action="store_true", default=False, help="Fait la mise a jour si l'option est cochee.")
    parser_start.add_argument("-P", "--padlock", action="store_true", default=False, help="Demmare l'antivol en tache de fond.")

    # client
    parser_client = subparsers.add_parser("client", help="Gestion des client qui se connectent au serveur.")
    parser_client.add_argument("-A", "--accept", action="store_true", default=False, help="Met un client en liste blanche.")
    parser_client.add_argument("-E", "--exile", action="store_true", default=False, help="Empeche a un client de se connecter.")
    parser_client.add_argument("-D", "--delete", action="store_true", default=False, help="Suprime un client des fichiers.")
    parser_client.add_argument("mac", type=str, nargs="?", help="L'adresse mac du client a considerer.")

    return parser

def catch_error(fonc):
    """
    |=====================================|
    | Decorateur qui transforme la sortie |
    | python par une sortie bash.         |
    |=====================================|

    * Si la fonction leve une exception,
    retourne un entier non nul qui correspond
    au code d'erreur.
    * Si la fonction ne leve pas d'exeption,
    la fonction decoree retourne 0.
    * Ne capture que les erreurs derivees
    de Exception, pas de BaseException.
    * Si la fonction retourne autre chose
    que None, la sortie est interceptee
    est est affichee dans le stdout.

    entree
    ------
    :param fonc: La fonction a decorer.
    :type font: callable

    sortie
    ------
    :return: Fonction decoree.
    :rtype: callable
    """
    def fonc_dec(*args, **kwargs):
        try:
            res = fonc(*args, **kwargs)
        except Exception as e:
            sys.stderr.write("%s: %s\n" % (type(e).__name__, e))
            return 1
        else:
            if res != None:
                print(res)
            return 0

    return fonc_dec


def _install_raisin():
    import raisin.application.install as install
    install.main()

def _uninstall_raisin():
    import raisin.application.uninstall as uninstall
    uninstall.main()

def _upgrade_raisin(unstable):
    import raisin.application.upgrade as upgrade
    upgrade.main("unstable" if unstable else "stable")

def _configure_raisin():
    import raisin.application.configuration as configuration
    configuration.Config()

def _psw_raisin():
    import raisin.security as security
    security.change_psw()

def _padlock_raisin():
    import raisin.application.configuration as configuration
    configuration.change_padlock()

def _start_server():
    import raisin.communication.tcp_server as tcp_server
    s = tcp_server.Server()
    s.start()

def _start_upgrade():
    import raisin.application.upgrade as upgrade
    upgrade.automatic_update()

def _start_padlock():
    import raisin.application.scripts.padlock as padlock
    padlock.main()

def _client_accept(mac):
    import raisin.communication.tcp_server as tcp_server
    tcp_server.client_accept(mac)

def _client_exile(mac):
    import raisin.communication.tcp_server as tcp_server
    tcp_server.client_exile(mac)

def _client_delete(mac):
    import raisin.communication.tcp_server as tcp_server
    tcp_server.client_remove(mac)


@catch_error
def main(args_brut=[]):
    """
    |===========================|
    | Interprete les commandes. |
    |===========================|

    * Permet de pouvoir utiliser 'raisin' en ligne
    de commande bash.

    entree
    ------
    :param args_brut: La liste des arguments passes.
    :types args_brut: list

    sortie
    ------
    :return: La sortie des fonctions appelees.
    """
    # Parsing des arguments.
    parser = parse_arguments()
    if args_brut:
        args = parser.parse_args(args_brut)
    else:
        args = parser.parse_args()
    
    if args.parser_name == "install":
        if args.module == "raisin":
            if args.upgrade:
                return _upgrade_raisin(args.unstable)
            else:
                return _install_raisin()
        else:
            raise NotImplementedError("Impossible d'installer un aute module que raisin.")
    elif args.parser_name == "uninstall":
        if args.module == "raisin":
            return _uninstall_raisin()
        else:
            raise NotImplementedError("Je ne suis pas capable de desinstaller un module autre que raisin.")
    elif args.parser_name == "reinstall":
        return not ((not _uninstall_raisin()) and (not _install_raisin()))
    elif args.parser_name == "upgrade":
        return _upgrade_raisin(args.unstable)
    elif args.parser_name == "configure":       # si il faut configurer raisin
        if args.category == "all":
            return _configure_raisin()
        elif args.category == "psw":
            return _psw_raisin()
        elif args.category == "padlock":
            return _padlock_raisin()
    elif args.parser_name == "psw":
        return _psw_raisin()
    elif args.parser_name == "padlock":
        return _padlock_raisin()
    elif args.parser_name == "start":           # si il faut lancer des scripts specifiques
        apps = [func for func, arg
            in [(_start_server, args.serv),
                (_start_upgrade, args.upgrade),
                (_start_padlock, args.padlock)]
            if arg]
        if len(apps) == 0:
            raise NotImplementedError("Il faut specifier quoi lancer.")
        elif len(apps) == 1:
            return apps[0]()
        else:
            import multiprocessing
            threads = [multiprocessing.Process(target=app) for app in apps]
            [t.start() for t in threads]
            [t.join() for t in threads]
            return None
    elif args.parser_name == "client":
        if args.delete:
            return _client_delete(args.mac)
        if args.accept:
            return _client_accept(args.mac)
        if args.exile:
            return _client_exile(args.mac)

    elif args.parser_name in ("cipher", "uncipher"):
        raise NotImplementedError("Impossible de chiffrer/dechifrer un fichier.")
    else:
        raise SyntaxError("Argument invalide.\nPour plus d'informations, tapez '%s -m raisin --help'\n" % sys.executable)

if __name__ == "__main__":
    main()
