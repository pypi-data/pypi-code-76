#!/usr/bin/env python3


import io
import os
import re
import sys

import raisin
from ..tools import Printer, identity


def make_analyse():
    """
    cherche les informations relatives a tous les modules installes
    retourne un dictionaire qui a chaque module, associ ces caracteristiques
    """
    with Printer("Updated information on modules..."):
        return {modulename: get_infos(modulename) for modulename in get_installed_modules()}

def get_infos(modulename):
    """
    retourne un tuple contenant 3 champs:
        -validite du module:
            -True si il est present et teste
            -None si il est present mais pas teste
            -False si il n'est pas present ou qu'il n'est pas fonctionnel
        -version:
            -(STR) ou None
        -code en python
            -True si le module est entierement code en python
            -None si on en sait rien
            -False si il y a autre chose que du python
    """
    assert type(modulename) is str, "'modulename' doit etre le nom du module (str), or il s'agit d'un (%s)." % type(modulename)

    with Printer("getting infos about '%s' ..." % modulename) as p:
        try:
            module = __import__(modulename)
        except KeyboardInterrupt as e:
            raise e from e
        except ImportError:
            p.show("Failed to import.")
            return False, None, None
        except MemoryError:
            p.show("Memory error.")
            return False, None, None
        except Exception as e:
            p.show(e)
            return False, None, None
        test = test_module(module, modulename)
        all_python = test_all_python(module)
        try:
            try:
                version = module.__version__
            except AttributeError:
                version = module.VERSION
            if type(version) is list or type(version) is tuple: # si la version est du genre (2, 5, 3)
                version = ".".join(map(str, version))           # on en fait un "2.5.3"
            if test is True:
                p.show("It works properly, version: %s." % version)
            elif test is False:
                p.show("It is all broken, version: %s." % version)
            else:
                p.show("No test available for this module, version: %s." % version)
            return test, version, all_python
        except AttributeError:
            if test is True:
                p.show("It works properly.")
            elif test is False:
                p.show("It is all broken.")
            else:
                p.show("No test available for this module.")
            return test, None, all_python
        finally:
            del module

