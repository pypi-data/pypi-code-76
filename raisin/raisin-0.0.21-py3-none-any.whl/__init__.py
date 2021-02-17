#!/usr/bin/env python3

"""
|=============================|
| Du calcul parallele facile! |
|=============================|

Pour plus d'informations voir:
https://framagit.org/robinechuca/raisin/-/blob/master/README.rst
"""

import io
import re
import sys

from . import raisin
from . import crashreporter

__version__ = "3.0.0"
__author__ = "Robin RICHARD <raisin@ecomail.fr>"
__all__ = ["dumps", "loads", "dump", "load", "copy",
           "serialize", "deserialize", "graph",
           "Map", "map", "Process", "process", "Scan", "scan",
           "open"]

# Pour recuperer l'erreur en cas de plantage.
sys.excepthook = crashreporter.crash_report


# Accessoires:

def dumps(obj, **kwargs):
    """
    |===================================================================|
    | Serialise, compresse et chiffre simplement tous type d'objets.    |
    | Retourne Une chaine de caractere plutot que des octets.           |
    | Le resultat tend vers 64/51 fois plus de symbols que 'serialize'. |
    |===================================================================|

    parametres
    ----------
    Ce sont les meme que 'serialize'

    sortie
    ------
    :return:
        Le resultats de la fonction serialize
        sous forme de gentil caracteres ASCII imprimables.
    :rtype: str

    exemple
    -------
    :Example:
    >>> import raisin
    >>> raisin.dumps(123456789)
    'f2Y@c30Mc3MLfz4OcPgRdzsUej0M..'
    >>> raisin.dumps(123456789, psw="mot de passe")
    'f2Y@ejsVdPMLfBYyG69Lq8CasrgYmyCfJRfeDTWCCAT3YDJhTABO8Z7bA8_WXZ4PFEbZWK5QBEZ8TLDhY30M..'
    >>>
    """
    import raisin.serialization.serialize as serialize_

    kwargs["compresslevel"] = kwargs.get("compresslevel", 5)

    return serialize_.dumps(serialize(obj, **kwargs))


def loads(chaine, **kwargs):
    """
    |===================================|
    | Bijection de la fonction 'dumps'. |
    |===================================|

    parametres
    ----------
    :param chaine: Objet python serialise par la fonction 'dumps'.
    :type chaine: str

    Les autres parametres sont les memes que ceux de
    la fonction 'deserialize'.
    
    sortie
    ------
    :return: L'objet de depart qui a ete serialise.
    :rtype: object

    exemple
    -------
    :Example:
    >>> import raisin
    >>> raisin.loads('f2Y@c30Mc3MLfz4OcPgRdzsUej0M..')
    123456789
    >>>
    """
    import raisin.serialization.deserialize as deserialize_
    assert isinstance(chaine, str), \
        "'chaine' doit etre un str, pas un {}.".format(
        type(chaine).__name__)

    return deserialize(deserialize_.loads(chaine), **kwargs)


def dump(obj, file, **kwargs):
    """
    |====================================|
    | Serialise un objet dans un fichier |
    |====================================|
    
    parametres
    ----------
    :param obj: N'importe quel type d'objet python,
        celui a serialiser.
    :type obj: object
    :param file: Flux d'ecriture des donnees.
    :type file: io.BufferedWriter

    Les autres parametres sont les memes que ceux de
    la fonction 'serialize'.
    
    sortie
    ------
    :return: Rien du tout.
    :rtype: None

    exemple
    -------
    :Example:
    >>> import raisin
    >>> with open("fichier", "wb") as f:
    ...     raisin.dump(123456789, f)
    ...
    >>>
    """
    assert isinstance(file, io.BufferedWriter), \
        "'file' doit etre un 'io.BufferedWriter', " \
        "pas un {}.".format(type(file).__name__)

    for pack in serialize(obj, **kwargs):
        file.write(pack)


