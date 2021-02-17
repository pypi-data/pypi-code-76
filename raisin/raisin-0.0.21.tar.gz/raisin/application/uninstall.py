#!/usr/bin/env python3

"""
|============================|
| Desinstalle l'application. |
|============================|

Ce fichier est a la fois un module est un script.

1) Retire raisin des applications au demarrage.
2) Supprime les repertoires crees par raisin.
3) Supprime les raccourcis qui pointent vers raisin.
"""

import os
import re
import shutil

import raisin.tools as tools # On ne fait pas d'import relatif
import raisin.application.settings as settings # de facon a ce qu'on
import raisin.application.hmi.dialog as dialog # puisse l'excecuter directement.


def uninstall_startup(home, *, service="all"):
    """
    |====================================|
    | Supprime le demarrage automatique. |
    |====================================|

    Desamorce si possible la partie de raisin
    qui se lance toute seule.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par la desinstallation.
        Ou la valeur speciale: 'all_users'
        si il faut desinstaller le service pour tous le monde.
    :type home: str
    :param service: Le type de service a desinstaller:
        'server' -> Desinstalle le serveur au demarrage.
        'upgrade' -> Desactive les mises a jour automatiquement.
        'padlock' -> Supprime l'antivol au demarrage
        'all' -> Desinstalle tous les services.
    :type service: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)
    assert isinstance(service, str), \
        "'service' has to be of type str, not %s." \
        % type(service).__name__
    assert service in {"all", "server", "upgrade", "padlock"}, \
        "'service' ne peut pas etre %s." % repr(service)

    # Si il faut desinstaller tous les services, on ne les prend pas tous d'un coup.
    if service == "all":
        uninstall_startup(home, service="server")
        uninstall_startup(home, service="upgrade")
        uninstall_startup(home, service="padlock")
        return

    # Si il faut desinstaller pour tous le monde, on le fait au fur a mesure.
    if home == "all_users":
        racine = "C:\\Users" if os.name == "nt" else "/home"
        for user in (user for user in os.listdir(racine) if user != "root"):
            uninstall_startup(os.path.join(racine, user), service=service)

    with tools.Printer(
            "Removing raisin {} to apps at startup for {}...".format(service,
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
        
        if os.name == "posix":
            if home == "all_users":
                if os.system(f"systemctl stop {service}_raisin"):
                    p.show(f"Failed to stop the '{service}_raisin' service.")
                else:
                    p.show(f"The '{service}_raisin' service is stoped.")
                if os.system(f"systemctl disable {service}_raisin"):
                    p.show(f"Failed to disable the '{service}_raisin' service.")
                else:
                    p.show(f"The '{service}_raisin' service is disabled.")
                path = f"/lib/systemd/system/{service}_raisin.service"
                if os.path.exists(path):
                    os.remove(path)
                    p.show("Removed %s." % repr(path))
                else:
                    p.show("Failed removed %s." % repr(path))
            else:
                header = ""
                if tools.identity["has_admin"]:
                    # export XDG_RUNTIME_DIR="/run/user/$UID"
                    # export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"
                    user = os.path.basename(home)
                    header = f"sudo -u {user} XDG_RUNTIME_DIR=/run/user/$(id -u {user}) "
                    if os.system("sudo loginctl enable-linger %s" % user):
                        raise SystemError("Impossible d'executer: "
                            "'sudo loginctl enable-linger %s'" % user)

                if os.system(f"{header}systemctl --user stop {service}_raisin"):
                    p.show(f"Failed to stop the '{service}_raisin' service.")
                else:
                    p.show(f"The '{service}_raisin' service is stoped.")
                if os.system(f"{header}systemctl --user disable {service}_raisin"):
                    p.show(f"Failed to disable the '{service}_raisin' service.")
                else:
                    p.show(f"The '{service}_raisin' service is disabled.")
                path = os.path.join(home, f".config/systemd/user/{service}_raisin.service")
                if os.path.exists(path):
                    os.remove(path)
                    p.show("Removed %s." % repr(path))
                else:
                    p.show("Failed to removed %s." % repr(path))
        
        elif os.name == "nt":
            if home == "all_users":
                if os.path.exists("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\"
                        f"Programs\\Startup\\{service}_raisin.pyw"):
                    os.remove("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\"
                        f"Programs\\Startup\\{service}_raisin.pyw")
                    p.show(f"The '{service}_raisin.pyw' file is deleted.")
                else:
                    p.show(f"Failed to delete the '{service}_raisin.pyw' file.")
            else:
                if os.path.exists(os.path.join(home, "AppData\\Roaming\\Microsoft\\"
                        f"Windows\\Start Menu\\Programs\\Startup\\{service}_raisin.pyw")):
                    os.remove(os.path.join(home, "AppData\\Roaming\\Microsoft\\" \
                        f"Windows\\Start Menu\\Programs\\Startup\\{service}_raisin.pyw"))
                    p.show(f"The '{service}_raisin.pyw' file is deleted.")
                else:
                    p.show(f"Failed to delete the '{service}_raisin.pyw' file.")

def uninstall_settings(home):
    """
    |================================|
    | Mange les crottes de 'raisin'. |
    |================================|

    * Supprime le repertoire '.raisin'.
    * Supprime aussi le repertoire d'enregistrement des resultats
        si il existe.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par le desamorcage.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    with tools.Printer(
            "Uninstall settings for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
        
        # Suppression rep enregistrement.
        real_home = os.path.expanduser("~") if home == "all_users" else home
        recording_directory = settings.Settings(home=real_home)["cluster_work"]["recording_directory"]
        if os.path.exists(recording_directory):
            shutil.rmtree(recording_directory)
            p.show("Removed %s." % repr(recording_directory))
        
        # Suppression rep de base.
        raisin_path = os.path.join(home, ".raisin")
        if os.path.exists(raisin_path):
            shutil.rmtree(raisin_path)
            p.show("Removed %s." % repr(raisin_path))
        else:
            p.show("Rep not found %s." % repr(raisin_path))

def uninstall_shortcut(home):
    """
    |=====================|
    | Supprime les alias. |
    |=====================|
    
    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par le desamorcage.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    with tools.Printer(
            "Uninstall shortcut for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
       
        real_home = os.path.expanduser("~") if home == "all_users" else home
        
        if os.name == "posix":
            bashrc = os.path.join(real_home, ".bashrc")
            with open(bashrc, "r", encoding="utf-8") as f:
                lines = [l for l in f if not re.search(r"alias raisin='.+ -m raisin'", l)]
                while lines and lines[-1] == "\n":
                    del lines[-1]
            with open(bashrc, "w", encoding="utf-8") as f:
                f.write("".join(lines))
            p.show("Removed raisin from %s." % repr(bashrc))
            # os.system("source ~/.bashrc") # Pour endre effectif.

        elif os.name == "nt":
            profile = os.path.join(real_home, "Documents", "profile.ps1")
            if os.path.exists(profile):
                with open(profile, "r", encoding="utf-8") as f:
                    lines = [l for l in f if not re.search(r"Set-Alias raisin '.+ -m raisin'", l)]
                    while lines and lines[-1] == "\n":
                        del lines[-1]
                if lines:
                    with open(profile, "w", encoding="utf-8") as f:
                        f.write("".join(lines))
                    p.show("Removed raisin from the 'profile.ps1' file")
                else:
                    os.remove(profile)
                    p.show("Removed %s." % repr(profile))
            else:
                p.show("File not found %s." % repr(profile))

def _list_home():
    """
    |===================================|
    | Liste les utilisateurs concernes. |
    |===================================|

    * Cede les repertoires personels de
    tous les utilisateurs qui doivent
    beneficier de la desinstallation de raisin.
    * Si cette fonction est lancee avec les
    droits administrateurs et que l'utilisateur
    veut faire que plus personne n'ai raisin,
    retourne la valeur speciale: 'all_users'.

    sortie
    ------
    :return: Le chemin du repertoire personel
        de chaque utilisateur concerne. Ou
        la valeur speciale: 'all_users'.
    :rtype: str
    """
    if tools.identity["has_admin"]:
        if 0 == dialog.question_choix_exclusif(
                question="How do you want to uninstall 'raisin'?",
                choix=["Do you want uninstall 'raisin' for each user?",
                       "Do you want uninstall 'raisin' for 'root'?"]):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
        else:
            yield "all_users"
    else:
        yield os.path.expanduser("~")

def main():
    """
    Desinstalle entierement l'application raisin.
    """
    with tools.Printer("Uninstall raisin..."):
        for home in _list_home():
            uninstall_shortcut(home)
            uninstall_settings(home)
            uninstall_startup(home)

if __name__ == "__main__":
    main()
