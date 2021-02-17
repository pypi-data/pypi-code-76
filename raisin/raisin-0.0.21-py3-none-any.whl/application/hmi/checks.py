#!/usr/bin/env python3

"""
|==================|
| User protection. |
|==================|

Verifi les entree utilisateur.
Les professeurs nous ont toujours appris:
Le pire ennemi en informatique, c'est l'utilisateur!
Et bien toute les verification de saisie de l'utilisateur se font ici
"""

import ipaddress
import os
import re
import socket

from ...tools import Printer, identity
from ...communication import constants

def dns_ip_verification(dns, version):
    """
    Verfifie que le dns 'dns' soit bien un nom de domaine valide et que en plus de ca, il pointe bien ici, et c'est pas fini:
    il faut par dessus le marche qu'il prene en compte le bon protocole ip
    retourne True si toutes ces conditions sont satisfaites, False sinon.
    """
    with Printer("DNS verification...") as p:
        if version != 6 and version != 4:
            p.show("La version de protocole ip doit etre 6 ou 4, pas %s." % version)
            return False
    if not re.fullmatch(r"(?!\-)(?:[a-zA-Z\d\-_]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}", dns):
        p.show("Le nom de domaine doit satisfaire l'expression suivante: "
            "^(?!\\-)(?:[a-zA-Z\\d\\-_]{0,62}[a-zA-Z\\d]\\.){1,126}(?!\\d+)[a-zA-Z\\d]{1,63}$")
        return False
    try:
        ip = socket.gethostbyname(dns)
    except socket.gaierror:
        p.show("Ce nom de domaine n'existe pas!")
        return False
    p.show("Le domaine '%s' est associé a l'adresse '%s'." % (dns, ip))
    if version == 6:
        if ipaddress.ip_address(ip) == identity["ipv6"]:
            return True
        elif ipaddress.ip_address(ip) == identity["ipv4_wan"]:
            p.show("Le DNS est bon, mais il est associer a une ipv4, pas 6, entrez le dans la case juste en dessous.")
            return False
        p.show("Le DNS ne pointe pas le bon endroit, il devrait pointer sur '%s'." % identity["ipv6"])
        return False
    else:
        if ipaddress.ip_address(ip) == identity["ipv4_wan"]:
            return True
        elif ipaddress.ip_address(ip) == identity["ipv6"]:
            p.show("Le DNS est bon, mais il est associer a une ipv6, pas 4, entrez le dans la case juste au dessus.")
            return False
        p.show("Le DNS ne pointe pas le bon endroit, il devrait pointer sur '%s'." % identity["ipv4_wan"])
        return False

def email_verification(email):
    """
    Retourne True si 'email'
    est une adresse couriel correcte.
    """
    import unidecode
    with Printer("Email verification...") as p:
        if re.fullmatch(
                r"[a-zA-Z0-9._-]{1,254}@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}",
                unidecode.unidecode(email)):
            p.show("Ok")
            return True
        p.show("Bad")
        return False

def paths_verification(paths, revert=False):
    """
    Verifie que la variable 'paths'
    ait une forme correcte pour decrire un ensemble
    de repertoires ou fichiers avec des options.
    S'assure aussi que les parametres soient coherents.
    Retourne True si la variable est ok, False si il y a un quoique.
    :param revert: Retourne le message d'erreur plutot qu'un booleen.
    """
    with Printer("Paths descriptor verification...") as p:
        with Printer("Data format verification..."):
            if not isinstance(paths, dict):
                message = "'paths' must be a dictionary, it is a %s." % type(paths).__name__
                p.show(message)
                return message if revert else False
            if "paths" not in paths:
                message = "Missing field 'paths'."
                p.show(message)
                return message if revert else False
            if "excluded_paths" not in paths:
                message = "Missing field 'excluded_paths'."
                p.show(message)
                return message if revert else False
            for val in paths.values():
                if not isinstance(val, list):
                    message = "Fileds have to be list, not %s." % type(val).__name__
                    p.show(message)
                    return message if revert else False
        with Printer("Data consistency check..."):
            # verification de la taille des champs
            for champs, val in paths.items():
                if champs not in ("paths", "excluded_paths"):
                    if len(val) != len(paths["paths"]):
                        message = "Il doit y avoir %d options a chaque fois. Or le champs %s en comporte %d." \
                            % (len(paths["paths"]), champs, len(val))
                        p.show(message)
                        return message if revert else False
            # verification que les chemins pointent tous quelque part
            for path in paths["paths"] + paths["excluded_paths"]:
                if not os.path.exists(path):
                    message = "Path %s does not exist!" % repr(path)
                    p.show(message)
                    return message if revert else False
                if not os.path.isabs(path):
                    message = "%s is not absolute." % repr(path)
                    p.show(message)
                    return message if revert else False
            # verification que les "excluded_paths" soient bien contenus dans les paths
            for excluded_path in paths["excluded_paths"]:
                est_inclu = False
                for path in paths["paths"]:
                    ex = os.path.abspath(os.path.realpath(excluded_path)) # on s'affranchit des liens symboliques et tout
                    pa = os.path.abspath(os.path.realpath(path))
                    if ex[:len(pa)] == pa and len(ex) > len(pa):
                        est_inclu = True
                        break
                if not est_inclu:
                    message = "The path %s has no parent." % repr(excluded_path)
                    p.show(message)
                    return message if revert else False
            # verification qu'il n'y ai pas de doublon
            if len(set(paths["paths"])) != len(paths["paths"]):
                message = "'paths': There is a duplicate path."
                p.show(message)
                return message if revert else False
            if len(set(paths["excluded_paths"])) != len(paths["excluded_paths"]):
                message = "'excluded_paths': There is a duplicate path."
                p.show(message)
                return message if revert else False
        return True