def load(file, **kwargs):
    """
    |=================================|
    | Bijection de la fonction 'dump' |
    |=================================|

    parametres
    ----------
    :param file: Flux en lecture contenant les donnees fournis par 'dump'.
    
    Les autres parametres sont les memes que ceux de
    la fonction 'deserialize'.

    sortie
    ------
    :return: L'objet de depart qui a ete serialise.

    exemple
    -------
    :Example:
    >>> import raisin
    >>> with open("fichier", "wb") as f:
    ...     raisin.dump(123456789, f)
    ...
    >>> with open("fichier", "rb") as f:
    ...     obj = raisin.load(f)
    ...
    >>> obj
    123456789
    >>>
    """
    assert isinstance(file, io.BufferedReader), \
        "'file' doit etre un 'io.BufferedReader', " \
        "pas un {}.".format(type(file).__name__)

    return deserialize(file, **kwargs)


def serialize(obj, **kwargs):
    """
    |========================================|
    | Serialise, compresse chiffre et assure |
    | l'authenticite de tout type d'objets.  |
    |========================================|

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
    import raisin.serialization.serialize as serialize_

    kwargs["compresslevel"] = kwargs.get("compresslevel", 0)
    assert isinstance(kwargs["compresslevel"], int), \
        "'compresslevel' have to 'int', not {}.".format(
            type(kwargs["compresslevel"]).__name__)
    assert -1 <= kwargs["compresslevel"] <= 5, \
        "'compresslevel' have to be in [-1, 5]," \
        + " not {d}".format(kwargs["compresslevel"])

    kwargs["copy_file"] = kwargs.get("copy_file", True)
    assert isinstance(kwargs["copy_file"], bool), \
        "'copy_file' have to be bool, not {}.".format(
        type(kwargs["copy_file"]).__name__)

    kwargs["psw"] = kwargs.get("psw", None)
    if kwargs["psw"] != None:
        if isinstance(kwargs["psw"], bytes):
            try:
                assert re.search(
                    r"-----BEGIN PUBLIC KEY-----(.|\n)+-----END PUBLIC KEY-----",
                    kwargs["psw"].decode()), \
                    "La clef publique n'est pas au format 'PEM'."
            except UnicodeDecodeError as e:
                raise ValueError(
                    "Si il est de type (bytes), le mot de passe doit etre une "
                    "clef publique RSA au format PEM, ce n'est pas la cas.") from e
        elif isinstance(kwargs["psw"], str):
            assert kwargs["psw"], \
                "Le mot de passe ne doit pas etre une chaine vide, " \
                + "Si il n'y a pas de mot passe, il ne faut pas le specifier."
        else:
            raise TypeError("'psw' have to be str or bytes, not {}.".format(
                type(kwargs["psw"]).__name__))

    kwargs["authenticity"] = kwargs.get(
        "authenticity",
        True if kwargs["psw"] != None else False)
    assert isinstance(kwargs["authenticity"], bool), \
        "'authenticity' have to be bool, not {}.".format(
            type(kwargs["authenticity"]).__name__)

    kwargs["parallelization_rate"] = kwargs.get("parallelization_rate", 0)
    assert isinstance(kwargs["parallelization_rate"], int), \
        "'parallelization_rate' have to 'int', not {}.".format(
            type(kwargs["parallelization_rate"]).__name__)
    assert 0 <= kwargs["parallelization_rate"] <= 2, \
        "'parallelization_rate' have to be in [0, 2]," \
        + " not {d}".format(kwargs["parallelization_rate"])
    surplus = set(kwargs) - {"compresslevel", "copy_file",
                             "psw", "authenticity", "parallelization_rate"}
    assert surplus == set(), \
        "'Le(s) parametre(s) {} est/sont en trop.".format(
            ", ".join(surplus))

    yield from serialize_.serialize(obj, **kwargs)

def deserialize(data, **kwargs):
    """
    |=======================================|
    | Bijection de la fonction 'serialize'. |
    |=======================================|

    parametres
    ----------
    :param data: Objet python serialise par la fonction 'serialize'.
    :type data: bytes, generator, io.BufferedReader, str, io.TextIOWrapper
        bytes: Recommande pour les petits objets,
               sinon la RAM en prend un coup!
        generator: Recommande. Doit ceder des bytes.
                   Peut provenir par example de 'serialize'
        io.BufferedReader: A utiliser que lorsque les donnees sont
                persistantes. Sinon, la lecture et l'ecriture
                dans le disque risque de ralentir l'operation.
        str: Deconseille, fonctionne uniquement si les donnees
             proviennent de 'dumps'.
        io.TextIOWrapper: Deconseille, a utiliser uniquement si
                les donnees sont persistantes et qu'elles
                priviennent des la fonction 'dumps'.
    :param psw: Permet de dechiffrer l'entree
    :type psw: str, bytes, None
        str: Dechiffre avec l'algorithme AES.
        bytes: Clef privee non chiffree au format PEM, RSA est utilise.
        None: Ne tente rien du tout.
    :param parallelization_rate: Permet de partager le calcul affin de mieu profiter des resources de l'ordinateur.
    :type parallelization_rate: int
        0: Aucune parallelisation, tout est excecuter dans le processus courant.
        1: Pseudo parallelisation, reparti les operations dans des threads du module 'threading'.
        2: Legere parallelisation, utilise les differents coeurs de la machine avec le module 'multiprocessing'.

    sortie
    ------
    :return: L'objet de depart qui a ete serialise

    exemple
    -------
    :Example:
    >>> import raisin
    >>> raisin.deserialize(b'</>0000</>123456789')
    123456789
    >>>
    """
    import raisin.serialization.deserialize as deserialize_

    assert  isinstance(data, bytes) or \
            hasattr(data, "__iter__") or \
            isinstance(data, io.BufferedReader) or \
            isinstance(data, str) or \
            isinstance(data, io.TextIOWrapper), \
            "'data' have to be bytes, generator, io.BufferedReader, " \
            "str or io.TextIOWrapper. Not {}.".format(type(data).__name__)
    kwargs["parallelization_rate"] = kwargs.get("parallelization_rate", 0)
    assert isinstance(kwargs["parallelization_rate"], int), \
        "'parallelization_rate' have to 'int', not {}.".format(
            type(kwargs["parallelization_rate"]).__name__)
    assert 0 <= kwargs["parallelization_rate"] <= 2, \
        "'parallelization_rate' have to be in [0, 2]," \
        + " not {d}".format(kwargs["parallelization_rate"])
    kwargs["psw"] = kwargs.get("psw", None)
    if kwargs["psw"] != None:
        if isinstance(kwargs["psw"], bytes):
            try:
                assert re.search(
                    r"-----BEGIN RSA PRIVATE KEY-----(.|\n)+-----END RSA PRIVATE KEY-----",
                    kwargs["psw"].decode()), \
                    "La clef privee n'est pas au format 'PEM'."
            except UnicodeDecodeError as e:
                raise ValueError(
                    "Si il est de type (bytes), le mot de passe doit etre une "
                    "clef privee RSA au format PEM, ce n'est pas la cas."
                    ) from e
        elif isinstance(kwargs["psw"], str):
            assert kwargs["psw"], \
                "Le mot de passe ne doit pas etre une chaine vide, " \
                + "Si il n'y a pas de mot passe, il ne faut pas le specifier."
        else:
            raise TypeError("'psw' have to be str or bytes, not {}.".format(
                type(kwargs["psw"]).__name__))
    surplus = set(kwargs) - {"psw", "parallelization_rate"}
    assert surplus == set(), \
        "'Le(s) parametre(s) {} est/sont en trop.".format(
            ", ".join(surplus))

    return deserialize_.deserialize(data, **kwargs)


def copy(obj):
    """
    |============================================|
    | Faire une copie vraie: Dupliquer un objet. |
    |============================================|

    :param obj: N'importe quel objet que l'on shouaite copier.
    :return: Une copie veritable de l'objet 'obj'.

    :Example:
    >>> import raisin
    >>> a = {0: "a", 1: "b"}
    >>> a
    {0: 'a', 1: 'b'}
    >>> b = a
    >>> b[1] = "c"              # a est aussi affecte
    >>> a, b
    ({0: 'a', 1: 'c'}, {0: 'a', 1: 'c'})
    >>> b = raisin.copy(a)
    >>> b[1] = "b"              # a n'est pas affecte
    >>> a, b
    ({0: 'a', 1: 'c'}, {0: 'a', 1: 'b'})
    >>>
    """
    import raisin.tools
    with raisin.tools.Printer("Copy of '%s'..." % obj):
        return deserialize(
            serialize(
                obj,
                compresslevel=1,
                copy_file=True),
        )


def open(file, mode="", **kwargs):
    """
    extension de la methode '<built-in function open>'
    'mode' peut prendre differentes valeurs:
        -"r" (read):
            renvoi l'objet _io.TextIOWrapper en mode "r"
        -"a" (append):
            renvoi l'objet _io.TextIOWrapper en mode "a"
        -"w" (write):
            renvoi l'objet _io.TextIOWrapper en mode "w"
        -"rb" (read binary):
            renvoi l'objet _io.BufferedReader
        -"ab" (append binary):
            renvoi l'objet _io.BufferedWriter
        -"wb" (write binary):
            renvoi l'objet _io.BufferedWriter
        -"rp" (read python):
            renvoi un objet specialiste de la lecture des fichiers python
            il est capable de normaliser le texte et retirer les commentaires
            il permet aussi une analyse poussee des ligne de codes
        -"rc" (read csv):
            renvoi un dictionaire contenant les valeurs de ce csv
        -"" (Lecure intelligente):
            dans le cas ou la methode 'read' ou __iter__ est appelle:
                -renvoi des objets deserialiser si le fichier en encapsule
                -renvoi du str si tous le fichier est encode en utf-8
                    -avec normalisation syntaxique dans le cas d'un fichier python
                -renvoi du bytes si ce n'est rien de tous ca
            dans le cas ou la methode 'write' est appelee:
                -ecrit du texte tant que seul du STR est passe en parametre
                -ecrit du binaire tant que seul du BYTES est passe en parametre
                -serialise et encapsule le reste si un objet autre est passe en parametre
    buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener
    """
    import raisin.reader
    return raisin.reader.open_extend(file, mode=mode, **kwargs)


# Fonction de alcul partage.

class Map(raisin.Map):
    """
    |==================================|
    | Comme 'map' mais en plus souple. |
    |==================================|

    :Example:
    >>> import raisin
    >>> def foo(x):
    ...    return x**2
    ...
    >>> m = raisin.Map(foo, [0, 1, 2, 3])
    >>> m.start()           # rend la main imediatement
    >>> list(m.get())
    [0, 1, 4, 9]
    >>>
    """
    def __init__(self,
                 target,
                 *iterables,
                 force=True,
                 timeout=3600 * 24 * 31,
                 job_timeout=3600 * 48,
                 save=True,
                 parallelization_rate=4,
                 ordered=True,
                 signature=None):
        """
        :param target: Fonction qui doit etre evaluee plein de fois.
        :type target: callable
        :param iterables: Chaque iterable associes a chacuns des arguments de la fonction, le premier iterable epuise arrette les autres.
        :param force: Permet de relancer le calcul meme si il le resultat est deja enregistre.
        :type force: bool
        :param timeout: Permet de lever une exception si ca met trop de temps en tout.
        :type timeout: int
        :param job_timeout: Permet de lever une exception sur chaque evaluation trop lente. Les autres threads continuent de tourner.
        :type job_timeout: int
        :param save: Permet de decider si le resultat est enregistrer.
        :type save: bool
            True: Le resultat est enregistre si cela en vaut la peine (gain de vitesse).
            False: Le resultat n'est pas enregistre nul part (il faut tout recommencer a chaque fois, pas de reprise possible)
        :param parallelization_rate: Permet de partager le calcul affin de mieu profiter des resources de l'ordinateur.
        :type parallelization_rate: int
            0: Aucune parallelisation, tout est excecuter dans le processus courant.
            1: Pseudo parallelisation, reparti les operations dans des threads du module 'threading'.
            2: Legere parallelisation, utilise les differents coeurs de la machine avec le module 'multiprocessing'.
            3: Grosse parallelisation, utilise toutes les ressources disponible dans le reseau local LAN.
            4: Monstrueuse parallelisation, utilise toutes les ressources accessibles dans le monde entier!
        :param ordered: Force a ceder les resultat dans l'ordre
        :type ordered: bool
        :param signature: N'importe quel objet qui permet d'afficher dans la bonne colone du terminal.
        """
        assert callable(target)
        assert type(force) is bool
        assert type(timeout) is int
        assert timeout > 0
        assert type(job_timeout) is int
        assert job_timeout > 0
        assert type(save) is bool
        assert type(parallelization_rate) is int
        assert 0 <= parallelization_rate <= 4
        assert type(ordered) is bool

        raisin.Map.__init__(self,
                            target,
                            *iterables,
                            force=force,
                            timeout=timeout,
                            job_timeout=job_timeout,
                            save=save,
                            parallelization_rate=parallelization_rate,
                            ordered=ordered,
                            signature=signature)


def map(*args, **kwargs):
    """
    |=======================================================================|
    | Make an iterator that computes the function using arguments from      |
    | each of the iterables. Stops when the shortest iterable is exhausted. |
    |=======================================================================|

    :seealso: raisin.Map

    sortie
    ------
    :return: Chaque evaluation de la fonction pour chaque argument cedes par l'iterable le plus vite epuise.
    :rtype: <class 'generator'>

    exemple
    -------
    :Example:
    >>> import raisin
    >>> def foo(x):
    ...    return x**2
    ...
    >>> list(raisin.map(foo, [1, 2, 3]))
    [1, 4, 9]
    >>>
    """
    m = Map(*args, **kwargs)
    m.start()
    yield from m.get()


class Process(raisin.Process):
    """
    |=====================================|
    | Comme 'process' mais en plus souple |
    |=====================================|

    :Example:
    >>> import raisin
    >>> def foo(x):
    ...     return x**2
    ...
    >>> p1 = raisin.Process(foo, args=(2,))
    >>> p2 = raisin.Process(foo, args=(3,))
    >>> p1.start()
    >>> p2.start()
    >>> (p1.get(), p2.get())
    (4, 9)
    >>>
    """
    def __init__(self,
                 target,
                 args=(),
                 kwds={},
                 *,
                 force=True,
                 timeout=3600 * 24 * 31,
                 job_timeout=3600 * 48,
                 save=True,
                 parallelization_rate=4,
                 signature=None):
        """
        :param target: Fonction qui doit etre evaluee plein de fois.
        :type target: callable
        :param args: Ensemble des arguments passes a la fonction. Devient 'target(*args)'.
        :type args: tuple
        :para kwds: dict
        :param force: Permet de relancer le calcul meme si il le resultat est deja enregistre.
        :type force: bool
        :param timeout: Permet de lever une exception si ca met trop de temps en tout.
        :type timeout: int
        :param job_timeout: Permet de lever une exception sur chaque evaluation trop lente. Les autres threads continuent de tourner.
        :type job_timeout: int
        :param save: Permet de decider si le resultat est enregistrer.
        :type save: bool
            True: Le resultat est enregistre si cela en vaut la peine (gain de vitesse).
            False: Le resultat n'est pas enregistre nul part (il faut tout recommencer a chaque fois, pas de reprise possible)
        :param parallelization_rate: Permet de partager le calcul affin de mieu profiter des resources de l'ordinateur.
        :type parallelization_rate: int
            0: Aucune parallelisation, tout est excecuter dans le processus courant.
            1: Pseudo parallelisation, reparti les operations dans des threads du module 'threading'.
            2: Legere parallelisation, utilise les differents coeurs de la machine avec le module 'multiprocessing'.
            3: Grosse parallelisation, utilise toutes les ressources disponible dans le reseau local LAN.
            4: Monstrueuse parallelisation, utilise toutes les ressources accessibles dans le monde entier!
        :param signature: N'importe quel objet qui permet d'afficher dans la bonne colone du terminal.
        """
        assert callable(target)
        assert type(args) is tuple
        assert type(kwds) is dict
        assert type(force) is bool
        assert type(timeout) is int
        assert timeout > 0
        assert type(job_timeout) is int
        assert job_timeout > 0
        assert type(save) is bool
        assert type(parallelization_rate) is int
        assert 0 <= parallelization_rate <= 4

        raisin.Process.__init__(self,
                                target,
                                args,
                                kwds,
                                force=force,
                                timeout=timeout,
                                job_timeout=job_timeout,
                                save=save,
                                parallelization_rate=parallelization_rate,
                                signature=signature)


def process(target, args=(), kwds={}, **kwargs):
    """
    |========================================|
    | Equivalent of 'target(*args, **kwds)'. |
    |========================================|

    Meme si elle parait inutile, cette fonction permet
    De soulager la charge de calcul dans un thread du module 'threading'.
    Cela permet aussi d'isoler la fonction pour la
    rendre completement etanche au reste du programme.

    :seealso: raisin.Process

    sortie
    ------
    :return: La valeur renvoyee par 'target(*args, **kwds)'.

    exemple
    -------
    :Example:
    >>> import raisin
    >>> def f(x, y):
    ...    return x**2 + y
    >>> raisin.process(f, args=(2, 0))
    4
    >>>
    """
    p = Process(target, args=args, kwds=kwds, **kwargs)
    p.start()
    return p.get()


class Scan(raisin.Scan):
    """
    |==================================|
    | Comme 'scan' mais en plus souple |
    |==================================|

    :Example:
    >>> import raisin
    >>> def foo(x, y):
    ...     return x - y
    >>> s = raisin.Scan(foo, [0, 1, 2], [1, 2])
    >>> s.start()
    >>> s.get()
    [[-1, -2], [0, -1], [1, 0]]
    >>>
    """

    def __init__(self,
                 target,
                 *iterables,
                 force=True,
                 timeout=3600 * 24 * 31,
                 job_timeout=3600 * 48,
                 save=True,
                 parallelization_rate=4,
                 signature=None):
        """
        :param target: Fonction qui doit etre evaluee plein de fois.
        :type target: callable
        :param iterables: Chaque iterable associes a chacuns des arguments de la fonction.
        :param force: Permet de relancer le calcul meme si il le resultat est deja enregistre.
        :type force: bool
        :param timeout: Permet de lever une exception si ca met trop de temps en tout.
        :type timeout: int
        :param job_timeout: Permet de lever une exception sur chaque evaluation trop lente. Les autres threads continuent de tourner.
        :type job_timeout: int
        :param save: Permet de decider si le resultat est enregistrer.
        :type save: bool
            True: Le resultat est enregistre si cela en vaut la peine (gain de vitesse).
            False: Le resultat n'est pas enregistre nul part (il faut tout recommencer a chaque fois, pas de reprise possible)
        :param parallelization_rate: Permet de partager le calcul affin de mieu profiter des resources de l'ordinateur.
        :type parallelization_rate: int
            0: Aucune parallelisation, tout est excecuter dans le processus courant.
            1: Pseudo parallelisation, reparti les operations dans des threads du module 'threading'.
            2: Legere parallelisation, utilise les differents coeurs de la machine avec le module 'multiprocessing'.
            3: Grosse parallelisation, utilise toutes les ressources disponible dans le reseau local LAN.
            4: Monstrueuse parallelisation, utilise toutes les ressources accessibles dans le monde entier!
        :param signature: N'importe quel objet qui permet d'afficher dans la bonne colone du terminal.
        """
        assert callable(target)
        assert type(force) is bool
        assert type(timeout) is int
        assert timeout > 0
        assert type(job_timeout) is int
        assert job_timeout > 0
        assert type(save) is bool
        assert type(parallelization_rate) is int
        assert 0 <= parallelization_rate <= 4

        raisin.Scan.__init__(self,
                             target,
                             args,
                             kwds,
                             force=force,
                             timeout=timeout,
                             job_timeout=job_timeout,
                             save=save,
                             parallelization_rate=parallelization_rate,
                             signature=signature)


def scan(target, *iterables, **kwargs):
    """
    |==========================================================|
    | Permet d'evaluer une fonction en balayant ces arguments. |
    |==========================================================|

    sortie
    ------
    :return: Un tenseur de dimension egale au nombre d'arguments len(iterables).
             Chaque valeur presente dans le tenseur et l'une des valeur de retour
             De la fonction 'target' evalue pour un couple de parametre fixe.
    :rtype: list

    exemple
    -------
    :Example:
    >>> import raisin
    >>> def foo(x, y):
    ...     return x - y
    >>> raisin.scan(f, [0, 1, 2], [1, 2])
    [[-1, -2], [0, -1], [1, 0]]
    >>>
    """
    s = Scan(target, *iterables, **kwargs)
    s.start()
    return s.get()
