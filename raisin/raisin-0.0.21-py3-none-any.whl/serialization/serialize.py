#!/usr/bin/env python3

"""
Serialise des objets pour les rendre transportables
"""

import cloudpickle
import inspect
import io
import itertools
import json
import os
import struct
import sys

from .constants import *
from .tools import *
from ..tools import Printer


def dumps(gen):
    """
    |===========================================|
    | Met sous forme de chaine de caractere les |
    | donnees serialisee par 'serialize'.       |
    |===========================================|

    Ne fait aucune verifications sur l'entree.
    Regroupe N_BYTES octets en N_SYMB caracteres ou
    bien 3 octets en 4 caracteres celon ce qui permet
    de compacter au mieux le resultat.

    parametres
    ----------
    :param gen: Generateur provenant directement de 'serialize'.
        Il ne doit pas etre vide ni epuise.
    :type gen: <class 'generator'>

    sortie
    ------
    :return: Une chaine de caractere contenant les objets serializes.
    :rtype: str
    """
    def anticipate_var(pack, size):
        """
        Generator qui cede des packets de 'size' octets.
        Cede aussi un booleen qui annonce l'arrive du dernier packet.
        """
        div, rest = divmod(len(pack), size)
        final = div + 1 if rest else div # ceil(pack/size)
        for i in range(final):
            yield (i+1 == final), pack[size*i:size*(i+1)]

    def int_to_alph(i, n_symb, n1):
        """
        Converti un entier en une chaine
        constitue par des symboles de l'alphabet.
        contraintes:
            i <= n1**n_symb
            retourne n_symb caracteres
        """
        chaine = ""
        while i:
            i, r = divmod(i, n1)
            chaine = ALPHABET[r] + chaine
        chaine = ALPHABET[0]*(n_symb-len(chaine)) + chaine
        return chaine

    def pack_to_int(pack):
        """
        Converti une chaine binaire en un entier.
        """
        return int.from_bytes(pack, byteorder="big", signed=False)

    # preparation (n1**n_symb >= n2**n_bytes)
    pack = b"".join(gen)
    if len(pack) < N_BYTES*3/4: # Si il vaut mieu ne pas faire des packets trop gros.
        sortie = HEADER["small dumps"][1].decode()
        n1 = 64 # Nbr de caracteres differents.
        n_bytes = 3 # C'est le nombre d'octet que l'on regroupe.
        n_symb = 4 # On converti 3 octets en 4 caracteres.
    else:
        sortie = HEADER["large dumps"][1].decode()
        n1 = len(ALPHABET) # Nbr de caracteres differents.
        n_bytes = N_BYTES # C'est le nombre d'octet que l'on regroupe.
        n_symb = N_SYMB # Regroupe N_BYTES octets en N_SYMB caracteres.

    # convertion
    for is_end, pack in anticipate_var(pack, n_bytes):
        sortie += int_to_alph(
            pack_to_int(pack),
            n_symb,
            n1)
        if is_end and len(pack) < n_bytes:
            return sortie + ALPHABET[len(pack)]
    return sortie

