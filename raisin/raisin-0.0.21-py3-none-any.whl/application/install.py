#!/usr/bin/env python3

"""
|=========================|
| Installe l'application. |
|=========================|

Ce fichier est a la fois un module est un script.

1) Gives write rights to the 'grape' module folder so as to allow updates.
2) Append alias/shortcut for 'raisin' command line.
3) Creation and recording of 'rasin' parameters.
4) Ensures that 'raisin' starts up on its own at the start.
"""

import os
import sys

import raisin.tools as tools # On ne fait pas d'import relatif
import raisin.application.hmi.dialog as dialog # afin de pouvoir le faire
import raisin.application.module as module # fonctionner comme un script.
import raisin.application.uninstall as uninstall
import raisin.application.upgrade as upgrade
import raisin.application.settings as settings


def install_dependencies():
    """
    Recherche les dependances non satisfaites de raisin
    et tente de les installer si l'utilisateur est d'accord.
    """
    # global tkinter, ttk # evite l'erreur: UnboundLocalError: local variable 'tkinter' referenced before assignment

    dependencies = module.get_unmet_dependencies("raisin") # recherches des dependances non satisfaites de raisin
    if dependencies:
        if dialog.question_binaire(
                "'raisin' depend des modules suivants:\n" \
                + " %s\n" % ", ".join(dependencies) \
                + "Voulez-vous les installer?", default=True):
            if not tools.identity["has_admin"]:
                if dialog.question_binaire(
                        "Vous n'avez pas les droits administrateur.\n"
                        "Preferez-vous installer les modules en tant "
                        "qu'administrateur?", default=True):
                    command = '%s -c "\n' % sys.executable
                    command += 'from raisin.application import module\n' \
                            + 'for dep in %s:\n' % repr(dependencies) \
                            + '\tmodule.install(dep)\n' \
                            + '"'
                    if os.name == "nt":
                        sudo = "runas /user:%s\\administrator" \
                                % tools.identity["hostname"]
                    else:
                        sudo = "sudo"
                    sudo_command = sudo + " " + command
                    with tools.Printer(
                        "Install dependencies as administrator...") as p:
                        p.show("$ %s" % repr(sudo_command))
                        os.system(sudo_command)
                    return
                else:
                    message = "Install dependencies without administrator rights..."
            else:
                message = "Install dependencies with administrator rights..."
            with tools.Printer(message):
                for dep in dependencies:
                    module.install(dep)

