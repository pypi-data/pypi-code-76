#!/usr/bin/env python3

"""
Permet de generer des clefs et de chiffrer / dechiffrer des donnees.
"""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, AES
import hashlib
import itertools
import os
import re
import secrets
import time
import uuid

from .application.settings import settings
from .application.hmi.dialog import question_reponse
import raisin.serialization.encrypt as encrypt
import raisin.serialization.decrypt as decrypt
from .tools import Printer


def rsa_keys(*, psw=None):
    r"""
    |===============================|
    | Genere une paire de clef RSA. |
    |===============================|

    parametres
    ----------
    :param psw: Permet de chiffrer la clef privee
    :type psw: str, None
        str: Est utilise comme codage symetrique.
        None: Ne chiffre rien du tout

    sortie
    ------
    :return: La clef privee suivie de la clef publique.
    :rtype: (bytes, bytes)

    exemple
    -------
    :Example:
    >>> from raisin.security import rsa_keys
    >>> rsa_keys()
    (b'-----BEGIN RSA PRIVATE KEY-----\nMIISKAIBAAK
    CBAEAk7rtT6a4lnBnpq0lStYuxzf7EGkDBIkW4YQGlisAuL
        ...
    42CYcXHQDymViYDtBLEkYSy9oIKUtgreb9M6sTVm1DgJBaC
    gInWOzU=\n-----END RSA PRIVATE KEY-----',
    b'-----BEGIN PUBLIC KEY-----\nMIIEIjANBgkqhkiG9
    w0BAQEFAAOCBA8AMIIECgKCBAEAk7rtT6a4lnBnpq0lStYu
        ...
    Ov9NLuUY5dS90iunJkV85zq9rBrLJvQKloLYhotULt\ngQI
    DAQAB\n-----END PUBLIC KEY-----')
    >>>
    """
    assert psw is None or isinstance(psw, str), \
        "Le mot de passe doit etre soit None, soit une "\
        +"chaine de caractere, pas un %s." % type(psw).__name__
    assert psw != "", "'psw' ne doit pas etre une chaine vide."
    
    with Printer("Generation of RSA keys (it can may a time)..."):
        private_key = RSA.generate(1<<13)
        if psw:
            private_key_serialisee = private_key.exportKey("PEM", passphrase=psw.encode("utf-8"))
        else:
            private_key_serialisee = private_key.exportKey("PEM")
        public_key = private_key.publickey()
        public_key_serialisee = public_key.exportKey("PEM")

        return private_key_serialisee, public_key_serialisee

def change_private_key(private_key_pem, old_psw, new_psw):
    """
    |====================================================|
    | Change le mot de passe qui protege la clef privee. |
    |====================================================|

    parametres
    ----------
    :param private_key_pem: Clef privee serialisee au format PEM.
    :type private_key_pem: bytes
    :param old_psw: Mot de passe qui protege actuellement la clef privee.
    :type old_psw: str, None
        str: Utilise le mot de passe pour dechiffrer la clef.
        None: La clef n'est pas chifree.
    :param new_psw: Nouveau mot de passe qui va bientot proteger la clef privee.
    :type new_psw: str, None
        str: La nouvelle clef va etre chiffree.
        None: Ne chiffre rien du tout.

    sortie
    ------
    :return: La clef privee reserialisee
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.security import rsa_keys, change_private_key
    >>> priv, pub = rsa_keys()
    >>> priv = change_private_key(priv, None, "mot de passe")
    >>>
    """
    assert type(private_key_pem) is bytes,\
        "La clef privee doit etre de type 'bytes', pas %s." % type(private_key_pem)
    assert re.search(r"-----BEGIN RSA PRIVATE KEY-----(.|\n)+-----END RSA PRIVATE KEY-----",
        private_key_pem.decode()),\
        "La clef privee n'est pas au format 'PEM'."
    assert old_psw is None or type(old_psw) is str,\
        "L'ancien mot de passe doit etre soit None, soit une chaine de caractere, pas un %s." % type(old_psw)
    assert new_psw is None or type(new_psw) is str,\
        "Le nouveau mot de passe doit etre soit None, soit une chaine de caractere, pas un %s." % type(new_psw)

    if old_psw == None and new_psw == None:
        return private_key_pem
    elif new_psw == None:
        sentence = "Decipher the privated key..."
    elif old_psw == None:
        sentence = "Cipher the private key..."
    else:
        sentence = "Change the private key's password..."
    with Printer(sentence):
        return RSA.importKey(
            private_key_pem,
            passphrase=old_psw.encode("utf-8") if old_psw else None
            ).exportKey(
                "PEM",
                passphrase=new_psw.encode("utf-8") if new_psw else None
                )

def get_private_key(*, force=False):
    r"""
    |======================================|
    | Recupere la clef privee de raisin.   |
    | Si elle n'existe pas, elle est cree. |
    | La clef retournee est dechiffree.    |
    |======================================|

    parametres
    ----------
    :param force: Si la clef est chiffrer, le mot de passe est
        dans tous les cas demande a l'utilisateur.
    :type force: bool

    sortie
    ------
    :return: la clef privee serialisee au format PEM.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.security import get_private_key
    >>> get_private_key()
    b'-----BEGIN RSA PRIVATE KEY-----\nMIISJwIBAAKCBAEA2ZNhutNMYZ1B
        ...
    XX4fIHm7SNLPest13niyDEGGEI/lg==\n-----END RSA PRIVATE KEY-----'
    >>>
    """
    assert isinstance(force, bool), \
        "'force' doit etre un booleen, pas %s." % type(force).__name__

    with Printer("Recuperation de la clef privee raisin..."):
        import raisin.application.settings as settings
        psw = request_psw(force=force, check=False)
        key_pem = settings.settings["account"]["security"]["private_key"]
        return change_private_key(key_pem, psw, None)

