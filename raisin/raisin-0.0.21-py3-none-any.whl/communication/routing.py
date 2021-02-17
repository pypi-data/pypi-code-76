#!/usr/bin/env python3

"""
|===========================================|
| Etabli la connection entres les machines. |
|===========================================|

Il permet la gestion bas niveau des sockets TCP.
C'est la partie qui permet de faire transiter les
donnees sans se preocuper de leure nature.
"""

import re
import socket

from ..tools import Printer
from ..serialization.serialize import serialize
from ..serialization.deserialize import deserialize
from ..serialization.tools import *
from ..errors import *
from . import checks


def send_data(s, data):
    """
    |====================|
    | Envoi des donnees. |
    |====================|

    Ne fait pas de verifications sur les entrees car
    cette fonction n'est pas destinee a l'utilisateur
    mais aux devlopeurs et aux autres fonctions.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param data: Les donnee serialises a envoyer.
    :type data: generator
    """
    with Printer("Sending datas...") as p:
        # Les donnees sont concatenee en gros paquets
        # pour que les protocoles de couches plus basse
        # puissent decouper les donnees comme il le shouaite.
        # Des fanions sont ajoutes de facon a ce que l'on puisse
        # envoyer plusieurs messages consecutif sans qu'ils ne
        # se melangent.
        for is_end, pack in anticipate(concat_gen(to_gen(gen=data))):
            tag = size_to_tag(len(pack)) # Cela permet a la reception de ne pas depasser sur le paque suivant.
            p.show("data: %s %s %s" % (bytes([is_end]), tag, pack))
            s.sendall(bytes([is_end]) + tag + pack)

def send_object(s, obj):
    """
    |========================|
    | Envoi un objet python. |
    |========================|

    Ne fait pas de verifications sur les entrees car
    cette fonction n'est pas destinee a l'utilisateur
    mais aux developeurs et aux autres fonctions.

    Fonctione de la meme facon que 'send_data'.
    N'est efficace que pour le petits objets. Si les
    objets sont lourd, utilisez 'send_data'.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param obj: Objet python a envoyer.
    :type obj: object
    """
    return send_data(s,
        serialize(
            obj,
            compresslevel=0,
            copy_file=False,
            psw=None,
            authenticity=False,
            parallelization_rate=0))

def send_error(s, message):
    """
    |======================================|
    | Envoi un message d'erreur au client. |
    |======================================|

    Envoi un message d'erreur bien formatter pour pouvoir
    passer les controles a la douane.
    Ferme la connection. Comme ca le client ne peut
    plus nous embeter.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param message: Le message d'erreur a envoyer.
    :type message: str
    """
    assert isinstance(message, str), \
        "Le message d'erreur doit etre une chaine de " \
        "caractere. Pas un %s." % type(message).__name__

    send_object(s, {"type": "error", "message": str(message)}) # Le str() compte car on verifie l'heritage.
    s.shutdown(socket.SHUT_RDWR)
    s.close()

def receive(s, timeout=None):
    """
    |============================================|
    | Reception les donnees et les deserialises. |
    |============================================|

    Deserialise les donnes au fur a mesure qu'elles arrivent.
    S'assure que les donnees aient le bon format.

    Fait deja quelques verifications sur les entrees.
    Si les entree ne sont pas bonne, Le message d'erreur
    est envoye puis la communication est coupee.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :param timeout: Permet de lever une exception si c'est trop long.
    :type timeout: int, float

    sortie
    ------
    :return: L'objet de depart envoye par le socket.
    :rtype: object
    :raises NotCompliantError: Si les donnes recut ne sont pas conformes.
    """
    def recv(s, size, timeout=None, buff_size=8192):
        """
        Recoit des paquets qui bout a bout font exactement
        'size' octets. Retourne en une seule fois.
        """
        default_timeout = s.gettimeout() # Peut renvoyer None si il n'y a pas de timeout.
        s.settimeout(timeout)

        buff = b"" # Buffer, concatenations des donnees.
        while len(buff) < size:
            data = s.recv(min(buff_size, size-len(buff)))
            if not data:
                raise BrokenPipeError("Communication is interrupted.") # ConnectionResetError
            buff += data
        
        s.settimeout(default_timeout)
        return buff

    def recvall(s, timeout):
        """
        Cede les donnes par paquet telle qu'elle sont emises.
        S'arrete des que les donnes du premier envoi sont
        epuise, meme si il y a d'autre envois deriere.
        """
        is_end = False # True des que l'on vient de ceder le dernier paquet.
        while not is_end:
            # Recuperation entete.
            first = recv(s, size=1, timeout=timeout) # Renseigne si c'est le dernier paquet ou pas.
            if first == b"\x01":
                is_end = True
            elif first != b"\x00":
                raise HeaderError(
                    "Les paquets recut doivent commencer par "
                    "b'\\x00' ou b'\\x01'. Pas %s." % first)

            # Recuperation taille.
            try:
                size, _, _ = tag_to_size(gen=(recv(s, size=1, timeout=timeout) for _ in range(11))) # On leve une erreur si ca fait plus de 1 Go.
            except (StopIteration, HeaderError) as e:
                raise NotCompliantError("Heder incorrecte ou incomplete.") from e

            # Recuperations des donnees utiles.
            yield recv(s, size=size, timeout=timeout)

    with Printer("Reception des donnes deserialisee...") as p:
        try:
            answer = deserialize(
                deconcat_gen(gen=recvall(s, timeout)),
                psw=None,
                parallelization_rate=0)
        except Exception as e:
            p.show("Erreur de reception: %s" % e.args)
            send_error(s, "Protocol error: %s" % e.args)
            raise e from e
        verif = checks.check(answer)
        if verif:
            p.show("Erreur detectee: %s" % verif)
            send_error(s, verif)
            raise NotCompliantError(
                "Reponse non conforme et donc suspicieuse.",
                "Cause de la suspicion: %s" % verif)
        return answer
