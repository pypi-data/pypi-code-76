#!/usr/bin/env python3

"""
Deserialise l'information affin de retrouver les objets de depart.
"""

import cloudpickle
import io
import itertools
import json
import os
import struct
import uuid

from .constants import *
from .tools import *
from ..tools import Printer, temprep


def loads(chaine):
    """
    |============================================================|
    | Desencapsule chaine pour retrouver les donnees originales. |
    |============================================================|

    Ne fait pas de verification sur l'entree.

    parametres
    ----------
    :param chaine: Donnees provenant directement de 'dumps'.
    :type chaine: str

    sortie
    ------
    :return: Les octets juste avant qu'ils ne soient transformes en str.
    :rtype: bytes
    """
    def anticipate_var(chaine, size):
        """
        Generator qui cede des packets de 'size' octets.
        Cede aussi un booleen qui annonce l'arrive du dernier packet.
        """
        div, rest = divmod(len(chaine), size)
        final = div + 1 if rest else div
        for i in range(final):
            yield i+1 == final, chaine[size*i:size*(i+1)]
    
    def alph_to_int(phrase, n1, index):
        """
        Converti une chaine constitue par des
        symboles de l'alphabet en entier.
        """
        i = 0
        for rang, symb in enumerate(reversed(phrase)):
            i += index[symb] * n1**rang
        return i

    def int_to_pack(i, n_bytes):
        """
        Converti un entier en une chaine binaire.
        Retourne 'n_bytes' octets.
        """
        return i.to_bytes(n_bytes, byteorder="big", signed=False)
   
    def alph_to_pack(phrases, n1, index, n_bytes):
        """
        Convertie tous les blocs d'un coup pour plus de
        performance
        """
        return b"".join([
            int_to_pack(
                alph_to_int(phrase, n1, index),
                n_bytes
            )
            for phrase in phrases
        ])

    # preparation (n1**n_symb >= n2**n_bytes)
    head, gen, pack = get_header(pack=chaine.rstrip().lstrip().encode("ascii"))
    chaine = (pack + b"".join(gen)).decode("ascii")
    index = {symb: i for i, symb in enumerate(ALPHABET)}
    if head == "small dumps":
        n1 = 64 # Nbr de caracteres differents.
        n_bytes = 3 # C'est le nombre d'octet que l'on regroupe.
        n_symb = 4 # On converti 3 octets en 4 caracteres.
    elif head == "large dumps":
        n1 = len(ALPHABET) # Nbr de caracteres differents.
        n_bytes = N_BYTES # C'est le nombre d'octet que l'on regroupe.
        n_symb = N_SYMB # Regroupe N_BYTES octets en N_SYMB caracteres.
    else:
        raise ValueError(
            "L'entete ne peut etre que 'small dumps' ou " \
            + "'large dumps'. Pas {}.".format(head))

    # desencapsulation
    data = b""
    phrases = []
    bloc = BUFFER_SIZE // n_bytes
    for i, (is_end, phrase) in enumerate(anticipate_var(chaine, n_symb)): # on regroupe la chaine par 'n_symb' caracteres
        if is_end and len(phrase) < n_symb:
            data += alph_to_pack(phrases, n1, index, n_bytes)
            data = data[:-n_bytes] + data[-alph_to_int(phrase, n1, index):]
            return data
        phrases.append(phrase)
        if not i % bloc:
            data += alph_to_pack(phrases, n1, index, n_bytes)
            phrases = []
    data += alph_to_pack(phrases, n1, index, n_bytes)
    return data