def test_module(module, modulename):
    """
    verifi que le module 'module', nome 'modulename'
    fonctionne correctement
    retourne True si le module est ok et False si il est defaillant
    Si on en sait rien, return None
    """
    with Printer("verification of the '%s' module..." % modulename) as p:
        if modulename == "abc":
            return None
        elif modulename == "aifc":
            return None
        elif modulename == "argparse":
            return None
        elif modulename == "array":
            return None
        elif modulename == "ast":
            return None
        elif modulename == "asynchat":
            return None
        elif modulename == "asyncio":
            return None
        elif modulename == "asyncore":
            return None
        elif modulename == "atexit":
            return None
        elif modulename == "audioop":
            return None
        elif modulename == "base64":
            return None
        elif modulename == "bdb":
            return None
        elif modulename == "binascii":
            return None
        elif modulename == "binhex":
            return None
        elif modulename == "bisect":
            return None
        elif modulename == "builtins":
            return None
        elif modulename == "bz2":
            return None
        elif modulename == "calendar":
            return None
        elif modulename == "cgi":
            return None
        elif modulename == "cgitb":
            return None
        elif modulename == "chunk":
            return None
        elif modulename == "cmath":
            return None
        elif modulename == "cmd":
            return None
        elif modulename == "code":
            return None
        elif modulename == "codecs":
            return None
        elif modulename == "codeop":
            return None
        elif modulename == "collections":
            return None
        elif modulename == "colorsys":
            return None
        elif modulename == "compileall":
            return None
        elif modulename == "concurrent":
            return None
        elif modulename == "configparser":
            return None
        elif modulename == "contextlib":
            return None
        elif modulename == "copy":
            return None
        elif modulename == "copyreg":
            return None
        elif modulename == "cProfile":
            return None
        elif modulename == "csv":
            return None
        elif modulename == "ctypes":
            return None
        elif modulename == "datetime":
            return None
        elif modulename == "dbm":
            return None
        elif modulename == "decimal":
            return None
        elif modulename == "difflib":
            return None
        elif modulename == "dis":
            return None
        elif modulename == "distutils":
            return None
        elif modulename == "doctest":
            return None
        elif modulename == "dummy_threading":
            return None
        elif modulename == "email":
            return None
        elif modulename == "encodings":
            return None
        elif modulename == "enum":
            return None
        elif modulename == "errno":
            return None
        elif modulename == "faulthandler":
            return None
        elif modulename == "filecmp":
            return None
        elif modulename == "fileinput":
            return None
        elif modulename == "fnmatch":
            return None
        elif modulename == "formatter":
            return None
        elif modulename == "fractions":
            return None
        elif modulename == "ftplib":
            return None
        elif modulename == "functools":
            return None
        elif modulename == "gc":
            return None
        elif modulename == "getopt":
            return None
        elif modulename == "getpass":
            return None
        elif modulename == "gettext":
            return None
        elif modulename == "glob":
            return None
        elif modulename == "gzip":
            return None
        elif modulename == "hashlib":
            return None
        elif modulename == "heapq":
            return None
        elif modulename == "hmac":
            return None
        elif modulename == "html":
            return None
        elif modulename == "http":
            return None
        elif modulename == "imaplib":
            return None
        elif modulename == "imghdr":
            return None
        elif modulename == "imp":
            return None
        elif modulename == "importlib":
            return None
        elif modulename == "inspect":
            return None
        elif modulename == "io":
            return None
        elif modulename == "ipaddress":
            return None
        elif modulename == "itertools":
            return None
        elif modulename == "json":
            return None
        elif modulename == "keyword":
            return None
        elif modulename == "lib2to3":
            return None
        elif modulename == "linecache":
            return None
        elif modulename == "locale":
            return None
        elif modulename == "logging":
            return None
        elif modulename == "lzma":
            return None
        elif modulename == "macpath":
            return None
        elif modulename == "mailbox":
            return None
        elif modulename == "mailcap":
            return None
        elif modulename == "marshal":
            return None
        elif modulename == "math":
            return None
        elif modulename == "mimetypes":
            return None
        elif modulename == "mmap":
            return None
        elif modulename == "modulefinder":
            return None
        elif modulename == "multiprocessing":
            return None
        elif modulename == "netrc":
            return None
        elif modulename == "nntplib":
            return None
        elif modulename == "numbers":
            return None
        elif modulename == "operator":
            return None
        elif modulename == "optparse":
            return None
        elif modulename == "os":
            return None
        elif modulename == "parser":
            return None
        elif modulename == "pathlib":
            return None
        elif modulename == "pdb":
            return None
        elif modulename == "pickle":
            return None
        elif modulename == "pickletools":
            return None
        elif modulename == "pkgutil":
            return None
        elif modulename == "platform":
            return None
        elif modulename == "plistlib":
            return None
        elif modulename == "poplib":
            return None
        elif modulename == "pprint":
            return None
        elif modulename == "profile":
            return None
        elif modulename == "pstats":
            return None
        elif modulename == "py_compile":
            return None
        elif modulename == "pyclbr":
            return None
        elif modulename == "pydoc":
            return None
        elif modulename == "queue":
            return None
        elif modulename == "quopri":
            return None
        elif modulename == "random":
            return None
        elif modulename == "re":
            if re.fullmatch(r"\s", " "):
                return True
            return False
        elif modulename == "reprlib":
            return None
        elif modulename == "rlcompleter":
            return None
        elif modulename == "runpy":
            return None
        elif modulename == "sched":
            return None
        elif modulename == "select":
            return None
        elif modulename == "selectors":
            return None
        elif modulename == "shelve":
            return None
        elif modulename == "shlex":
            return None
        elif modulename == "shutil":
            return None
        elif modulename == "signal":
            return None
        elif modulename == "site":
            return None
        elif modulename == "smtpd":
            return None
        elif modulename == "smtplib":
            return None
        elif modulename == "sndhdr":
            return None
        elif modulename == "socket":
            return None
        elif modulename == "socketserver":
            return None
        elif modulename == "sqlite3":
            return None
        elif modulename == "ssl":
            return None
        elif modulename == "stat":
            return None
        elif modulename == "statistics":
            return None
        elif modulename == "string":
            return None
        elif modulename == "stringprep":
            return None
        elif modulename == "struct":
            return None
        elif modulename == "subprocess":
            return None
        elif modulename == "sunau":
            return None
        elif modulename == "symbol":
            return None
        elif modulename == "symtable":
            return None
        elif modulename == "sys":
            return None
        elif modulename == "sysconfig":
            return None
        elif modulename == "tabnanny":
            return None
        elif modulename == "tarfile":
            return None
        elif modulename == "telnetlib":
            return None
        elif modulename == "tempfile":
            return None
        elif modulename == "textwrap":
            return None
        elif modulename == "threading":
            return None
        elif modulename == "time":
            return None
        elif modulename == "timeit":
            return None
        elif modulename == "tkinter":
            return None
        elif modulename == "token":
            return None
        elif modulename == "tokenize":
            return None
        elif modulename == "trace":
            return None
        elif modulename == "traceback":
            return None
        elif modulename == "tracemalloc":
            return None
        elif modulename == "turtle":
            return None
        elif modulename == "types":
            return None
        elif modulename == "typing":
            return None
        elif modulename == "unicodedata":
            return None
        elif modulename == "unittest":
            return None
        elif modulename == "urllib":
            return None
        elif modulename == "uu":
            return None
        elif modulename == "uuid":
            return None
        elif modulename == "venv":
            return None
        elif modulename == "warnings":
            return None
        elif modulename == "wave":
            return None
        elif modulename == "weakref":
            return None
        elif modulename == "webbrowser":
            return None
        elif modulename == "wsgiref":
            return None
        elif modulename == "xdrlib":
            return None
        elif modulename == "xml":
            return None
        elif modulename == "xmlrpc":
            return None
        elif modulename == "zipapp":
            return None
        elif modulename == "zipfile":
            return None
        elif modulename == "zipimport":
            return None
        elif modulename == "zlib":
            return None
        else:
            p.show("the module %s is unknown" % modulename)
            return None

