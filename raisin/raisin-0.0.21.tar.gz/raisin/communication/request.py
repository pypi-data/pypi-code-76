#!/usr/bin/env python3

"""
|============================|
| Permet de poser des        |
| petites questions simples. |
|============================|

Permet de poser des questions simple parmis un pannel
de question et de recuperer la reponse. Toutes les
verifications sont faites de sorte a rendre
ces fonctions le plus autonome possible.

Instancie un rotocole de communication haut niveau,
faisant abstraction de la couche phisique. C'est la partie
qui traite les requettes ou met en forme les requettes
a envoyer.
"""

import socket
import uuid

from . import checks, routing
from ..tools import Printer, identity
from ..errors import *


def ask_challenge(s, public_key):
    """
    |====================|
    | Envoi un chalenge. |
    |====================|

    En cas d'echec, le message d'erreur est envoye au correpondant.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    :public_key: Clef publique du correspondant au format PEM.
    :type public_key: str

    sortie
    ------
    :return: True si le challenge est reussi.
        False si le chalenge n'est pas resolu dans le temps imparti.
    :rtype: boolean
    """
    with Printer("Sending a challenge...") as p:
        # On l'importe ici car c'est le seul
        # endroit ou c'est utilise et c'est pas systematique.
        import raisin.serialization.encrypt as encrypt
        challenge = uuid.uuid4().hex   # Creation aleatoire d'une phrase.
        question = {  
            "type": "question",
            "question": "challenge",
            "description": encrypt.cipher(
                bytes.fromhex(challenge),
                psw=public_key).hex()}
        del encrypt # On relibere la memoire.
        routing.send_object(s, question) # On demande au client de la dechiffrer.
        try:
            answer_challenge = routing.receive(s, timeout=30)
        except socket.timeout:
            p.show("Correspondent expelled because he is too slow to try the challenge.")
            routing.send_error(s, "You are too slow to try the challenge.")
            return False
        except NotCompliantError:
            p.show("Correspondent expelled because he is threatening.")
            return False # Le message d'erreur est deja envoye depuis 'receive'.
        error = checks.check_coherence(answer_challenge, question)
        if error:
            p.show("Correspondent expelled because he is off the mark.")
            routing.send_error(s, error)
            return False
        if answer_challenge["challenge"] != challenge:
            p.show("Correspondent expelled because he failed to meet the challenge.")
            routing.send_error(s, "You failed to meet the challenge.")
            return False
        return True

def ask_identity(s):
    """
    |===============================|
    | Recupere l'identitee complete |
    | du correspondant.             |
    |===============================|

    En cas d'echec, le message d'erreur est envoye au correpondant.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket

    sortie
    ------
    :return: L'identitee du corespondant.
        En cas d'echec, un dictionaire vide est renvoye.
    :rtype: dict
    """
    with Printer("Ask for full identity...") as p:
        question = {"type": "question", "question": "identity",
            "description": "How are you?"}
        routing.send_object(s, question)
        try:
            identity = routing.receive(s, timeout=60)
        except socket.timeout:
            p.show("Correspondent expelled because he is too slow to give his identity.")
            routing.send_error(s, "You are too slow to give your identity.")
            return {}
        except NotCompliantError:
            p.show("Correspondent expelled because he is threatening.")
            return {} # Le message d'erreur est deja envoye depuis 'receive'.
        error = checks.check_coherence(identity, question)
        if error:
            p.show("Correspondent expelled because he is off the mark.")
            routing.send_error(s, error)
            return {}
        return identity["identity"]

def ask_public_key(s):
    """
    |============================|
    | Recupere la clef           |
    | publique du correspondant. |
    |============================|

    En cas d'echec, le message d'erreur est envoye au correpondant.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket

    sortie
    ------
    :return: La clef publique du correspondant au format PEM.
        En cas d'echec, une chaine vide est retournee.
    :rtype: str
    """
    with Printer("Ask for public_key...") as p:
        question = {"type": "question", "question": "public_key", "description": "What is your public key?"}
        routing.send_object(s, question)
        try:
            public_key = routing.receive(s, timeout=30)
        except socket.timeout:
            p.show("Correspondent expelled because he is too slow to give his public key.")
            routing.send_error(s, "You are too slow to give your public key.")
            return ""
        except NotCompliantError:
            p.show("Correspondent expelled because he is threatening.")
            return "" # Le message d'erreur est deja envoye depuis 'receive'.
        error = checks.check_coherence(public_key, question)
        if error:
            p.show("Correspondent expelled because he is off the mark.")
            routing.send_error(s, error)
            return ""
        return public_key["public_key"]

def send_welcome(s):
    """
    |========================|
    | Shouaite la bienvenue. |
    |========================|

    Envoi un message de bienvenu au correspondant,
    souvent un client. C'est pour dire au client
    qu'il a reussi tous les tests et que la
    connection est bien etablie.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    """
    routing.send_object(s,
        {"type": "info", "welcome": "I am now at your disposal"})

def send_mac(s):
    """
    |======================|
    | Envoi l'adresse mac. |
    |======================|

    Envoi l'adresse mac local de facon a dire au
    serveur qui il est.

    entree
    ------
    :param s: Socket tcp du client ou du serveur
        avec qui la connection est etablie.
    :type s: socket.socket
    """
    routing.send_object(s,
        {"type": "info", "mac": identity["mac"]})

def answering(request):
    """
    |========================|
    | Repond a une requette. |
    |========================|

    entree
    ------
    :param request: La requette deserialise et verifiee au maximum.
        La requete est recuperee via 'routing.receive'.
    :type request: dict

    sortie
    ------
    :return: La reponse a la requette.
    :rtype: dict
    """
    if request["type"] == "question":        
        if request["question"] == "identity":
            return {"type": "answer", "question": "identity",
                    "identity": dict(identity)}
        
        if request["question"] == "challenge":
            import raisin.serialization.decrypt as decrypt
            try:
                return {"type": "answer", "question": "challenge",
                        "challenge": decrypt.decipher(bytes.fromhex(request["description"])).hex()}
            except DecryptError:
                return {"type": "error", "message": "Challenge trop difficile."}
            finally:
                del decrypt

        if request["question"] == "public_key":
            import raisin.application.settings as settings
            return {"type": "answer", "question": "public_key",
                    "public_key": settings.settings["account"]["security"]["public_key"]}

    return {"type": "error", "message": "incomprehensible request."}