def deserialize(data, psw, parallelization_rate):
    """
    |==================================================|
    | Deserialize les donnes pour en faire des objets. |
    |==================================================|
    N'effectue aucune verifications.
    Leve une Valuerror si les donnees sont incorrectes.
    
    parametres
    ----------
    :param data: Les donnes de l'objet a deserialiser.
    :type data: bytes, iter, io.BufferedReader, str, io.TextIOWrapper
    :type psw: str, bytes, None
        str: Dechiffre avec l'algorithme AES.
        bytes: Clef privee non chiffree au format PEM, RSA est utilise.
        None: Ne tente rien du tout.
    :param parallelization_rate: Permet de partager le calcul
        afin de mieu profiter des resources de l'ordinateur.
    :type parallelization_rate: int
        0: Aucune parallelisation, tout est excecuter
            dans le processus courant.
        1: Pseudo parallelisation, reparti les operations dans
            des threads du module 'threading'.
        2: Legere parallelisation, utilise les differents coeurs
            de la machine avec le module 'multiprocessing'.

    sortie
    ------
    :return: L'objet deserialise.
    :rtype: object
    """
    def format_data(data):
        """
        Interprete 'data' pour en faire un generateur
        d'octet. Retourne un generateur.
        """
        def _bufferedreader(data):
            while 1:
                pack = data.read(BUFFER_SIZE)
                if pack:
                    yield pack
                else:
                    break

        def _textiowrapper(data):
            while 1:
                    pack = data.read(BUFFER_SIZE)
                    if pack:
                        yield pack.encode(encoding="utf-8")
                    else:
                        break

        def _iter(data):
            for p in data:
                if type(p) is bytes:
                    yield p
                elif type(p) is str:
                    yield p.encode(encoding="utf-8")
                else:
                    raise TypeError("Les donnees cedes par le generateur \n" \
                        + "doivent etre de type bytes ou str, pas %s." % type(p))

        if type(data) is bytes:
            return (lambda:(yield from []))(), data
        elif type(data) is str:
            return (lambda:(yield from []))(), data.encode(encoding="utf-8")
        elif issubclass(type(data), io.BufferedReader):
            return _bufferedreader(data), b""
        elif issubclass(type(data), io.TextIOWrapper):
            if "r" in data.mode:
                return _textiowrapper(data), b""
            else:
                raise Valuerror(
                    "Le fichier doit etre en lecture, il est en %s." % data.mode)
        elif hasattr(data, "__iter__"):
            return _iter(data), b""
        else:
            raise TypeError("'data' n'est pas d'un type correct.\n" \
                            + "type(data) = %s\n" % type(data) \
                            + "Les types autorises sont bytes, " \
                            + "str, io.BufferedReader, io.TextIOWrapper, iter.")

    with Printer("Deserialization...") as p:
        gen, pack = format_data(data)
        head, gen, pack = get_header(gen=gen, pack=pack) # recuperation de l'entete
        p.show("data -> %s" % head)

        if head in TABLE1:
            return TABLE1[head](gen, pack)
        elif head in TABLE2:
            obj = TABLE2[head]
            _exhaust(gen, pack)
            return obj
        elif head in TABLE3:
            return deserialize(
                TABLE3[head](gen, pack),
                psw=psw,
                parallelization_rate=parallelization_rate,)
        else:
            raise ValueError("The header '%s' is unknown." % head)

def _exhaust(gen, pack):
    """
    S'assure que le generateur est epuise.
    Leve une ValueError si il n'est pas mort.
    Itere donc une fois de plus l'iterateur.
    """
    if pack:
        if len(pack) > 40:
            raise ValueError(
                "Il ne devrai pas rester de donnees!\n" \
                + "'pack' n'est pas vide, il vaut %s...%s ." \
                % (repr(pack[:20]), repr(pack[20:])))
        raise ValueError(
            "Il ne devrai pas rester de donnees!\n" \
            + "'pack' n'est pas vide, il vaut %s." % repr(pack))
    d = next(iter(gen), "vide")
    if d != "vide":
        if len(d) > 40:
            raise ValueError(
                "Il ne devrai pas rester de donnees!\n" \
                + "Le generateur n'est pas epuise, il reste au moins %s...%s ." \
                % (repr(d[:20]), repr(d[20:])))
        raise ValueError(
            "Il ne devrai pas rester de donnees!\n" \
            + "Le generateur n'est pas epuise, il reste au moins %s." % repr(d))