def serialize(obj, **kwargs):
    """
    |====================================================|
    | Serialise, compresse et encrypt tous type d'objet. |
    |====================================================|

    Ne fait aucune verifications des entrees.
    Tous les parametres doivent etre specifies.

    parametres
    ----------
    :param obj:
        N'importe quel type d'objet python, celui a serialiser.
    :type obj: object
    :param compresslevel:
        Permet de compresser sans perte le resultat.
    :type compresslevel: int
        -1: Intelligente, compresse au mieu
            en fonction du debit demande.
            Si 'parallelization_rate' >= 0
        0: Pas de compression du tout.
        1: Choisi un encodage moins lisible par
           l'humain mais plus performant.
        2: Legere compression, la plus rapide
           en temps de calcul.
        3: Legere compression qui maximise
           le ratio 'taille_gagnee/temps'.
        4: Moyenne compression qui vise un ratio
           environ egal a 95% du ratio maximum.
        5: Compression maximale qui ne se preocupe pas du temps.
    :param copy_file:
        Permet de copier le fichier si 'obj' est un nom de fichier.
        La chaine de caractere ne sera alteree en aucun cas.
    :type copy_file: bool
        True: Le fichier est copie et fait parti du resultat.
              Au moment de la deserialisation,
              le fichier sera regenere.
        False: Si 'obj' est un nom de fichier, il sera
               seulement considerer comme un 'str'.
    :param psw: Permet de chiffrer la valeur de retour.
    :type psw: str, bytes, None
        str: Chiffre avec l'algorithme AES.
        bytes: Clef publique au format PEM, RSA est utilise.
        None: Ne chiffre rien du tout.
    :param authenticity: Permet d'ajouter un hash cryptographique.
    :type authenticity: bool
        True: Ajoute des donnees de controle.
        False: N'ajoute rien du tout.
    :param parallelization_rate:
        Permet de partager le calcul afin de mieu profiter
        des resources de l'ordinateur.
    :type parallelization_rate: int
        0: Aucune parallelisation, tout est excecute
           dans le processus courant.
        1: Pseudo parallelisation, reparti les operations
           dans des threads du module 'threading'.
        2: Legere parallelisation, utilise les differents coeurs
           de la machine avec le module 'multiprocessing'.

    sortie
    ------
    :return: Une suite de 'bytes' qui contient l'information
             suffisante pour reconstiuer l'objet.
    :rtype: <class 'generator'>
    """
    with Printer("Serialization of a {} object...".format(type(obj).__name__)) as p:
        obj_ser = to_gen(gen=_serialize(
            obj,
            copy_file=kwargs["copy_file"],
            p=p,
            compact=(1 if kwargs["compresslevel"] else 0)))
        if kwargs["compresslevel"] not in (0, 1):
            import raisin.serialization.compress as compress
            obj_ser = to_gen(gen=compress.compress_gen(obj_ser, **kwargs))
        if kwargs["authenticity"]:
            import raisin.serialization.encrypt as encrypt
            obj_ser = to_gen(gen=encrypt.authenticity(
                obj_ser,
                compact=(1 if kwargs["compresslevel"] else 0)
                ))
        if kwargs["psw"]:
            import raisin.serialization.encrypt as encrypt
            obj_ser = to_gen(gen=encrypt.cipher_gen(
                obj_ser,
                psw=kwargs["psw"],
                compact=(1 if kwargs["compresslevel"] else 0),
                ))
        yield from obj_ser