def test_all_python(module):
    """
    retourne True si le module 'module' est entierement code en python
    retourne False le cas echeant
    """
    return False # a coder

def get_installed_modules():
    """
    cede le nom de tous les modules present sur cette machine
    """
    with Printer("Recovery of the names of all installed modules..."):
        for dossier in sys.path:                    # pour chaque repertoir ou python est succeptible d'aller chercher des modules
            if os.path.isdir(dossier) and dossier != "":
                for file in os.listdir(dossier):    # pour chaque machine qu'il y a dans ce repertoire
                    if os.path.isfile(os.path.join(dossier, file)) and re.fullmatch(r".+\.py", file):# si c'est un fichier python
                        if re.fullmatch(r"[a-zA-Z_\x7f-\U000fffff][a-zA-Z0-9_\x7f-\U000fffff]*", file[:-3]):
                            if file[:-3] not in ["antigravity"]:# si ce n'est pas un module a eviter
                                yield file[:-3]     # alors ce fichier est un module
                    elif os.path.isdir(os.path.join(dossier, file)) and file != "__pycache__":
                        if re.fullmatch(r"[a-zA-Z_\x7f-\U000fffff][a-zA-Z0-9_\x7f-\U000fffff]*", file):
                            if file not in ["antigravity"]:# si ce n'est pas un module a eviter
                                yield file

