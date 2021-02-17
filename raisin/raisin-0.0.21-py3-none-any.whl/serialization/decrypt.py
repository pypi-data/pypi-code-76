#!/usr/bin/env python3

"""
Dechiffre les donnees avec RSA ou AES.
"""

from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import hashlib
import itertools
import os
import re

import raisin
import raisin.serialization.deserialize as deserialize
from .constants import *
from .tools import *
from ..errors import *
from ..tools import Printer


def decipher(data, *, psw=None):
    r"""
    |================================================|
    | Dechiffre les donnees prealablement chiffrees. |
    |================================================|

    Ne fait aucune verification.
    L'entete doit etre comprise dans 'data'.

    parametres
    ----------
    :param data: Donnees chiffrees.
    :type data: bytes
    :param psw: Le mot de passe ou la clef publique rsa.
    :type psw: str, bytes, None
        str: Dechiffrage AES.
        bytes: Clef privee RSA.
        None: Dechiffrage qui utilise la clef privee de raisin.

    sortie
    ------
    :return: Les donnees dechiffrees.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.serialization.cipher import cipher
    >>> from raisin.serialization.decipher import decipher
    >>>
    >>> mess_ciph = cipher(b"message en clair")
    >>> mess_ciph
    b'\x03\x08\x82\x08\x80:\x8c\xbe=\x07\xe92gy\x8a\x8
        ...
    \xbcr\xe4\xf4\x1a\xa1xr\xedGcF\x0c\xc2\xf4$\xad9H,\xe6\x8e'
    >>> decipher(mess_ciph)
    b'message en clair'
    >>>
    """
    if psw == None:
        import raisin.security
        psw = raisin.security.get_private_key()

    return b"".join(decipher_gen((
        lambda d: (yield d))(data),
        psw=psw))

def decipher_aes(data, passphrase):
    """
    |========================================================|
    | Dechiffre des donnees chiffrees avec l'algorithme AES. |
    |========================================================|

    Ne fait aucune verification sur les entrees.
    L'entete doit faire partie de data.

    parametres
    ----------
    :param data: Donnees chiffrees.
    :type data: bytes
    :param passphrase: Extrait du mot de passe de 32 octets.
    :type passphrase: bytes

    sortie
    ------
    :return: les donnees dechiffrees 
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> import hashlib
    >>> from raisin.serialization.encrypt import cipher_aes
    >>> from raisin.serialization.decrypt import decipher_aes
    >>>
    >>> passphrase = hashlib.blake2s(b'mot de passe', digest_size=32).digest()
    >>> ciph_mes = cipher_aes(b"message en clair", passphrase, 1)
    >>> decipher_aes(ciph_mes, passphrase)
    b'message en clair'
    >>>
    """
    with Printer("Deciphering bloc with AES..."):
        head, gen, data = get_header(pack=data)
        if head != "aes bloc":
            raise ValueError(
                "L'entete n'est pas bonne 'aes bloc' est attendu " \
                + "mais %s est recut." % head)
        data = data + b"".join(gen)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(passphrase, AES.MODE_EAX, nonce)
        try:
            return cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError as e:
            raise PswError("La passphrase n'est pas la bonne.") from e

def decipher_rsa(data, private_key_pem):
    r"""
    |========================================================|
    | Dechiffre des donnees chiffrees avec l'algorithme RSA. |
    |========================================================|

    Ne fait pas de verification sur les entrees.

    parametres
    ----------
    :param data: Donnees chiffrees
    :type data: bytes
    :param private_key_pem: Clef privee serialisee au format PEM.
    :type private_key_pem: bytes

    sortie
    ------
    :return: les donnees dechiffrees 
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.security import rsa_keys
    >>> from raisin.serialization.encrypt import cipher_rsa
    >>> from raisin.serialization.decrypt import decipher_rsa
    >>> priv, pub = rsa_keys()
    >>> ciph_mes = cipher_rsa(b"message en clair", pub, 1)
    >>> ciph_mes
    b'3\x08\x80&\x1d4g\xb7_\xc7\xfd\x9d% ... \xc0\x89\xbaI\xeb\xa28\xa4'
    >>> decipher_rsa(ciph_mes, priv)
    b"message en clair"
    >>>
    """
    with Printer("Deciphering block with RSA..."):
        head, gen, pack = get_header(pack=data)
        if head != "rsa bloc":
            raise ValueError(
                "L'entete n'est pas bonne 'rsa bloc' est attendu " \
                + "mais %s est recut." % head)
        
        try:
            decryptor = PKCS1_OAEP.new(RSA.importKey(private_key_pem))
        except ValueError as e:
            raise DecryptError("La clee privee est chiffree!") from e
        try:
            return b"".join(
                    map(
                        decryptor.decrypt,
                        deconcat_gen(
                            gen=gen,
                            pack=pack
                        )
                    )
                )
        except ValueError as e:
            raise PswError("La clef privee n'est pas la bonne.") from e