def _des_filename(gen, pack):
    """
    Change le repertoire courant pour se metre dans un repertoire temporaire.
    Si le fichier d'origine avait pour nom un chemin absolu,
    alors toute une arboresance va etre construite a partir du repertoir
    courant de facon a retourner exactement la meme chaine que celle definie par
    l'utilisateur qui a prealablement enregistre le fichier.
    si le fichier d'origine avait pour nom un chemin relatif,
    alors, un nouveau fichier nome par ce meme nom est cree dans le repertoir courant
    ne prend aucune precaution, peu donc ecraser un fichier si un fichier de meme nom etait deja present
    dans le repertoir par defaut
    Retourne le nom de ce fichier, relatif par rapport au repertoir courant.
    """
    def split_directories(directories):
        """
        retourne une liste avec chaques dossier
        les un apres les autres
        """
        liste = []                                                  # initialisation de la liste vide
        directories = os.path.normpath(directories)
        while directories != "":                                    # tant que l'on a pas parcouru la totalite du chemin
            directories, e = os.path.split(directories)             # on extrait le dossier du bout
            if e == "":                                             # si jamais on frole la boucle infinie
                break                                               # on ne s'y aventure pas plus que ca
            liste.insert(0, e)                                      # ajout de cet element dans la liste
        return liste

    # lecture entete
    taille_filename, gen, pack = tag_to_size(gen=gen, pack=pack)    # annalyse de l'entete qui permet de recuperer la taille du nom de fichier
    while len(pack) < taille_filename:                              # on sait jamais, il se peut que le nom de fichier soit
        pack += next(gen)                                           # trop grand pour aparraitre en entier dans pack
    filename, pack = pack[:taille_filename].decode("utf-8"), pack[taille_filename:]# une fois qu'on est certain qu'il y soit, on le recupere
    
    # preparation du terrain (creation des repertoires si besoin)
    os.chdir(temprep)                                               # on change de chemin courant
    if os.path.isabs(filename):                                     # si il s'agit d'un chemin absolu vers un fichier
        filename = os.path.basename(filename)                       # alors on ne s'embete pas, on le transforme en chemin relatif
    directories, file = os.path.split(filename)                     # separation entre le nom du fichier et le chemin qui y mene
    if directories != "":
        chemin_complet = ""                                         # cela va etre le chemin complet qui mene au dossier
        for directory in split_directories(directories):            # pour chaque dossier a parcourir
            chemin_complet = os.path.join(chemin_complet, directory)# on l'ajoute a la pile
            if not os.path.exists(chemin_complet):                  # si ce chemin n'est pas deja sur le disque
                os.mkdir(chemin_complet)                            # alors on l'ajoute
        filename = os.path.join(chemin_complet, file)               # quitte afaire quelque modification, on retourne un path valide

    # restitution du fichier
    with open(filename, "wb") as f:                                 # ouverture du fichier
        f.write(pack)                                               # puis on ecrit dedans son contenu
        for pack in gen:                                            # pour chaque packet restant
            f.write(pack)                                           # on y vide aussi le contenu du generateur
    return filename

def _des_textiowrapper(gen, pack):
    """
    'gen' cede la continuite de 'pack'.
    'pack' est une sequence d'octets.
    Deserialise un fichier text.
    """
    class TextIOWrapper(io.TextIOWrapper):
        def __init__(self, flux, *args, **kwargs):
            io.TextIOWrapper.__init__(self, flux.buffer, *args, **kwargs)
            self.__flux = flux # permet de faire en sorte que le ramasse miette ne ferme pas le fichier
            self.mode = flux.mode

        def close(self):
            super().close()
            self.__del__()

        def __del__(self):
            try:
                os.remove(self.name)
            except (AttributeError, FileNotFoundError):
                pass

    # lecture entete
    size_closed, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_closed:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur l'etat de fermeture du fichier."
                ) from e
    closed, pack = bool(pack[0]), pack[1:]

    size_mode, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_mode:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur le mode d'ouverture du fichier."
                ) from e
    mode, pack = pack[:size_mode].decode("utf-8"), pack[size_mode:]
    
    size_encoding, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_encoding:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur l'encodage du fichier."
                ) from e
    encoding, pack = pack[:size_encoding].decode("utf-8"), pack[size_encoding:]

    size_errors, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_errors:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur la gestion d'erreur du fichier."
                ) from e
    errors, pack = pack[:size_errors].decode("utf-8"), pack[size_errors:]

    size_stream_position, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_stream_position:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur la position du curseur dans le fichier."
                ) from e
    stream_position = deserialize(
                        pack[:size_stream_position],
                        psw=None,
                        parallelization_rate=None)
    pack = pack[size_stream_position:]

    # preparation du fichier
    filename = os.path.join(temprep, uuid.uuid4().hex)
    if "r" in mode:
        content = True if pack else False
        with open(filename, "wb") as f:
            f.write(pack)
            for pack in gen:
                content = True if pack else content
                f.write(pack)
        if not content:
            os.remove(filename)

    # creation de l'objet
    flux = open(filename, mode=mode) # On tente de reproduire fidellement l'etat du flux serialise.
    f = TextIOWrapper(flux, encoding=encoding, errors=errors)
    if "r" not in mode:
        f.write(pack.decode(encoding))
        for pack in gen:
            f.write(pack.decode(encoding)) 
    f.seek(stream_position, 0) # On place le curseur la ou il etait.
    if closed:
        f.close()
    return f

