#!/usr/bin/env python3

"""
Chiffre les donnees avec AES et RSA.
"""

from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import hashlib
import itertools
import os
import re
import secrets

import raisin
from .constants import *
from .tools import *
import raisin.serialization.serialize as serialize
from ..tools import Printer


def cipher(data, *, psw=None, compact=1):
    r"""
    |===============================================|
    | Chiffre Les donnees avec l'algotithme adapte. |
    |===============================================|

    Compatible avec decipher et decipher_generator.
    Ne fait aucune verification.
    
    parametres
    ----------
    :param data: Les donnees a chiffrer.
    :type data: bytes
    :param psw: Le mot de passe ou la clef publique rsa.
    :type psw: str, bytes, None
        str: Chiffrage rapide avec AES.
        bytes: Clef publique RSA, Chiffrement lent.
        None: Chiffrage qui utilise la clef publique de raisin.
    :param compact: Determine si les objets serializes.
        doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.

    sortie
    ------
    :return: Les donnees chiffrees.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.serialization.cipher import cipher
    >>>
    >>> cipher(b"message en clair", psw="mot de passe")
    b'\x02\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde"\xda\xf6@
    \x04\x0fr\x1f\n-Om\x9a\x1e\x03AN\x15\r\x8ei\xbc\xac
    \xe9\xd1\xb7\x0e\xe6-N4n\xb4\x89\x12h.\xfc\xee\xb6'
    >>>
    """
    if psw == None:
        import raisin.application.settings as settings
        psw = settings.settings["account"]["security"]["public_key"]
        del settings

    with Printer("Ciphering datas..."):
        return b"".join(cipher_gen(
            to_gen(pack=data),
            psw=psw,
            compact=compact
            ))