def padlock_verification(padlock):
    """
    Retourne True si 'padlock' est correcte.
    Retourne False dans le cas contraire.
    """
    with Printer("Padlock verification...") as p:
        if not isinstance(padlock, dict):
            p.show("'padlock' doit etre un dictionaire, c'est un %s." % type(padlock).__name__)
            return False
        if "cipher" not in padlock:
            p.show("Il maque le champs 'cipher'.")
            return False
        if "paths" not in padlock:
            p.show("Il manque le champs 'paths'.")
            return False
        if "break_time" not in padlock:
            p.show("Il manque le champs 'break_time'.")
            return False
        if "notify_by_email" not in padlock:
            p.show("Il manque le champs 'notify_by_email'.")
            return False
        if type(padlock["cipher"]) is not bool:
            p.show("'padlock[\"cipher\"]' doit etre un booleen, c'est un %s." % type(padlock["cipher"]))
            return False
        if not paths_verification(padlock["paths"]):
            p.show("The paths description is not correct")
            return False
        if type(padlock["break_time"]) is not int:
            p.show("'padlock[\"break_time\"]' doit etre un entier, c'est un %s." % type(padlock["break_time"]))
            return False
        if padlock["break_time"] < 0:
            p.show("'padlock[\"break_time\"]' doit etre positif.")
            return False
        if type(padlock["notify_by_email"]) is not bool:
            p.show("'padlock[\"notify_by_email\"]' doit etre un booleen, c'est un %s." % type(padlock["notify_by_email"]))
            return False
        return True

def port_verification(port):
    """
    S'assure que le port d'ecoute specifie soit correcte
    retourne True si c'est la cas et False sinon.
    """
    with Printer("Port verification...") as p:
        if type(port) is str:
            if not port.isdigit():
                p.show("'port' doit etre un entier positif.")
                return False
            port = int(port)
        if type(port) is not int:
            p.show("'port' doit etre un entier ou une chaine de caractere, pas un %s." % type(port))
            return False
        if port < 1 or port > 49151:
            p.show("'port' doit etre compris entre 1 et 49151.")
            return False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if identity["ipv4_lan"]:
                sock.bind((str(identity["ipv4_lan"]), port))
            else:
                sock.bind(("127.0.0.1", port))
            sock.listen()
            sock.close()
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            if identity["ipv6"]:
                sock.bind((str(identity["ipv6"]), port))
            else:
                sock.bind(("::1", port))
            sock.listen()
            sock.close()
        except PermissionError:
            p.show("Le port %d nessecite d'avoir les droits d'administrateur, embetant!" % port)
            return False
        except OSError:
            p.show("Le port est deja utilise par une autre application.")
            return False
        if port in constants.RESERVED_PORTS:
            proche = sorted((set(range(1024, 49152, 1)) - set(constants.RESERVED_PORTS)), key=lambda p : abs(p-port))[0]
            p.show("Ce port %d est reservé par l'institut de l'IANA. Le port libre le plus proche est le port %d." % (port, proche))
        return True