def change_psw(*, existing_window=None, save_dico=settings):
    """
    Change le mot de passe de raisin.

    entree
    ------
    :param save_dico: Dictionaire dans lequel on viens lire
        et ecrire les nouvelle informations.
    :type save_dico: dict

    sortie
    ------
    :return: La partie security.
    :rtype: dict
    """
    with Printer("Change the raisin security parameters..."):
        import raisin.application.hmi.psw as psw
        old_psw = request_psw(force=True)
        new_psw, sentence_memory, clair = psw.get_new_psw(existing_window=existing_window)
        sel = secrets.token_bytes(32)
        save_dico["account"]["security"]["sentence_memory"] = sentence_memory
        save_dico["account"]["security"]["private_key"] = change_private_key(
            save_dico["account"]["security"]["private_key"],
            old_psw,
            new_psw)
        if clair:
            save_dico["account"]["security"]["psw"] = new_psw
        else:
            save_dico["account"]["security"]["psw"] = None
        save_dico["account"]["security"]["sel"] = sel
        if new_psw:
            save_dico["account"]["security"]["hash"] = hashlib.sha512(sel + new_psw.encode("utf-8")).hexdigest()
        else:
            save_dico["account"]["security"]["hash"] = None
        if old_psw != new_psw:
            request_psw.time = 0 # Pour eviter d'utiliser le mauvais mot de passe
        return save_dico["account"]["security"]

class PswRequester:
    """
    Demande le mot de passe a l'utilisateur.
    """
    def __init__(self):
        self.psw = None # Le dernier mot de passe entre.
        self.time = 0   # La derniere date ou ce mot de passe a ete saisi.

    def __call__(self, force, *, message="", check=True, existing_window=None, signature=None):
        """
        |=====================================|
        | Recupere le mot de passe de raisin. |
        | Demande a l'utilisateur si besoin.  |
        |=====================================|

        parametres
        ----------
        :param force: Permet d'eviter de constament soliciter l'utilisateur.
        :type force: bool
            True: Demande le mot de passe a l'utilisateur. Meme si il est connu.
            False: Evite dans la mesure du possible de soliciter l'utilisateur.
        :param message: C'est une indication qui precise pourquoi on demande le mot de passe.
        :type message: bool
        :param check: Permet d'etre tres vigilant.
        :type check: bool
            True: S'assure que les clefs privees et publiques vont bien ensembles.
            False: Se contente de comparer les hash des mot de passe.
        :param existing_window: Permet de mieu gerer la nouvelle fenetre tkinter de dialogue.
        :param signature: N'importe quel objet qui permet d'afficher
            dans la bonne colone du terminal.

        sortie
        ------
        :return: Le mot de passe en clair.
        :rtype: str, None
        """
        def validate(security, psw=None):
            """
            Retourne True si les parametres sont coherent, False sinon.
            """
            if not psw:
                psw = security["psw"]
            if b"ENCRYPTED" in security["private_key"]:
                if not psw:
                    return False
                if hashlib.sha512(
                        security["sel"] + psw.encode("utf-8")
                        ).hexdigest() != security["hash"]:
                    return False
            test = uuid.uuid4().bytes
            try:
                if decrypt.decipher_rsa(
                        encrypt.cipher_rsa(
                            test,
                            security["public_key"],
                            1),
                        change_private_key(
                            security["private_key"],
                            psw,
                            None)
                        ) != test:
                    return False
            except KeyboardInterrupt as e:
                raise e from e
            except decrypt.DecryptError:
                return False
            return True

        # verifications
        assert type(force) is bool
        assert type(message) is str
        assert type(check) is bool

        security = settings["account"]["security"]
        
        # Les cas ou l'on peu eviter de poser la question.
        if (security["psw"] and not force) or (b"ENCRYPTED" not in security["private_key"]):
            if check:
                if not validate(security):
                    raise ValueError("Il y a une incoherence dans les parametres du mot de passe.")
            return security["psw"]                      # on le retourne tel qu'il est

        # si il a deja ete saisie il a moins d'une heure
        if self.psw and time.time() - self.time < 3600:
            if check:
                if not validate(security, self.psw):
                    raise ValueError("Il y a un probleme dans les parametres du mot de passe.")
            self.time = time.time()
            return self.psw                     # on le renvoi sans poser trop de questions

        # cas ou il faut poser la question
        validatecommand = lambda psw : validate(security, psw)
        surplus = '"%s\n"' % message if message else ""
        indication = " (%s)" % security["sentence_memory"] if security["sentence_memory"] else ""
        psw = question_reponse(
            "%sPlease enter the 'raisin' password%s:" % (surplus, indication),
            default=None,
            validatecommand=validatecommand,
            existing_window=existing_window,
            show="*")
        self.psw = psw
        self.time = time.time()
        return psw

request_psw = PswRequester() # permet de garder en memoire le mot de passe