def cipher_aes(data, passphrase, compact):
    r"""
    |============================================|
    | Chiffre des donnees avec l'algorithme AES. |
    |============================================|

    Ne fait aucune verifications sur les entrees.

    parametres
    ----------
    :param data: Donnees brute non chifrees.
    :type data: bytes
    :param passphrase: Sorte de mot de passe sur 32 octets.
    :type passphrase: bytes
    :param compact: Determine si les objets serializes.
        doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.

    sortie
    ------
    :return: les donnees chifrees.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> import hashlib
    >>> from raisin.serialization.cipher import cipher_aes
    >>>
    >>> passphrase = hashlib.blake2s(b'mot de passe', digest_size=32).digest()
    >>> cipher_aes(b"message en clair", passphrase)
    b"oz4\x0bE\xeaD\xb5\x8d\x87\xads\xcf\x96\xaa\xeb
    \xce ?\x10)\xd2\xf6'\xe1\xcfk*\x06\x1a\xe8b\xe2<
    \x15%\x9d\xb9}7\xa8\xe02j\xab\x04\x97\x94"
    >>>
    """
    with Printer("Ciphering bloc with AES..."):
        cipher = AES.new(passphrase, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return HEADER["aes bloc"][compact] + cipher.nonce + tag + ciphertext

def cipher_rsa(data, public_key_pem, compact):
    r"""
    |============================================|
    | Chiffre des donnees avec l'algorithme RSA. |
    |============================================|
    
    Attention, les donnees chiffrees prennent 2 fois plus de place.
    N'effectue pas de verifications sur les entrees.

    parametres
    ----------
    :param data: Donnees brute non chiffrees.
    :type data: bytes
    :param public_key_pem: Clef publique serialisee au format PEM.
        La clef doit etre dechifree.
    :type public_key_pem: bytes
    :param compact: Determine si les objets serializes.
        doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.

    sortie
    ------
    :return: les donnees chiffrees 
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.security import rsa_keys
    >>> from raisin.serialization.cipher import cipher_rsa
    >>> priv, pub = rsa_keys()
    >>> cipher_rsa(b"message en clair", pub)
    b'\x08\x80B+\xc3"\xe9z\x07 ... \x89\xaf\xfe\xfd0\xf1\x87'
    >>>
    """
    with Printer("Ciphering bloc with RSA..."):
        encryptor = PKCS1_OAEP.new(RSA.importKey(public_key_pem)) # deserialisation de la clef RSA
        return HEADER["rsa bloc"][compact] + b"".join(
            concat_gen([
                encryptor.encrypt(data[i:i+500])
                for i in range(0, len(data), 500)
                ])
            )

def cipher_gen(gen, psw, compact):
    r"""
    |=============================================|
    | Chiffre sequentiellement chaque packets     |
    | cedes par le generateur sans les regrouper. |
    |=============================================|
    
    Ne fait pas de verification sur les entrees.
    L'interet de ce generateur est de pouvoir chiffrer
    de grosses donnees sans surcharger la RAM. Les donnees
    sont chiffrees a mesure qu'elles defilent.
    Ces paquets peuvent etre gros, plusieurs Mo.

    parametres
    ----------
    :param generator: Generateur qui cede des 'bytes'.
    :type generator: iter
    :param psw: Le mot de passe ou la clef publique rsa.
    :type psw: str, bytes, None
        str: Chiffrage rapide avec AES.
        bytes: Clef publique RSA, Chiffrement lent.
    :param compact: Determine si les objets serializes.
        doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.

    sortie
    ------
    :return: Les donnees Chiffrees.
    :rtype: iter

    exemple
    -------
    :Example:
    >>> import uuid
    >>> from raisin.serialization.cipher import cipher_generator
    >>>
    >>> gen = (uuid.uuid4().bytes for i in range(3))
    >>> for d in cipher_generator(gen):
    ...     print(d)
    ...
    b'\x03\x08\x82\x08\x80\x8d\xb ...
    b"\xb0\xb3J*~\xfc-+\x1 ...
    b"\xb0c\x0fsbT,\xd36\xfeJ ...
    >>>
    """
    with Printer("Ciphering generator..."):
        for i, (is_end, data) in enumerate(anticipate(to_gen(gen=gen))):
            if i == 0 and is_end and len(data) <= 500: # Dans le cas ou l'on a pas grand chose a chiffrer.
                if isinstance(psw, str):
                    sel = secrets.token_bytes(32) # Rend difficile l'attaque d'arc en ciel.
                    passphrase = hashlib.blake2s(
                        sel + psw.encode("utf-8"),
                        digest_size=32
                        ).digest()
                    yield HEADER["aes sel"][compact] \
                        + sel \
                        + cipher_aes(data, passphrase, compact)
                else:
                    yield cipher_rsa(data, psw, compact)
                break
            elif i == 0: 
                if isinstance(psw, str): # Beaucoup a faire en AES.
                    sel = secrets.token_bytes(32) # Sel contre l'arc en ciel.
                    hash_ = hashlib.sha512(sel + psw.encode("utf-8")).digest()
                    passphrases = [hash_[:32], hash_[32:]]
                    yield HEADER["aes gen"][compact] + sel
                else: # Si on doit faire beaucoup en RSA.
                    passphrases = [secrets.token_bytes(32) for _ in range(500//32)]
                    yield HEADER["rsa gen"][compact] + b"".join(
                        concat_gen(
                            frozgen=[cipher_rsa(b"".join(passphrases), psw, compact)]
                            )
                        )
            ciphdata = cipher_aes(data, passphrases[i%len(passphrases)], compact)
            yield size_to_tag(len(ciphdata)) + ciphdata

def _cipher_file(filename, **kwargs):
    """
    |=====================|
    | Chiffre un fichier. |
    |=====================|

    Supprime l'ancien fichier pour ne laisser que le nouveau.
    Ne fait aucune veriication sur les donnees d'entrees.

    parametres
    ----------
    :param filename: Le nom d'un fichier ou son chemin.
    :type filename: str
    
    Les autres arguments sont les memes que
    ceux de la fonction 'cipher_gen'.

    sortie
    ------
    :return: Le nom du fichier chiffre.
    :rtype: str

    exemple
    -------
    :Example:
    >>> from raisin.security.encrypt import _cipher_file
    >>> _cipher_file("monfichier.txt")
    'monfichier.txt.crsn'
    >>>
    """
    def generator(filename):
        """
        Cede filename par petits bouts.
        """
        with open(filename, "rb") as f:
            while True:
                pack = f.read(BUFFER_SIZE)
                if pack == b"":
                    break
                yield pack
    
    with Printer("Encryption of the file %s..." % repr(filename)):
        new_file = filename + ".crsn"
        # while os.path.exists(new_file):
        #     new_file = new_file[:-5] + "_bis.crsn"
        try:
            with open(new_file, "wb") as f:
                for pack in cipher_gen(
                        generator(filename),
                        **kwargs):
                    f.write(pack)
            os.remove(filename)
        except Exception as e:
            if os.path.exists(new_file):
                os.remove(new_file)
            raise e from e
        return new_file

def authenticity(gen, compact):
    """
    |==============================================|
    | Calcul est ajoute un hash au contenu de gen. |
    |==============================================|

    Ne fait aucune verifications sur les entrees.

    parametres
    ----------
    :param generator: Generateur qui cede des 'bytes'.
    :type generator: iter
    :param compact: Determine si les objets serializes.
        doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.

    sortie
    ------
    :return: Les donnes d'entree suivi du hash
        permetant d'assurer l'authencicite du generateur.
    :rtype: <type generator>
    """
    hash_ = b""
    with Printer("Put authenticity..."):
        yield HEADER["authenticity"][compact]
        for pack in to_gen(gen=gen):
            hash_ = hashlib.sha512(hash_ + pack).digest()
            yield size_to_tag(len(pack)) + pack
        yield size_to_tag(len(hash_)) + hash_