def get_dependencies(modulename):
    """
    retourne l'ensemble des modules directement importe a l'interieur
    de 'modulename'
    """
    assert type(modulename) is str, "'modulename' doit etre le nom du module (str), or il s'agit d'un (%s)." % type(modulename)

    with Printer("Recherche des dependance du module '%s'..." % modulename) as p:
        with Printer("Recherche de l'emplacement..."):
            emplacements = []                       # contient les chemin de tous les fichier python faisant parti du module
            for papa in sys.path:                   # on regarde de partou ou sont cence se trouver les modules
                papa = os.path.abspath(papa)
                if not os.path.isdir(papa):
                    continue
                for m in os.listdir(papa):
                    if m == modulename + ".py":     # si on a trouve le module et que c'est un fichier
                        emplacements.append(os.path.join(papa, m)) # on l'ajoute
                        p.show(os.path.join(papa, m))
                    elif m == modulename and os.path.isdir(os.path.join(papa, m)): # si le module est un repertoire
                        for base, dirs, files in os.walk(os.path.join(papa, m)): # on fouille les sous-repertoires
                            if os.path.join(os.path.dirname(__file__), "venv") in base: # sauf si il s'agit du repertoir d'environement virtuel
                                continue            # car ca permet de gagner du temps si on s'analyse soit meme
                            for file in files:
                                if file.split(".")[-1] == "py":
                                    emplacements.append(os.path.join(base, file))
                                    p.show(os.path.join(base, file))
            if not emplacements:                    # si on a rien trouve
                p.show("Module file not found...")
                return set()
        with Printer("Analysis of these files..."):
            depend = set()
            for filname in emplacements:
                with raisin.open(filname, "rp") as f:
                    try:
                        tree = f.read()             # on extrait l'arbre syntaxique de chacun des ces fichiers
                    except SyntaxError:
                        break
                    depend |= tree.get_modules()    # puis on y recherche les modules
            depend = {mod.split(".")[0] for mod in depend}
            depend = {mod for mod in depend if mod and mod != modulename}
            return depend

def get_all_dependencies(modulename):
    """
    retourne l'ensemble des modules qui interviennent de facon
    plus ou moin directe dans modulename
    retourne les dependances, et les epandance des depandances, et les ...
    annalyse les dependance (afin d'eviter une boucle infinie)
    """
    assert type(modulename) is str, "'modulename' doit etre le nom du module (str), or il s'agit d'un (%s)." % type(modulename)

    def get_all(modulename, made):
        """
        renvoi les dependances et le nouveau made
        """
        deps = get_dependencies(modulename)
        made.add(modulename)
        continuer = True
        while continuer:
            continuer = False
            for dep in deps.copy():
                if dep not in made:
                    n_dep, made = get_all(dep, made)
                    if n_dep & deps:
                        continuer = True
                    deps |= n_dep
        return deps, made

    with Printer("Recherche de toutes les dependances de '%s', meme les plus elognes..." % modulename):
        deps, made = get_all(modulename, set())
        return deps

def get_unmet_dependencies(modulename):
    """
    retourne l'ensemble des dependances non satisfaite
    par le module de nom 'modulename'
    """
    assert type(modulename) is str, "'modulename' doit etre le nom du module (str), or il s'agit d'un (%s)." % type(modulename)

    missing = set()
    with Printer("Get unmet dependances..."):
        for dep in get_dependencies(modulename):
            validity, version, is_python = get_infos(dep)
            if validity is False:
                missing.add(dep)
    return missing