def security_verification(security):
    """
    Fait des verifications afin de s'assurer
    que les champs presents dans 'security' soient valides et
    coherent entre eux. Retourne True si ils sont coherent et False si ils ne le sont pas.
    """
    with Printer("Security verification...") as p:
        if not isinstance(security, dict):
            p.show("'security' doit etre un dictionaire, c'est un {}.".format(
                type(security).__name__))
            return False
        
        # presence des bons champs
        champs = ["public_key", "private_key", "psw", "hash", "sel", "sentence_memory"]
        manque = set(champs) - set(security.keys())
        if manque:
            p.show("Missing %s keys." % ", ".join(map(repr, security.keys())))
            return False
        surplus = set(security.keys()) - set(champs)
        if surplus:
            p.show("To much keys (%s)." % ", ".join(map(repr, security.keys())))
            return False

        # bon types
        if not isinstance(security["public_key"], bytes):
            p.show("'public_key' must be bytes, no '%s'." % type(security["public_key"]).__name__)
            return False
        if not isinstance(security["private_key"], bytes):
            p.show("'private_key' must be bytes, no '%s'." % type(security["private_key"]).__name__)
            return False
        if security["psw"] != None and not isinstance(security["psw"], str):
            p.show("'psw' must be None or str, no '%s'."  % type(security["psw"]).__name__)
            return None
        if security["hash"] != None and not isinstance(security["hash"], str):
            p.show("'hash' must be None or str, no '%s'."  % type(security["hash"]).__name__)
            return None
        if not isinstance(security["sel"], bytes):
            p.show("'sel' must be bytes, no '%s'."  % type(security["sel"]).__name__)
            return None
        if not isinstance(security["sentence_memory"], str):
            p.show("'sentence_memory' must be str, no '%s'."  % type(security["sentence_memory"]).__name__)
            return None

        # bonne forme
        if not re.search(
                r"-----BEGIN PUBLIC KEY-----(.|\n)+-----END PUBLIC KEY-----",
                security["public_key"].decode(errors="ignore")):
            p.show("La clef publique n'est pas au format 'PEM'.")
            return False
        if not re.search(
                r"-----BEGIN RSA PRIVATE KEY-----(.|\n)+-----END RSA PRIVATE KEY-----",
                security["private_key"].decode()):
            p.show("La clef privee n'est pas au format 'PEM'.")
            return False
        if security["psw"] == "":
            p.show("Le mot de passe ne doit pas etre une chaine vide.")
            return False

        return True

def username_verification(username):
    """
    Retourne True si le 'username' est un
    username valide, retourne False le cas echeant.
    """
    import unidecode
    with Printer("Username verification...") as p:
        if re.fullmatch(
                r"[a-zA-Z]{3,30}\d{,5}(?:[ _-][a-zA-Z0-9]{1,30}?){0,5}",
                unidecode.unidecode(username)):
            p.show("Ok")
            return True
        p.show("Bad")
        return False

def schedules_verification(schedules):
    """
    S'assure que 'schedules' est un dictionaire qui represente
    correctement les horaires.
    """
    with Printer("Schedules verification...") as p:
        if not isinstance(schedules, dict):
            p.show("'schedules' doit etre un dictionaire, pas un %s." \
                % type(schedules).__name__)
            return False
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            if not day in schedules:
                p.show("The '%s' key is missing." % day)
                return False
            if not isinstance(schedules[day], dict):
                p.show("Chaque jour doit etre represente par un dictionaire, pas par un %s." \
                    % type(schedules[day]).__name__)
                return False
            for date, limitation in schedules[day].items():
                if not re.fullmatch(r"\d{1,2}:\d{1,2}", date):
                    p.show("Le format de la date doit satisfaire l'expression reguliere:"
                        " \\d{1,2}:\\d{1,2}. %s ne la respecte pas." % date)
                    return False
                h, m = date.split(":")
                if int(h) >= 24:
                    p.show("On ne peut pas metre une heure plus tardive que 23h.")
                    return False
                if int(m) >= 60:
                    p.show("Il n'y a pas plus de 60 minutes dans une heure!")
                    return False
                if not isinstance(limitation, int) and not isinstance(limitation, float):
                    p.show("Les valeurs doivent bool, int ou float, pas %s." \
                        % type(limitation).__name__)
                    return False
        return True

def temperature_verification(temperature):
    """
    S'assure que la temperature reflete bien une valeur
    de temperature coherente pour un processeur.
    """
    with Printer("Temperature verification...") as p:
        if not isinstance(temperature, int) and not isinstance(temperature, float):
            p.show("La temperature doit etre un nombre, pas par un %s." \
                % type(temperature))
            return False
        if temperature < 20 or temperature > 100:
            p.show("Le tempertaure doit etre comprise en tre 20°C et 100°C. "
                "%d n'est pas dans cette fourchette." % temperature)
            return False
        return True