def install_shortcut(home):
    """
    |============================================|
    | Ajoute des alias qui pointent vers raisin. |
    |============================================|

    Se contente de faire l'alias permanent suivant:
    'python3 -m raisin' devient simplement 'raisin'

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' have to be str, not %s." % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Install shortcut for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))):
        uninstall.uninstall_shortcut(home) # On prend des precautions
        real_home = os.path.expanduser("~") if home == "all_users" else home
        if os.name == "posix":
            config_file = os.path.join(real_home, ".bashrc")
            command = "alias raisin='%s -m raisin'" % sys.executable
            # os.system(". ~/.bashrc") # Pour endre effectif.
        elif os.name == "nt":
            config_file = os.path.join(real_home, "Documents", "profile.ps1")
            command = "Set-Alias raisin '%s -m raisin'" % sys.executable
        
        with open(config_file, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(command)
            f.write("\n")

def install_settings(home, action):
    """
    |==============================|
    | Genere et enregistres les    |
    | parametres de l'utilisateur. |
    |==============================|

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    :param action: Le mode d'installation:
        - 'paranoiac' Pour une securitee maximale,
            au detriment parfois de l'efficacite.
        - 'normal' Pour un bon compromis entre la securite,
            la vie privee et l'efficacite.
        - 'altruistic' Pour maximiser l'efficacite,
            au detriment de la securite et de la vie privee.
        - 'custom' Pose la question a l'utilisateur a chaque etape.
    :type action: str
    """
    assert isinstance(home, str), \
        "'home' have to be str, not %s." % type(home).__name__
    assert isinstance(action, str), \
        "'action' have to be str, not %s." % type(action).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)
    assert action in ("paranoiac", "normal", "altruistic", "custom"), \
            "Les actions ne peuvent que etre 'paranoiac', " \
            + "'normal', 'altruistic' ou 'custom'. Pas '%s'." % action

    with tools.Printer(
            "Install settings for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))):
        home = os.path.expanduser("~") if home == "all_users" else home
        s = settings.Settings(home=home, action=action)
        s.flush()

def install_startup(home, *, service="all"):
    r"""
    |==========================|
    | Fait en sorte que raisin |
    | se lance de lui-meme.    |
    |==========================|

    * Si 'home' vaut "all_users":
        - Fait en sorte que 'raisin' se
        lance une seule fois au demarrage de l'ordinateur.
        - Raisin se lance pour 'root'.
    * Si 'home' vaut "/home/<username>":
        - Fait en sorte qu'une instance de raisin
        se lance des que le user <username>
        se connecte a sa session.
    * Si 'home' vaut "C:\\Users\\<username>":
        - Fait comme juste au dessus mais ne
        restreind pas les droits de l'application
        car sur windows c'est complique.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    :param service: Le type de service a installer:
        'server' -> Installe le serveur au demarrage.
        'upgrade' -> Applique les mises a jour automatiquement.
        'padlock' -> Lance l'antivol au demarrage
        'all' -> Installe tous les services.
    :type service: str

    sortie
    ------
    :raises PermissionError: Si les droits ne sont pas suffisants
        pour installer les fichiers la ou il faut.
    :raises SystemError: Si le systeme d'exploitation ne permet
        pas a raisin de se debrouiller tout seul.
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

    if service == "all":
        install_startup(home, service="server")
        install_startup(home, service="upgrade")
        install_startup(home, service="padlock")
        return

    with tools.Printer(
            "Adding raisin {} to apps at startup for {}...".format(service,
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:

        # Recherche des dossiers ou il faut metre les services.
        p.show("Finding folders configuration.")
        racine = "C:\\Users" if os.name == "nt" else "/home"
        if os.name == "posix":
            if not os.path.exists("/lib/systemd/system/"):
                raise SystemError("It doesn't appear that "
                    "the service manager is 'systemd'.")
            root_path = f"/lib/systemd/system/{service}_raisin.service"
            user_path = os.path.join(home,
                f".config/systemd/user/{service}_raisin.service")
        elif os.name == "nt":
            root_path = ("C:\\ProgramData\\Microsoft\\"
                f"Windows\\Start Menu\\Programs\\Startup\\{service}_raisin.pyw")
            user_path = os.path.join(home,
                "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\"
                f"Programs\\Startup\\{service}_raisin.pyw")
        else:
            raise SystemError("I don't know the standard %s." % repr(os.name),
                "I can to succeed with 'posix' or 'nt'.")

        # Suppresion des daemons a reinstaller.
        p.show("Checking consistency.")
        uninstall.uninstall_startup(home, service=service)

        # Preparation des dossiers.
        if os.name == "posix":
            if home != "all_users" and not os.path.exists(os.path.join(
                    home, ".config/systemd/user/")):
                os.makedirs(os.path.join(home, ".config/systemd/user/"))

        # Installation des fichiers.
        instructions = ["start", "--{}".format(service)]
        if os.name == "posix":
            command = "%s -m raisin %s" % (sys.executable, " ".join(instructions))
            if home == "all_users":
                p.show("Writing %s." % root_path)
                with open(root_path, "w") as f:
                    # Partie Unit.
                    f.write("[Unit]\n")
                    f.write("Description=The raisin %s service.\n" % service)
                    f.write("After=network-online.target\n")
                    f.write("\n")

                    # Partie Service.
                    f.write("[Service]\n")
                    f.write("Type=simple\n")
                    f.write("ExecStart=%s\n" % command)
                    f.write("Restart=on-abort\n")
                    f.write("\n")

                    # Partie Install.
                    f.write("[Install]\n")
                    f.write("WantedBy=multi-user.target\n")
                
                os.chmod(root_path, 0o644)
                if os.system(f"systemctl enable {service}_raisin"):
                    raise SystemError(f"Impossible d'excecuter: 'systemctl enable {service}_raisin'")
                if os.system(f"systemctl start {service}_raisin"):
                    raise SystemError(f"Impossible d'excecuter: 'systemctl start {service}_raisin'")
            else:
                p.show("Writing %s." % user_path)
                with open(user_path, "w") as f:
                    # Partie Unit.
                    f.write("[Unit]\n")
                    f.write("Description=The raisin %s service.\n" % service)
                    f.write("After=graphical.target\n")
                    f.write("\n")

                    # Partie Service.
                    f.write("[Service]\n")
                    f.write("Type=simple\n")
                    # f.write("User=deluge\n")
                    # f.write("Group=deluge\n")
                    f.write("ExecStart=%s\n" % command)
                    # f.write("Environment=XAUTHORITY=~/.Xauthority\n")
                    f.write("Restart=on-failure\n")
                    f.write("\n")

                    # Partie Install.
                    f.write("[Install]\n")
                    f.write("WantedBy=default.target\n")
                
                header = ""
                if tools.identity["has_admin"]:
                    # export XDG_RUNTIME_DIR="/run/user/$UID"
                    # export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"
                    os.chmod(user_path, 0o644)
                    user = os.path.basename(home)
                    header = f"sudo -u {user} XDG_RUNTIME_DIR=/run/user/$(id -u {user}) "
                    if os.system("sudo loginctl enable-linger %s" % user):
                        raise SystemError("Impossible d'executer: "
                            "'sudo loginctl enable-linger %s'" % user)
                print(user_path)
                if os.system(f"{header}systemctl --user enable {service}_raisin.service"):
                    raise SystemError(f"Impossible d'excecuter: '{header}systemctl --user enable {service}_raisin.service'")
                if os.system(f"{header}systemctl --user start {service}_raisin.service"):
                    raise SystemError(f"Impossible d'excecuter: '{header}systemctl --user start {service}_raisin.service'")
        
        elif os.name == "nt":
            filename = root_path if home == "all_users" else user_path
            p.show("Writing %s." % repr(filename))
            with open(filename, "w") as f:
                f.write("import raisin.__main__\n"
                        "\n"
                        "raisin.__main__.main([%s])\n" % ", ".join(instructions))

def _list_home():
    """
    |===================================|
    | Liste les utilisateurs concernes. |
    |===================================|

    * Cede les repertoires personels de
    tous les utilisateurs qui doivent
    beneficier de l'installation de raisin.
    * Si cette fonction est lancee avec les
    droits administrateurs et que l'utilisateur
    veut faire beneficier tout le monde de raisin,
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
                question="How do you want to install 'raisin'?",
                choix=[("Do you want an instance of 'raisin' start independently for "
                    "each user each time they log in, (so each user can configure "
                    "the behavior of the application as they wish) ?"),
                    ("Do you want a single instance of 'raisin' start a the "
                    "computer boot, (so the root user is the only user "
                    "that can to configure the behavior) ?")]):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
        else:
            yield "all_users"
    else:
        yield os.path.expanduser("~")

def main():
    """
    Installe les elements fondamentaux
    pour le bon fonctionnement de l'application.
    N'agit pas de la même facon selon les droits.
    """
    with tools.Printer("Install raisin...") as p:
        
        # On donne les droits d'ecriture pour les mises a jour
        if tools.identity["has_admin"]:
            try:
                raisin_path = upgrade.find_folder()
            except OSError:
                pass
            else:
                for d, _, fs in os.walk(raisin_path):
                    os.chmod(d, 0o777)
                    for f in fs:
                        os.chmod(os.path.join(d, f), 0o777)

        # install_dependencies()
        actions = ["paranoiac", "normal", "altruistic", "custom"]
        action = actions[
            dialog.question_choix_exclusif(
                "Quel mode d'installation ?",
                ["paranoiac (maximum security)",
                 "normal (compromise between safety and efficiency)",
                 "altruistic (maximum performance)",
                 "custom (request your detailed opinion)"])]
        for home in _list_home():
            install_shortcut(home)
            install_settings(home, action)
            install_startup(home)

if __name__ == "__main__":
    main()
