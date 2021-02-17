#!/usr/bin/env python3

"""
|==================================|
| Met a jour raisin depuis le git. |
|==================================|

Telecharge l'archive depuis le depos 'framagit'.
Prend le derniers commit sur la branche 'stable'
ou 'master' selon ce qui est demande.
Les nouveaux fichiers ecrasents la version
locale exisyante de raisin.
"""


import os
import requests
import shutil
import sys
import tarfile
import time

from dirhash import dirhash # Pour avoir le hash d'un dossier complet.

from ..tools import Printer, temprep, identity


URL_UNSTABLE = "https://framagit.org/robinechuca/raisin/-/archive/master/raisin-master.tar.gz?path=raisin"
URL_STABLE = "https://framagit.org/robinechuca/raisin/-/archive/stable/raisin-stable.tar.gz?path=raisin"


def automatic_update(version="stable"):
    """
    |==============================|
    | En ecoute d'une mise a jour. |
    |==============================|

    Cette fonction ne retourne jamais.
    Elle tente de faire une mise a jour
    toutes les 24 heures.

    entree
    ------
    :param version: "stable" ou "unstable". Permet de choisir
        si la mise a jour est faite a partir d'une version stable
        ou a partir de la version en cours de devellopement.
    :type version: str
    :raises OSError: Si raisin est mal installe.
        Ou dumoins que le dossier d'installation n'est
        pas clair.
    :raises PermissionError: Si les permisions ne sont pas
        suffisantes pour pouvoir ecrire la nouvelle version.
    """
    import raisin.application.settings as settings
    while True:
        if settings.settings["account"]["automatic_update"]:
            main(version)
        else:
            break
        time.sleep(24*3600)

def find_folder():
    """
    Recherche le repertoire dans lequel se trouve raisin.

    :return: Le chemin du dossier 'raisin'.
    :rtype: str
    :raises OSError: Si l'emplacement de raisin n'est pas cleirement defini.
    """
    with Printer("Searching for the destination folder...") as p:
        candidats = set()
        for path in sys.path:
            if os.path.isdir(path):
                if "raisin" in os.listdir(path):
                    candidats.add(path)
        if len(candidats) >= 2:
            candidats = {c for c in candidats if c != os.getcwd()}
        if not candidats:
            p.show("Folder not found!")
            raise FileNotFoundError("'raisin' ne semble pas etre bien installe dans l'ordinateur.\n"
                "Si il est installe a un endroit bizzard, ajoutez le repertoire au PYTHONPATH.\n"
                "Si il n'est pas installe, tapez '%s -m raisin install'" % sys.executable)
        if len(candidats) >= 2:
            p.show("'raisin' is installed in too many places!")
            raise FileExistsError(
                "'raisin' est installe a differents endroits.\n" \
                + "les voici: {}\n".format(", ".join(candidats)) \
                + "Supprimez les doublons de raisin.")
        dest = os.path.join(list(candidats)[0], "raisin")
        p.show("Folder: %s" % repr(dest))
        return dest

def main(version="stable"):
    """
    |========================|
    | Fait la mise a niveau. |
    |========================|

    La mise a jour est faite a partir du depo framagit.

    entree
    ------
    :param version: "stable" ou "unstable". Permet de choisir
        si la mise a jour est faite a partir d'une version stable
        ou a partir de la version en cours de devellopement.
    :type version: str

    sortie
    ------
    :raises OSError: Si raisin est mal installe.
        Ou dumoins que le dossier d'installation n'est
        pas clair.
    :raises PermissionError: Si les permissions ne sont pas
        suffisantes pour pouvoir ecrire la nouvelle version.
    """
    assert version == "stable" or version == "unstable", \
        "'version' cans only be 'stable' ou 'unstable'.\n" \
        "Not %s." % repr(version)

    with Printer("Upgrade raisin with %s version..." % version) as p:
        # Recherche du dossier de destination
        dest = find_folder()

        # Telechargement.
        url = URL_STABLE if version == "stable" else URL_UNSTABLE
        with Printer("Download %s files..." % version):
            p.show("URL: %s" % repr(url))
            r = requests.get(url)
            archive = os.path.join(temprep, "raisin.tar.gz")
            data = r.content
            p.show("Datasize: %.2f Mio" % (len(data)/2**20))
            with open(archive, "wb") as f:
                f.write(data) # Creation du fichier 'raisin.tar.gz'.
        
        # Extraction dans le bon dossier.
        with Printer("Archive extraction..."):
            archive_ex = os.path.join(temprep, "raisin")
            with tarfile.open(archive) as fs: # Extraction du fichier 'raisin.tar.gz'.
                fs.extractall(path=archive_ex) # Creation du dossier 'raisin'.
            if not os.path.exists(archive_ex):
                raise PermissionError(
                    "Impossible d'extraire l'archice ici: %s" \
                    % repr(archive_ex))
            os.remove(archive) # Suppression du fichier 'raisin.tar.gz'.
            p.show("Datasize: %.2f Mio" % (sum(os.path.getsize(os.path.join(pa, f))
                    for pa, _, fs in os.walk(archive_ex) for f in fs)/2**20))

        # La version actuelle n'est-elle pas deja la derniere?
        with Printer("Change analysis.."):
            src = os.path.join(archive_ex, os.listdir(archive_ex)[0], "raisin")
            hash1 = dirhash(dest, "md5", match=["*.py"])
            hash2 = dirhash(src, "md5", match=["*.py"])
            if hash1 == hash2:
                p.show("The current version is already the latest.")
                return

        # Remplacement.
        with Printer("Replacing new files..."):
            # Supression ancien.
            for old_mod in os.listdir(dest):
                # On ne fait pas juste shutil.copytree(src, dest)
                # car les droits du dossier raisin sraient perdus.
                if os.path.isfile(os.path.join(dest, old_mod)):
                    os.remove(os.path.join(dest, old_mod))
                else:
                    shutil.rmtree(os.path.join(dest, old_mod))
            
            for new_mod in os.listdir(src):
                shutil.move(os.path.join(src, new_mod), os.path.join(dest, new_mod))
            shutil.rmtree(archive_ex) # Supression du dossier 'raisin' en locale.

        # On donne les droits de modifications.
        if identity["has_admin"]:
            for d, _, fs in os.walk(dest):
                os.chmod(d, 0o777)
                for f in fs:
                    os.chmod(os.path.join(d, f), 0o777)