def bandwidth_verification(downflow, rising_flow):
    """
    S'assure que les parametre soient corecte
    Renvoie True si les debit sont coherent, retourne False sinon.
    """
    with Printer("Bandwidth verification...") as p:
        if not isinstance(downflow, int) and not isinstance(downflow, float):
            p.show("'downflow' doit etre un nonmbre, pas un %s." \
                % type(downflow).__name__)
            return False
        if not isinstance(rising_flow, int) and not isinstance(rising_flow, float):
            p.show("'rising_flow' doit etre un nonmbre, pas un %s." \
                % type(rising_flow).__name__)
            return False
        if downflow < 0 or downflow > 125:
            p.show("'downflow' doit etre compris entre 0 et 125 Mio/s. "
                "%d ne fait pas parti de cet intervalle." % downflow)
            return False
        if rising_flow < 0 or rising_flow > 125:
            p.show("'rising_flow' doit etre compris entre 0 et 125 Mio/s. "
                "%d ne fait pas parti de cet intervalle." % rising_flow)
            return False
        return True

def recording_directory_verification(recording_directory):
    """
    S'assure que le repertoire 'recording_directory' existe bien
    et que l'on a les droit d'ecriture dedans.
    Retourne False si l'une des cvonditions n'est pas respecee, True sinon.
    """
    with Printer("Recording directory verification...") as p:
        if not isinstance(recording_directory, str):
            p.show("'recording_directory' doit etre une chaine de "
                "caractere, pas un %s." % type(recording_directory).__name__)
            return False
        if not os.path.isdir(recording_directory):
            p.show("\"%s\" n'est pas un repertoire existant." % recording_directory)
            return False
        try:
            with open(os.path.join(recording_directory, "tmp"), "w") as f:
                f.write("contenu test")
        except PermissionError:
            p.show("Il n'y a pas les droits d'ecriture dans "
                "le dossier \"%s\"." % recording_directory)
            return False
        else:
            os.remove(os.path.join(recording_directory, "tmp"))
        return True

def free_size_verification(free_size, path):
    """
    S'assure que 'free_size' soit correcte.
    """
    with Printer("Free size verification...") as p:
        if isinstance(free_size, str):
            if not free_size.isdigit():
                p.show("'free_size' doit etre un entier positif.")
                return False
            free_size = int(free_size)
        if not isinstance(free_size, int):
            p.show("'free_size' doit etre un entier ou une chaine "
                "de caractere, pas un %s." % type(free_size).__name__)
            return False
        try:
            import shutil
        except ImportError:
            return True
        else:
            dispo = int(shutil.disk_usage(path).total/2**20)
            if free_size > dispo:
                p.show("Le disque fait seulement %d Mio!" % dispo)
                return False
        return True

def listen_verification(listen):
    """
    S'assure que le nombre de connection simultane
    maximum admissible par le serveur soit correct.
    retourne True si c'est la cas et False sinon.
    """
    with Printer("Listen verification...") as p:
        if isinstance(listen, str):
            if not listen.isdigit():
                p.show("'listen' doit etre un entier positif.")
                return False
            listen = int(listen)
        if not isinstance(listen, int):
            p.show("'listen' doit etre un entier. Pas un %s." \
                % type(listen).__name__)
            return False
        if listen < 1:
            p.show("'listen' doit etre supperieur ou egal a 1.")
            return False
        return True

def network_name_verification(network_name):
    """
    Retourne True si 'network name' permet bien de
    se raccrocher a un cluster.
    """
    return True
    raise NotImplementedError("S'assurer que le nom de serveur est correcte.")

def port_forwarding_verification(port):
    """
    S'assure que la redirection de port annoncee soit bien coherente.
    Retourne True si c'est la cas et False si ce n'est pas le cas.
    """
    with Printer("Port forwarding verification...") as p:
        if isinstance(port, str):
            if not port:
                return True
            if not port.isdigit():
                p.show("'port' doit etre un entier positif.")
                return False
            port = int(port)
        if not isinstance(port, int):
            p.show("'port' doit etre un entier ou une chaine de "
                "caractere, pas un %s." % type(port).__name__)
            return False
        if port < 1 or port > 49151:
            p.show("'port' doit etre compris entre 1 et 49151.")
            return False

        return True
        raise NotImplementedError("Faire la verification que le port colle")

def access_token_verification(access_token):
    """
    Retourne True si l'access token Drobox est valide.
    """
    with Printer("Access token verification...") as p:
        if not isinstance(access_token, str):
            p.show("'access token' must be str, "
                "not %s." % type(access_token).__name__)
            return False
        import raisin.communication.dropbox as dropbox
        try:
            dropbox.Dropbox("id", access_token).connect()
        except KeyboardInterrupt as e:
            raise e from e
        except Exception as e:
            p.show(" and ".join(e.args))
            p.show("Imposible de se connecter avec cet acces token.")
            return False
        else:
            return True