def decipher_gen(gen, psw):
    """
    |===========================================|
    | Dechiffre sequentiellement chaque packets |
    | cedes par le generateur en les regroupant |
    | tel qu'ils etaient avant.                 |
    |===========================================|

    parametres
    ----------
    :param gen: Generateur qui cede des 'bytes'.
    :type gen: iter
    :param psw: Le mot de passe ou la clef publique rsa.
    :type psw: str, bytes, None
        str: Dechiffrage rapide avec AES.
        bytes: Clef privee RSA.

    sortie
    ------
    :return: Les donnees dechiffrees.
    :rtype: iter

    exemple
    -------
    :Example:
    >>> import uuid
    >>> from raisin.serialization.encrypt import cipher_gen
    >>> from raisin.serialization.decrypt import decipher_gen
    >>>
    >>> gen1 = [uuid.uuid4().bytes for i in range(10)]
    >>> gen2 = cipher_generator(gen1)
    >>> gen3 = decipher_generator(gen2)
    >>>
    >>> all([a == b for a, b in zip(gen1, gen3)])
    True
    >>>
    """
    with Printer("Deciphering generator..."):
        head, gen, pack = get_header(gen=gen)
        fini = True
        if head == "aes bloc":
            yield decipher_aes(
                HEADER[head][1] + pack + b"".join(gen),
                passphrase=psw)
        elif head == "rsa bloc":
            yield decipher_rsa(
                HEADER[head][1] + pack + b"".join(gen),
                private_key_pem=psw)
        elif head == "aes sel":
            if psw == None:
                raise DecryptError("Je ne peux pas dechiffrer sans mot de passe!")
            pack = pack + b"".join(gen)
            sel, pack = pack[:32], pack[32:]
            yield decipher_aes(
                pack,
                passphrase=hashlib.blake2s(
                    sel + psw.encode("utf-8"),
                    digest_size=32
                    ).digest()
                )
        elif head == "aes gen":
            if psw == None:
                raise DecryptError("Je ne peux pas dechiffrer sans mot de passe!")
            while len(pack) < 32:
                pack += next(gen)
            sel, pack = pack[:32], pack[32:]
            hash_ = hashlib.sha512(sel + psw.encode("utf-8")).digest()
            passphrases = [hash_[:32], hash_[32:]]
            fini = False
        elif head == "rsa gen":
            size, gen, pack = tag_to_size(gen=gen, pack=pack)
            while len(pack) < size:
                pack += next(gen)
            hash_, pack = decipher_rsa(
                pack[:size],
                private_key_pem=psw), \
                pack[size:]
            passphrases = [hash_[32*i:32*(i+1)] for i in range(len(hash_)//32)]
            fini = False
        else:
            raise ValueError(
                "L'entete n'est pas correcte. Elle vaut %s." % head)

        if not fini:
            for i, pack in enumerate(deconcat_gen(gen=gen, pack=pack)):
                yield decipher_aes(
                    pack,
                    passphrase=passphrases[i%len(passphrases)])

def _decipher_file(filename, **kwargs):
    """
    |=======================|
    | Dechiffre un fichier. |
    |=======================|
    
    Supprime l'ancien fichier pour ne laisser
    que le nouveau fichier dechiffre.
    Ne fait aucune verifcation sur les entrees.

    parametres
    ----------
    :param filename: Le nom d'un fichier ou son chemin.
    :type filename: str
    
    Les autres arguments sont les memes que
    ceux de la fonction 'decipher_gen'.

    sortie
    ------
    :return: Le nom du fichier dechiffre.
    :rtype: str

    exemple
    -------
    :Example:
    >>> from raisin.security.decrypt import _decipher_file
    >>> _decipher_file("monfichier.txt.crsn")
    'monfichier.txt'
    >>>
    """
    def generator(filename):
        """
        Cede filename par bout de BUFFER_SIZE.
        """
        with open(filename, "rb") as f:
            while 1:
                pack = f.read(BUFFER_SIZE)
                if pack == b"":
                    break
                yield pack
    
    with Printer("Decryption of the file %s..." % repr(filename)):
        if filename.endswith(".crsn"):
            new_file = filename[:-5]
        else:
            new_file = "deciphered_" + filename
        try:
            with open(new_file, "wb") as f:
                for pack in decipher_gen(
                        generator(filename),
                        **kwargs):
                    f.write(pack)
        except Exception as e:
            if os.path.exists(new_file):
                os.remove(new_file)
            raise e from e
        else:
            os.remove(filename)
        return new_file

def authenticity(gen):
    """
    |=============================================|
    | S'assure que le generateur est authentique. |
    |=============================================|

    L'entete doit etre presente dans 'gen'.

    parametres
    ----------
    :param generator: Generateur qui cede des 'bytes'.
    :type generator: iter

    sortie
    ------
    :return: Les donnees initiales.
    :rtype: <type generator>
    """
    with Printer("Verify authenticity..."):
        head, gen, pack = get_header(gen=gen)
        if head != "authenticity":
            raise ValueError(
                "L'entete n'est pas correcte. Elle vaut %s. " % head \
                + "Or 'authenticity' est attendu.")
        
        hash_ = b""
        for is_end, pack in anticipate(deconcat_gen(gen=gen, pack=pack)):
            if is_end:
                if hash_ != pack:
                    raise AuthenticityError("Les donnees ne sont pas authentiques!")
                break
            hash_ = hashlib.sha512(hash_ + pack).digest()
            yield pack