def _des_buffered(gen, pack):
    """
    'gen' cede la continuite de 'pack'.
    'pack' est une sequence d'octets.
    Deserialise un fichier text.
    """
    class BufferedReader(io.BufferedReader):
        def __init__(self, flux, *args, **kwargs):
            io.BufferedReader.__init__(self, flux.raw, *args, **kwargs)
            self.__flux = flux # permet de faire en sorte que le ramasse miette ne ferme pas le fichier

        def close(self):
            super().close()
            self.__del__()
            
        def __del__(self):
            try:
                os.remove(self.name)
            except (AttributeError, FileNotFoundError):
                pass
    # lecture entete
    size_closed, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_closed:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur l'etat de fermeture du fichier."
                ) from e
    closed, pack = bool(pack[0]), pack[1:]

    size_mode, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_mode:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur le mode d'ouverture du fichier."
                ) from e
    mode, pack = pack[:size_mode].decode("utf-8"), pack[size_mode:]
    
    size_stream_position, gen, pack = tag_to_size(gen=gen, pack=pack)
    while len(pack) < size_stream_position:
        try:
            pack += next(gen)
        except StopIteration as e:
            raise Valuerror(
                "Il manque des informations sur la position du curseur dans le fichier."
                ) from e
    stream_position = deserialize(
                        pack[:size_stream_position],
                        psw=None,
                        parallelization_rate=None)
    pack = pack[size_stream_position:]

    # preparation du fichier
    filename = os.path.join(temprep, uuid.uuid4().hex)
    content = True if pack else False
    if "r" in mode:
        with open(filename, "wb") as f:
            f.write(pack)
            for pack in gen:
                content = True if pack else content
                f.write(pack)
        if not content:
            os.remove(filename)

    # creation de l'objet
    flux = open(filename, mode=mode) # on tente de reproduire fidellement l'etat du flux serialise
    if "r" in mode:
        f = BufferedReader(flux)
    else:
        flux.write(pack)
        for pack in gen:
            flux.write(pack) 
        f = flux
    f.seek(stream_position, 0)   # on place le curseur la ou il etait
    if closed:
        f.close()
    return f

def _des_iter(gen, pack):
    """
    Deserialise un iterable.
    """
    class IterObj:
        """
        Itere sur un seul element.
        """
        def __init__(self, gen, pack):
            self.gen = gen
            self.pack = pack
            self.end = None # True quand l'objet est entierement cede
            self.last = False # True quand il n'y a pas d'autres objets apres
            self.is_end()

        def __next__(self):
            """
            Retourne le packet suivant.
            Si il n'y en a plus, leve StopIteration.
            """
            # verification de non epuisement
            if self.is_end():
                raise StopIteration

            # recuperation des donnees suivantes
            try:
                size, self.gen, self.pack = tag_to_size(gen=self.gen, pack=self.pack)
            except ValueError as e:
                raise ValueError(
                    "Impossible de recuperer l'entete de l'element."
                    ) from e
            while len(self.pack) < size:
                try:
                    self.pack += next(self.gen)
                except StopIteration as e:
                    raise ValueError(
                        "L'element n'est pas complet."
                        ) from e
            data, fanion, self.pack = self.pack[:size-1], self.pack[size-1:size], self.pack[size:]

            if fanion == b"c": # si l'objet n'est pas entierement cede
                self.end = False
            elif fanion == b"n": # si il est cede et qu'il y en a un autre deriere
                self.end = True
            elif fanion == b"e":
                self.end = True
                self.last = True
            else:
                raise ValueError("Le fanion ne peut etre que b'c', b'n' ou b'e', pas %s." % fanion)
            return data

        def __iter__(self):
            """
            Appele quand l'iterateur est creer.
            c'est quand on fait iter(self)
            """
            # return self
            while 1:
                try:
                    yield next(self)
                except StopIteration:
                    break

        def is_end(self):
            """
            Retourne les objets
            de l'iterateur serialises
            ont etes cedes
            """
            if self.end == None:
                if self.pack:
                    self.end = False
                else:
                    try:
                        self.pack = next(self.gen)
                        self.end = False
                    except StopIteration:
                        self.end = True
                        self.last = True
            return self.end

        def is_last(self):
            """
            Retourne True il n'y a pas d'autres objets apres.
            """
            return self.last

    iterobj = IterObj(gen, pack)
    while not iterobj.is_last():
        yield deserialize(
            relocate(iterobj),
            psw=None,
            parallelization_rate=0,
            )
        gen, pack = iterobj.gen, iterobj.pack
        iterobj = IterObj(gen, pack)
    _exhaust(iterobj.gen, iterobj.pack)

