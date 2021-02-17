#!/usr/bin/env python3

"""
C'est ici qu'il y a les petites fonctions
utiles un peu de partout.
Bref, il y a tout ce qui est partage.
"""

import os
import uuid

from .constants import BUFFER_SIZE, HEADER
from ..tools import temprep
from ..errors import *


def size_to_tag(size):
    r"""
    |=================================================|
    | Cre un fanion qui permet de regrouper n octets. |
    |=================================================|
    
    parametres
    ----------
    :param size: Le nombre d'octets a englober.
    :type size: int

    sortie
    ------
    :return: Les donnees chiffrees.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import size_to_tag
    >>>
    >>> data = b'\x00\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde'
    >>> size_to_tag(len(data)) + data
    b'\x8a\x00\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde'
    >>>
    """    
    # on va decouper ce nbr en base 2**7 pour garder un bit de libre par octet
    binaire_txt = bin(size)[2:]
    binaire_txt = "0"*(-len(binaire_txt) % 7) + binaire_txt # on bourre de 0 afin d'avoir un multiple de 7
    fanion_list = []    # contient les bytes correspondants
    for i in range(len(binaire_txt)//7): # pour chaque sous_packets
        fanion_list.append(sum((int(bit) << j for j, bit in enumerate(binaire_txt[7*i:7*i+7][::-1])))) # on ecrit le nombre en base 7
    fanion_list[-1] += 1 << 7 # on ajoute un drapeau pour dire qu'il n'y a plus rien apres
    return bytes(fanion_list) # on transforme ca en type bytes

def tag_to_size(*, gen=(lambda:(yield from []))(), pack=b""):
    r"""
    |=============================================|
    | Regroupe et retourne un packet d'octets     |
    | prealablement 'fanionne' par 'size_to_tag'. |
    |=============================================|
    
    Leve une StopIteration exception si pack et le generateur sont epuises.
    Leve une HeaderError si les entrees sont incorrectes.
    
    parametres
    ----------
    :param gen: La suite des paquets, generateur de 'bytes'.
    :type gen: iter
    :param pack: Le debut d'une suite d'octet, fanion inclus.
    :type pack: bytes

    sortie
    ------
    :return: (
        La longeur representee par le fanion,
        Le generateur possiblement un peu plus itere,
        'pack' depourvu du fanion.
        )
    :rtype: tuple (int, iter, bytes)

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import *
    >>>
    >>> data1 = b'\x00\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde'
    >>> data2 = b'\xe9\xd1\xb7\x0e\xe6-N4n\xb4'
    >>> ens = size_to_tag(len(data1)) + data1 + data2
    >>> ens
    b'\x8a\x00\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde\xe9\xd1\xb7\x0e\xe6-N4n\xb4'
    >>> tag_to_size(ens, (lambda:(yield b''))())
    (10, <generator object <lambda> at 0x7ff437890350>,
    b'\x00\xb0\xe9\xe3\xd4\xcdv\xaf\xbf\xde\xe9\xd1\xb7\x0e\xe6-N4n\xb4')
    >>>
    """
    gen = iter(gen)
    size = 0        # initialisation
    while 1:        # tant que le fanion n'est pas termine
        if pack:
            octet = pack[0]
            pack = pack[1:]
        else:
            while not pack:
                try:
                    pack = next(gen)
                except (StopIteration, TypeError) as e:
                    if size:
                        raise HeaderError("L'indicateur de longueur de packet n'est pas complet.") from e
                    raise StopIteration from e
            octet, pack = pack[0], pack[1:]
        if octet > 127: # si on arrive a la fin du fanion
            size = (size << 7) + (octet - 128)
            return size, gen, pack
        size = (size << 7) + octet

def to_gen(*, gen=(lambda:(yield from []))(), pack=b"", size=BUFFER_SIZE):
    r"""
    |=============================================|
    | Regroupe les packets cedes par 'gen' afin   |
    | de cedez des packets de longeur normalizee. |
    |=============================================|
    
    Ne fait pas de verifications sur les entrees pour
    une question d'optimisation.

    parametres
    ----------
    :param gen: La suite des paquets, generateur de 'bytes'.
    :type gen: iter
    :param pack: Le debut d'une suite d'octet, fanion inclus.
    :type pack: bytes
    :param size: Taille maximale des paquets retournes.
    :type size: int

    sortie
    ------
    :return: Les packets de taille BUFFER_SIZE.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> import random
    >>> from raisin.serialization.constants import BUFFER_SIZE
    >>> from raisin.serialization.tools import gen_to_gen
    >>>
    >>> l = [b'\x00'*random.randint(0, 2*BUFFER_SIZE) for i in range(5)]
    >>> [len(e) for e in l]
    [6051175, 14551972, 13463655, 7948728, 12289630]
    >>>
    >>> lbis = list(gen_to_gen(iter(l)))
    >>> [len(e) for e in lbis]
    [10485760, 10485760, 10485760, 10485760, 10485760, 1876360]
    >>>
    >>> BUFFER_SIZE
    10485760
    >>>
    """
    for data in gen:
        pack += data
        while len(pack) > size:
            yield pack[:size]
            pack = pack[size:]
    yield pack

def anticipate(frozgen, **kwargs):
    r"""
    |====================================================|
    | Permet de savoir si le packet cede est le dernier. |
    |====================================================|

    parametres
    ----------
    :param frozgen:
        -Generateur de 'longeur' inconnue,
        qui cede des objets de longeur quelquonque.
    :type frozgen: iter
    :param frozpack: Le premier packet de 'frozgen'.
        Ce n'est pas une copie de ce que va commencer par cede 'frozgen'.
        ```
            anticipate(g, frozpack=frozpack)
        <=> anticipate(iter([frozpack] + list(g)))
        ```
    :type frozpack: object

    sortie
    ------
    :return: A chaque iterations cede 2 choses:
        -Un booleen qui vaut True si le packet est le dernier, False sinon.
        -Le packet.
        Si le generateur ced un None, leve un ValueError.
    :rtype: tuple (bool, object)

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import anticipate
    >>>
    >>> gen = [0, "a", 1.5, b'\xff']
    >>> for is_end, e in anticipate(gen):
    ...     print(is_end, e)
    ...
    False 0
    False a
    False 1.5
    True b'\xff'
    >>>
    """
    is_empty = True
    if "frozpack" in kwargs:
        prec = kwargs["frozpack"]
        is_empty = False

    for i, pack in enumerate(frozgen):
        if i == 0 and is_empty:     # si on a pas encore constitue de memoire
            prec = pack             # et bien on fait une boucle a vide
            is_empty = False        # de sorte a s'assurer qu'il y a une memoire
            continue
        yield False, prec           # si par contre il y a une memoire
        prec = pack                 # on cede puis on decale d'un cran

    if not is_empty:
        yield True, pack

def concat_gen(frozgen, *, frozpack=None):
    r"""
    |======================================|
    | Permet de concatener les elements du |
    | generateur de facon reversible.      |
    |======================================|
    
    parametres
    ----------
    :param frozgen: Generateur de 'bytes' inconnue.
    :type frozgen: iter
    :param frozpack: Le premier packet de 'frozgen'.
        Ce n'est pas une copie de ce que va commencer par cede 'frozgen'.
        ```
            concat_gen(g, frozpack=frozpack)
        <=> concat_gen(iter([frozpack] + list(g)))
        ```
    :type frozpack: bytes

    sortie
    ------
    :return: Les elements du generateurs pourvu d'un fanion.
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import concat_gen
    >>>
    >>> gen = (b'\x00'*i for i in range(5))
    >>> b''.join(concat_gen(gen))
    b'\x80\x81\x00\x82\x00\x00\x83\x00\x00\x00\x84\x00\x00\x00\x00'
    >>>
    """
    if frozpack != None:
        yield size_to_tag(len(frozpack)) + frozpack
    for e in frozgen:
        yield size_to_tag(len(e)) + e

def deconcat_gen(*, gen=(lambda:(yield from []))(), pack=b""):
    r"""
    |================================|
    | Retrouve les packets initiaux. |
    |================================|
    
    Leve une ValueError si l'entree n'est pas correcte.
    
    parametres
    ----------
    :param gen:
        La suite des paquets, generateur de 'bytes'.
        Les packets cedes ne doivent pas specialement etre bien regroupes.
        Par contre ils doivents etre dans le bon ordre.
    :type gen: iter
    :param pack:
        pack: Le premier packet de 'gen'.
        Ce n'est pas une copie de ce que va commencer par cede 'gen'.
        ```
            deconcat_gen(g, pack=pack)
        <=> deconcat_gen(iter([pack] + list(g)))
        ```
    :type pack: bytes

    sortie
    ------
    :return: Les packets initialement encapsules..
    :rtype: bytes

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import *
    >>> gen = iter([b'a', b'houla', b'', b'hihi'])
    >>> d = b''.join(concat_gen(gen))
    >>> d
    b'\x81a\x85houla\x80\x84hihi'
    >>> list(deconcat_gen(pack=d))
    [b'a', b'houla', b'', b'hihi']
    >>>
    """
    n_packet = 0
    while 1:
        # recuperation de la longueur
        n_packet += 1
        try:
            size, gen, pack = tag_to_size(gen=gen, pack=pack)
        except ValueError as e:
            raise ValueError("Probleme dans l'entete du packet n°%d." % n_packet) from e
        except StopIteration:
            break

        # extraction du bon nombre de donnees
        while len(pack) < size:
            try:
                pack += next(gen)
            except StopIteration as e:
                raise ValueError(
                    "Le packet n°%d est incomplet.\n" \
                    + "Longeur attendue: %d\n" % size \
                    + "Longeur disponible: %s." % len(pack)) from e

        # on cede les donnees
        yield pack[:size]
        pack = pack[size:]

def get_header(*, gen=(lambda:(yield from []))(), pack=b""):
    """
    |=================================|
    | Extrait et interprete l'entete. |
    |=================================|
    
    Leve une ValueError si l'entete n'est pas correcte.

    parametres
    ----------
    :param gen: Generateur de 'bytes'.
    :type gen: iter
    :param pack: Le premier packet de 'gen'.
        Ce n'est pas une copie de ce que va commencer par cede 'frozgen'.
        ```
            get_header(g, pack=pack)
        <=> get_header(iter([pack] + list(g)))
        ```
    :type pack: bytes

    sortie
    ------
    :return: (
        La signification de l'entete,
        Le generateur possiblement un peu plus itere,
        'pack' depourvu de l'entete.
        )
    :rtype: tuple (str, iter, bytes)

    exemple
    -------
    :Example:
    >>> from raisin.serialization.tools import get_header
    >>>
    >>> data = b'</>small int</>3246510'
    >>> h, g, p = get_header(pack=data)
    >>> h
    'small int'
    >>> p
    b'3246510'
    >>>
    """
    gen = iter(gen)
    size_max = 0 # taille de la plus grosse balise

    # recuperation du premier octet
    while not len(pack):
        try:
            pack += next(gen)
        except StopIteration as e:
            raise ValueError("Impossible de recuperer l'entete d'une chaine vide.") from e
    head = pack[:1]
    for sign, heads in HEADER.items():
        if head == heads[1]:
            return sign, gen, pack[1:]
        size_max = max(size_max, len(heads[0]))

    # recuperation de l'entete totale
    i_end = 6
    while len(pack) < 6 or pack[i_end-3:i_end] != b"</>":
        if i_end < len(pack):
            i_end += 1
            continue
        if len(pack) > size_max:
            raise ValueError("L'entete est trop longue.\n" \
                             + "Elle ne doit pas exceder %d octets.\n" % size_max \
                             + "Le debut de l'entete vaut %s." % pack[:2*size_max])
        try:
            pack += next(gen)
        except StopIteration as e:
            raise ValueError("L'entete n'est pas de la forme b'</>...</>'.\n" \
                             + "Le debut de l'entete vaut %s." % pack[:2*size_max])
    head = pack[:i_end]
    for sign, heads in HEADER.items():
        if head == heads[0]:
            return sign, gen, pack[i_end:]
    raise ValueError("L'entete %s n'est pas connue." % head)

def relocate(frozgen):
    """
    |=========================================================|
    | Epuise un generateur en le transferant dans un fichier. |
    | Cede la meme chose que l'entree mais decharge l'entree  |
    | avant de ceder le premier packet.                       |
    |=========================================================|
    
    parametres
    ----------
    :param frozgen: Generateur de 'bytes' inconnue.
    :type frozgen: iter

    sortie
    ------
    :return: La meme chose que 'frozengen'.
    :rtype: bytes
    """

    total_size = 0  # nbr d'octets en memoire
    tampon = []     # decharge frozgen tant que c'est pas trop gros
    sizes = []      # la taille des elements presents dans le fichier
    for e in frozgen:
        total_size += len(e)
        if total_size <= BUFFER_SIZE: # cas ou tout tient dans la ram
            tampon.append(e)
        else:       # cas ou il faut decharger la ram dans le disque
            if not sizes: # cas ou c'est la goutte qui fait deborder le vase
                f = open(os.path.join(temprep, uuid.uuid4().hex), "wb")
            f.write(e)
            sizes.append(len(e))
    yield from tampon
    if sizes:
        f.close()
        with open(f.name, "rb") as fr:
            for size in sizes:
                yield fr.read(size)
        os.remove(f.name)