def _serialize(obj, copy_file, p, compact):
    """
    |=========================================|
    | Serialise les objets sans les securiser |
    | ni sans non plus les compresser.        |
    |=========================================|
    
    parametres
    ----------
    :param obj: L'objet a serialiser.
    :type obj: object
    :param copy_file: Booleen qui indique si le nom de fichier doivent
        etre considerer comme des str ou comme un fichier.
        -True: Copie aussi le contenu du fichier.
        -False: Ne cherche rien a savoir, interprete come un str.
    :type copy_file: bool
    :param p: Instance de l'objet printer.
    :type p: raisin.tools.Printer
    :param compact: Determine si les objets serializes doivent restes humainement visibles.
    :type compact: int
        0: Le plus lisible possible.
        1: Le plus compact possible.
    sortie
    ------
    :return: L'objet serialise decoupe en packets de taille tres variable.
    :rtype: iter
    """
    def is_filename(obj, copy_file):
        """
        Retourne True si l'objet est un chemin vers un fichier
        et qu'il faut copier les fichiers.
        """
        if not copy_file:                   # si l'utilisateur ne nous autorise pas d'interpreter l'objet comme un fichier
            return False                    # alors on ne fait meme pas la suite du test
        if type(obj) == str:                # deja il faut que l'objet soit une chaine de caractere
            if len(obj) < 32767:            # et qu'il ne soit pas trop gros, sinon microchiotte windaube plante
                return os.path.isfile(obj)  # alors on fait le test
        return False    

    def is_jsonisable(obj, copy_file):
        """
        Retourne True si l'objet peu etre serialise avec json.
        Retourne False le cas echeant.
        """
        if type(obj) in (int, float, bool, type(None)):     # si l'objet est vraiment basique
            return True                                     # alors json sait le serialiser
        elif type(obj) == str:                              # dans le cas ou c'est une chaine de caractere
            if not is_filename(obj, copy_file):
                return True
        elif type(obj) == list:                             # dans le cas ou l'objet est une liste
            for element in obj:                             # on a pas d'autre choix que de parcourir la liste
                if not is_jsonisable(element, copy_file):   # si l'un des elements n'est pas compatible avec json
                    return False                            # alors la liste n'est pas jsonisable
            return True                                     # par contre, si tout est ok, allors on le jsonisifi
        elif type(obj) == dict:                             # de meme, dans le cas ou l'objet est un dictionnaire
            for key, value in obj.items():                  # pour faire la verification, on s'y prend comme pour les listes
                if not is_jsonisable(value, copy_file):     # si l'un des elements du dictionnaire fait tout capoter
                    return False                            # on ne va pas plus loin
                elif not is_jsonisable(key, copy_file):     # meme si c'est moin probable, mais si la clef n'est pas satisfesante
                    return False                            # tant pis, ça fait tout arreter quand meme
            return True                                     # si tout semble ok, et bien on dit qu'il est jsonalisable
        return False                                        # dans tous les autres cas, json ne fait pas bien le boulot

    def ser_filename(filename):
        """
        Encapsule le nom du fichier et le contenu du fichier.
        """
        filename_bytes = filename.encode("utf-8")
        yield size_to_tag(len(filename_bytes)) + filename_bytes
        with open(filename, "rb") as f:
            while 1:
                pack = f.read(BUFFER_SIZE)
                if pack:
                    yield pack
                else:
                    break

    def ser_float(f):
        """
        Recherche la representation la plus compacte possible.
        Retourne le type de solution ("s" ou "b") et les datas
        """
        as_str = str(f)                 # on represente le flotant en virant les 0 en trop
        if as_str[:2] == "0.":          # 0.123 devient .123
            as_str = as_str[1:]
        elif as_str[:3] == "-0.":       # -0.123 devient -.123
            as_str = as_str[0] + as_str[2:]
        elif as_str[-2:] == ".0":       # si il y a des 0 en trop a la fin
            as_str = as_str[:-2]        # 12.0 devient 12
            end_0 = 0 # nombre de 0 a la fin
            while as_str[-end_0-1:] == "0"*(end_0+1):
                end_0 += 1
            if end_0 >= 3:
                as_str = as_str[:-end_0] + "e" + str(end_0)
        as_str = as_str.replace("e+", "e")
        
        if len(as_str) < 16:
            if len(as_str) % 2:
                as_str = "0" + as_str
            pack = b""
            cor = {**{str(i):i for i in range(10)}, **{"-":10, "e":11, ".":12}}
            for i in range(0, len(as_str), 2):
                pack += bytes([cor[as_str[i+1]] + cor[as_str[i]]*len(cor)])
            return "round float", pack
        return "normal float", struct.pack("d", f)

    def ser_textiowrapper(file, p):
        """
        Cede des packet d'entete et de contenu du fichier
        """
        closed = b"\x01" if file.closed else b"\x00"     # 1 si le flux est ferme ou 0 si il est encore actif
        mode = file.mode.encode("utf-8")                 # son mode ("r", "w", "a", ...)
        encoding = file.encoding.encode("utf-8")         # l'encodage dans lequel on doit lire le fichier
        errors = file.errors.encode("utf-8")             # les differents modes de gestion possible des erreur de lecture
        stream_position = b"".join(_serialize(
            obj=(0 if obj.closed else obj.tell()),
            copy_file=False,
            p=p,
            compact=1))                                 # la position en nombre de caractere du curseur courant par rapport au debut du fichier
        
        yield size_to_tag(len(closed)) + closed \
              + size_to_tag(len(mode)) + mode \
              + size_to_tag(len(encoding)) + encoding \
              + size_to_tag(len(errors)) + errors \
              + size_to_tag(len(stream_position)) + stream_position

        if not b"r" in mode and not closed:             # si on est en ecriture
            file.flush()                                # on force l'ecriture sur le support phisique
        with open(file.name, "rb") as f:
            while 1:
                pack = f.read(BUFFER_SIZE)
                if pack:
                    yield pack
                else:
                    break

    def ser_buffered(file, p):
        """
        Cede les packets qui contiennent
        toutes l'informations suffisante pour
        recrer un fichier binaire dans le meme etat.
        """
        closed = b"\x01" if file.closed else b"\x00"    # 1 si le flux est ferme ou 0 si il est encore actif
        mode = file.mode.encode("utf-8")                # son mode ("rb", "wb", "ab", ...)
        stream_position = b"".join(_serialize(
            obj=(0 if file.closed else file.tell()),
            copy_file=False,
            p=p,
            compact=1))                                 # la position en nombre de caractere du curseur courant par rapport au debut du fichier
        
        yield size_to_tag(len(closed)) + closed \
              + size_to_tag(len(mode)) + mode \
              + size_to_tag(len(stream_position)) + stream_position

        if not b"r" in mode:                            # si on est en ecriture
            if not closed:
                file.flush()                            # on force l'ecriture sur le support phisique
            with open(file.name, "rb") as f:            # affin d'avoir acces au contenu
                while 1:
                    pack = f.read(BUFFER_SIZE)
                    if pack:
                        yield pack
                    else:
                        break
        else:                                           # si on est en lecture
            curs = file.tell()                          # on en profite pour ne pas reouvrir un autre fichier
            file.seek(0, 0)
            while 1:
                pack = file.read(BUFFER_SIZE)
                if pack:
                    yield pack
                else:
                    break
            file.seek(curs, 0)

    def ser_iter(iterable, copy_file, compact):
        """
        'iterable' est un iterable.
        Serialise un iterable on concatenant de facon
        reversible la serialisation de chacuns des elements.
        """
        with Printer("Iterable serialization...") as p:
            new = b"n"                   # fanion qui announce que il faut passer a l'element suivant
            end = b"e"                   # fanion qui indique que c'est fini
            cont = b"c"                  # fanion qui indique qu'on est encore en plein dans l'objet

            for is_end_iter, e in anticipate(iterable): # pour chaque element de l'iterable
                for is_end_elem, pack in anticipate(
                        to_gen(
                            gen=_serialize(
                                e,
                                copy_file=copy_file,
                                p=p,
                                compact=compact)
                            )
                        ):
                    indication = (end if is_end_iter else new) if is_end_elem else cont
                    yield size_to_tag(len(pack)+1) + pack + indication

    if type(obj) == int:
        if not compact and sys.getsizeof(obj) <= 64:
            p.show("small int -> data")
            yield HEADER["small int"][0] + str(obj).encode()
        else:
            p.show("large int -> data")
            yield HEADER["large int"][compact] + obj.to_bytes(
                length=(8 + (obj + (obj < 0)).bit_length()) // 8,
                byteorder="big",
                signed=True) # on encode plus efficacement
    elif is_filename(obj, copy_file):
        p.show("filename + file_content -> data")
        yield HEADER["filename"][compact]
        yield from ser_filename(obj)
    elif type(obj) == str:
        p.show("str -> data")
        yield HEADER["str"][compact] + obj.encode("utf-8")
    elif type(obj) == float:
        p.show("float -> data")
        if compact:
            g, data = ser_float(obj)
            yield HEADER[g][compact] + data
        else:
            yield HEADER["float"][compact] + str(obj).encode()
    elif type(obj) == complex:
        p.show("complex -> data")
        r = b"".join(_serialize(obj.real, copy_file=copy_file, p=p, compact=compact))
        i = b"".join(_serialize(obj.imag, copy_file=copy_file, p=p, compact=compact))
        yield HEADER["complex"][compact] + size_to_tag(len(r)) + r + i
    elif type(obj) == bytes:
        p.show("bytes -> data")
        yield HEADER["bytes"][compact] + obj
    elif issubclass(type(obj), io.TextIOWrapper):
        p.show("io.TextIOWrapper -> data")
        yield HEADER["TextIOWrapper"][compact]
        yield from ser_textiowrapper(obj, p)
    elif issubclass(type(obj), io.BufferedReader):
        p.show("io.BufferedReader -> data")
        yield HEADER["BufferedReader"][compact]
        yield from ser_buffered(obj, p)
    elif issubclass(type(obj), io.BufferedWriter):
        p.show("io.BufferedWriter -> data")
        yield HEADER["BufferedWriter"][compact]
        yield from ser_buffered(obj, p)
    elif type(obj) == tuple:
        p.show("tuple -> data")
        yield HEADER["tuple"][compact]
        yield from ser_iter(obj, copy_file, compact)
    elif type(obj) == bool:
        p.show("bool -> data")
        yield HEADER["true"][compact] if obj else HEADER["false"][compact]
    elif obj == None:
        p.show("null -> data")
        yield HEADER["null"][compact]
    elif type(obj) == set:
        p.show("set -> data")
        yield HEADER["set"][compact]
        yield from ser_iter(obj, copy_file, compact)
    elif type(obj) == frozenset:
        p.show("frozenset -> data")
        yield HEADER["frozenset"][compact]
        yield from ser_iter(obj, copy_file, compact)
    elif inspect.isclass(obj):                                      # si l'objet est une classe, qu'elle soit integree ou creee dans du code python
        p.show("class -> data")
        raise NotImplementedError()
    elif inspect.ismodule(obj):                                     # si l'objet est un module
        p.show("module -> data")
        raise NotImplementedError()
    elif inspect.isfunction(obj):                                   # si l'objet est une fonction python, qui inclut des fonctions creees par une expression lambda
        p.show("function -> data")
        raise NotImplementedError()
    elif inspect.isgenerator(obj):                                  # si l'objet est un generateur
        p.show("generator -> data")
        yield HEADER["generator"][compact]
        yield from ser_iter(obj, copy_file, compact)
    elif not compact and sys.getsizeof(obj) <= BUFFER_SIZE and is_jsonisable(obj, copy_file):
        p.show("json -> data")
        yield HEADER["json"][compact] + json.dumps(obj).encode("utf-8")
    
    elif type(obj) == list:
        p.show("list -> data")
        yield HEADER["list"][compact]
        yield from ser_iter(obj, copy_file, compact)
    elif type(obj) == dict:
        p.show("dict -> data")
        yield HEADER["dict"][compact]
        yield from ser_iter(
            obj.items(),
            copy_file,
            compact)
    else:
        p.show("unknown object -> pickle -> data")
        yield HEADER["pickle"][compact] + cloudpickle.dumps(obj)