def install(modulename):
    """
    install le module 'modulename'
    retourne True si le module est installe et fonctionne
    retourne None si il est installe mais qu'il n'est pas teste
    retourne False si il y a un quoique
    """
    def install_tkinter():
        """
        sur linux, tkinter s'installe un peu speciallement
        """
        with Printer("Install tkinter from package manager...") as p:
            if os.name == "posix":
                p.show("Try with 'apt'.")
                if identity["has_admin"]:
                    p.show("Apt has administrator.")
                    if os.system("apt install python3-tk") == 0:
                        return True
                else:
                    p.show("Please put me as administrator.")
                p.show("Try with 'packman'.")
                if os.system("packman -S python3-tk") == 0:
                    return True
            return False

    def install_giacpy():
        """
        xcas est un peu complique a installer, quelque soit la situation

        si il y a le bug:
            W: Erreur de GPG : http://www-fourier.ujf-grenoble.fr/~parisse/debian stable Release : 
            Les signatures suivantes n'ont pas pu être vérifiées car la clé publique n'est pas disponible : 
            NO_PUBKEY 8E62E25D998B1156
        on peu faire:
            gpg --keyserver hkp://keyserver.ubuntu.com:11371 --recv-key 998B1156
            gpg -a --export 998B1156 | apt-key add -
            apt-get update
        """
        with Printer("Install tkinter from package manager...") as p:
            if os.name == "posix":
                p.show("Try with 'apt'.")
                if identity["has_admin"]:
                    p.show("Apt has administrator.")
                    if os.system("apt install python3-giacpy") == 0:
                        return True
                else:
                    p.show("Please put me as administrator.")
                p.show("Try with 'packman'.")
                if os.system("pacman -S python3-giacpy") == 0:
                    return True
                p.show("Try manualy.")
                if identity["has_admin"]:
                    p.show("As administrator.")
                    if os.system("add-apt-repository 'deb http://www-fourier.ujf-grenoble.fr/~parisse/debian/ stable main'") == 0:
                        with open("xcas_public_key.gpg", "wb") as f:
                            f.write(b'-----BEGIN PGP PUBLIC KEY BLOCK-----\n'
                                    b'Version: GnuPG v1.4.10 (GNU/Linux)\n\n'
                                    b'mQENBE/a6hoBCAC/ReFI2FbsyL5csp7guN5m+x'
                                    b'l4MwRdLWt00MtgkdL6oMEN+hug\nz/nmZaPoZq'
                                    b'uDIDNDPssNGuwU0nUivYGtIaT60AJ7zv7yWGhF'
                                    b'KLPcrv7Jo97crYOK\nskEE03L2zOA1DRxlZo6h'
                                    b'vUdfZj8XgjxSvyhmrMiyoP5iQf5vPhUbUGwYZ1'
                                    b'xNQpZh\nQjzFEZpuZ/QC0KkrGjSP42vAK0rEEM'
                                    b'AJ3eaHxlUxdykg6+De274AS4xv2/otB6JF\ng0'
                                    b'TWpfyI+lAo+ydhFDFecceIrZI6xNhKRXhuamfY'
                                    b'tegUVq06EGs0OZ+7S+CBSpVH\nX/TJea3HpQk2'
                                    b'ugfiKkxhZ+GYzWEWfDz8g36JABEBAAG0MUJlcm'
                                    b'5hcmQgUGFyaXNz\nZSA8YmVybmFyZC5wYXJpc3'
                                    b'NlQHVqZi1ncmVub2JsZS5mcj6JATgEEwECACIF'
                                    b'Ak/a\n6hoCGwMGCwkIBwMCBhUIAgkKCwQWAgMB'
                                    b'Ah4BAheAAAoJEI5i4l2ZixFWEwkH/0+4\nVUrU'
                                    b'GpLUEnaNa6d2ft/ccqn+JeL3/jOAjTCiirTSrM'
                                    b'hIjaVoOPt4Le69TA2Pxg9t\nWC3vI2TKSUfON1'
                                    b'YOzsVO4PlQGrQRIUPFnlouIeem4AzD6Jk0KZbW'
                                    b'qNJEnscT4Gvy\nhFg4XaXVFhv4ilNNY7Iw2qqW'
                                    b'1bzp3GDF4jUPRVJpkivsrwMSYgmOTcDpHuwB7B'
                                    b'Uh\n0+peJD0nakVBRSR86zGKKpfvjYvMSWXAXn'
                                    b'qf3Hr/2PajgWWcj78IwT6ouQWiE4a9\nMYwXfR'
                                    b'MLjJEePtvYXzs52Qvqk2avQXlac6Cj57r3XrUD'
                                    b'RTTQKLMvnUAFDOuk0K0W\n3VxL0giUwV+2E/Pp'
                                    b'yeu5AQ0ET9rqGgEIAMKv0pLzuhZAINO+QReBvM'
                                    b'wu5oByptfs\n5FOqD6NXovsml6jwlZENKvrHj2'
                                    b'+kB9cbPEzxYQe7BvVnTcg1LuD6ALfzr7MXleIH'
                                    b'\nrlZlQDIYxDy/C4ST7yk5LWz9itpOExYVMqn2'
                                    b'CmWwIK24MUrTgmo4uT25lLqDxll7\naS7w3QV3'
                                    b'YMhqGzw4Pa2lNtnbBqiFwqp8zgaVH1l5iSARpi'
                                    b'dOTlBWuWrfbdKpyuZb\nmHZOyi2qy5pSvWO333'
                                    b'Q9tQsCe1CFilc3c3rHNwO7NkU+2PE5vlTcFVj1'
                                    b't1D1tllm\nl1L3C62uqbfzkO47bbSZzp38yZPt'
                                    b'3yqQY9R2WFJnLR2mJcGR6UToY0MAEQEAAYkB\n'
                                    b'HwQYAQIACQUCT9rqGgIbDAAKCRCOYuJdmYsRVo'
                                    b'i2B/4neWZ8F6QE5Hu06eEitPbV\nH5YtZl7IyA'
                                    b'pe/X6/qROdt9tfSdMJrN4vl31LMK6ECCnGN4Vd'
                                    b'ZW13Z2D2mQqsjwDy\nM0b4lkmQ5ZHwzQLacvo1'
                                    b'XcSCazi9Av9rGQpnwu4k+vioMk1znsyVGqJgjS'
                                    b'EQDRI+\nZ9YANtGurhHYUgxT9WCJod3ogvDnrq'
                                    b'TFSRpEyrZPPDZb9HfFTI+rTHGTRHCx4+xk\nwe'
                                    b'CxL8fVj3/YDrii9FW/Hm1fSt1zwQZWgX2cHte+'
                                    b'6pD6gVH4c6h0C87yZOJ4YxcH\ntbU0JgFGJhf6'
                                    b'GxHjCk5/F5bLMHjfsVLrJyWd7sN3gH76MwcSLf'
                                    b'tF/Durjx0F9r64\n=1H7u\n-----END PGP PU'
                                    b'BLIC KEY BLOCK-----\n')
                        os.system("apt add xcas_public_key.gpg")
                        os.remove("xcas_public_key.gpg")
                        if os.system("apt update") == 0:
                            if os.system("apt-get install *giac*") == 0:
                                return True
                else:
                    p.show("Please put me as administrator.")
            return False

    assert type(modulename) is str, "'modulename' doit etre le nom du module (str), or il s'agit d'un (%s)." % type(modulename)

    with Printer("Install '%s'..." % modulename) as p:
        validity, version, is_python = get_infos(modulename)
        if validity is True: # si le module est present et teste
            p.show("The module '%s' is already installed!" % modulename)
            return validity
        elif validity is None: # si le module est present mais pas teste
            p.show("The module '%s' is already installed, but it is not tested!" % modulename)
            return validity

        if modulename == "tkinter":
            return install_tkinter()
        elif modulename == "Crypto":
            return install("pycryptodome")
        elif modulename == "Cryptodome":
            return install("pycryptodomex")
        elif modulename == "cv2":
            return install("opencv-python")
        elif modulename == "sksound":
            return install("scikit-sound")
        elif modulename == "giacpy":
            return install_giacpy()
        elif modulname == "graph":
            return install("graph-theory")

        # install with pip
        with Printer("Install '%s' with 'pip'..." % modulename) as p:
            if identity["has_admin"]:
                p.show("Installation with administrator privileges.")
            else:
                p.show("Installation without admin privilages.")
            res = os.system("%s -m pip -q install --upgrade %s" % (sys.executable, modulename))
            if res == 0:
                validity, version, is_python = get_infos(modulename)
                if validity in (True, None):
                    p.show("Le module '%s' a ete installe avec succes!" % modulename)
                    return validity

        p.show("Le module '%s' ne s'est pas bien installe!" % modulename)
        return False