def _des_round_float(gen, pack):
    """
    Retourne le flottant originel.
    """
    as_str = ""
    cor = {**{i:str(i) for i in range(10)}, **{10:"-", 11:"e", 12:"."}}
    for b in pack + b"".join(gen):
        as_str += cor[b // len(cor)] + cor[b % len(cor)]
    as_str = as_str if as_str[0] != "0" else as_str[1:]
    return float(as_str)

def _des_complex(gen, pack):
    """
    Retourne le complex originel.
    """
    size, gen, pack = tag_to_size(gen=gen, pack=pack)
    pack += b"".join(gen)
    return complex(
        deserialize(pack[:size], psw=None, parallelization_rate=0),
        deserialize(pack[size:], psw=None, parallelization_rate=0))

def _des_authenticity(gen, pack):
    """
    Retourne le generateur initial en s'assurant qu'il soit authentique.
    """
    import raisin.serialization.decrypt as decrypt
    yield from decrypt.authenticity(itertools.chain([pack], gen))

def _des_decipher(gen, pack, psw):
    """
    Cede les donnees dechifrees.
    """
    import raisin.serialization.decrypt as decrypt
    yield from decrypt.decipher_gen(itertools.chain([pack], gen), psw)

# retour avec contenu
TABLE1 = {
    "small int": lambda gen, pack : int(str((pack + b"".join(gen)).decode())),
    "large int": lambda gen, pack : int.from_bytes(pack + b"".join(gen), byteorder="big", signed=True),
    "filename": lambda gen, pack: _des_filename(gen, pack),
    "str": lambda gen, pack: (pack + b"".join(gen)).decode("utf-8"),
    "round float": lambda gen, pack: _des_round_float(gen, pack),
    "normal float": lambda gen, pack: struct.unpack("d", pack + b"".join(gen))[0],
    "float": lambda gen, pack: float(str((pack + b"".join(gen)).decode())),
    "complex": lambda gen, pack: _des_complex(gen, pack),
    "bytes": lambda gen, pack: pack + b"".join(gen),
    "TextIOWrapper": lambda gen, pack: _des_textiowrapper(gen, pack),
    "BufferedReader": lambda gen, pack: _des_buffered(gen, pack),
    "BufferedWriter": lambda gen, pack: _des_buffered(gen, pack),
    "list": lambda gen, pack: list(_des_iter(gen, pack)),
    "tuple": lambda gen, pack: tuple(_des_iter(gen, pack)),
    "set": lambda gen, pack: set(_des_iter(gen, pack)),
    "frozenset": lambda gen, pack: frozenset(_des_iter(gen, pack)),
    "dict": lambda gen, pack: {k: v for k, v in _des_iter(gen, pack)},
    "generator": lambda gen, pack: (e for e in _des_iter(gen, pack)),
    "json": lambda gen, pack: json.loads((pack + b"".join(gen)).decode("utf-8")),
    "pickle": lambda gen, pack: cloudpickle.loads(pack + b"".join(gen)),
}

# retour imediat sans contenu
TABLE2 = {
    "true": True,
    "false": False,
    "null": None,
}

# etape avant le retour
TABLE3 = {
    "small dumps": lambda gen, pack: loads((HEADER["small dumps"][0] + pack + b"".join(gen)).decode()),
    "large dumps": lambda gen, pack: loads((HEADER["large dumps"][0] + pack + b"".join(gen)).decode()),
    "authenticity": lambda gen, pack: _des_authenticity(gen, HEADER["authenticity"][0] + pack),
    "aes sel": lambda gen, pack: _des_decipher(gen, HEADER["aes sel"][0] + pack, psw),
    "aes bloc": lambda gen, pack: _des_decipher(gen, HEADER["aes bloc"][0] + pack, psw),
    "rsa bloc": lambda gen, pack: _des_decipher(gen, HEADER["ras bloc"][0] + pack, psw),
    "aes gen": lambda gen, pack: _des_decipher(gen, HEADER["aes gen"][0] + pack, psw),
    "rsa gen": lambda gen, pack: _des_decipher(gen, HEADER["rsa gen"][0] + pack, psw),
}
