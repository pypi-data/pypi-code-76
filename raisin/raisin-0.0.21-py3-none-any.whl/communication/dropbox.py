#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import warnings
import os
import time

try:
    import dropbox
except ImportError:
    dropbox = None
    warnings.warn("'dropbox' failed to import, there may be difficulty communicating")

import raisin


class Dropbox:
    """
    lien vers dropbox
    les exception ne sont pas geres a ce niveau la, il faut les gerer au dessus
    """
    def __init__(self, name, key):
        assert dropbox is not None, "To use dropbox, install the dropbox module!"
        assert type(name) is str, "The type(name) must be 'str', '%s' is not 'str': it is '%s'." % (name, type(name))

        self.name = name            # nom de ce serveur dropbox
        self.access_token = key     # clef pour ce connecter a l'api du bon compte dropbox
        self.linked = False         # est True quand le serveur est bien connecte
        self.last_connection = 0    # date de la derniere tentative reussi de conection au serveur (pas time.time)
        self.free = True            # est True quand c'est libre
        self.dbx = None             # objet dropbox natif, initialiser avec self.connect()

    def connect(self, signature=None):
        """
        tente d'etablire une connection avec le serveur
        tout va se passer a la racine: '/'
        """
        if self.linked and (time.time() - self.last_connection < 60):       # si la derniere connection est toute fraiche
            return                                                          # on ne retente pas a nouveau
        try:                                                                # on prend des precautions pour la suite car avec internet, on est sur de rien
            with raisin.Printer("connection to %s..." % self.name, signature=signature):# on dit ce que l'on fait
                self.dbx = dropbox.Dropbox(self.access_token)               # on se lie theoriquement
                self.dbx.users_get_current_account()                        # releve les informations du compte pour etre certain que la connection est bonne
                self.linked = True                                          # si la connection n'a pas echouer
                self.last_connection = time.time()                          # on le note
        except Exception as e:                                              # si il y a une erreur
            self.linked = False                                             # est bien on s'assure que tout le monde soit bien au courant
            raise e from e                                                  # puis on le cri bien fort

    def get_free_space(self, signature=None):
        """
        recupere l'espace disponible en octet
        """
        self.connect()
        with raisin.Printer("Get free space of '%s'..." % self.name, signature=signature) as p:# on annonce que l'on va faire une operation risque
            u = self.dbx.users_get_space_usage()                            # recuperation de toutes les informations
            free_space = u.allocation.get_individual().allocated - u.used   # exctraction de la bonne info
            p.show("There remains %d Mo." % (free_space*1e-6))              # on l'affiche pour la metre en forme
            return free_space

    def send(self, data, filename, signature=None):
        """
        envoi sur ce dropbox un fichier name /filename
        contenant data
        """
        assert type(data) is bytes, "type(data) must be 'bytes', %s is not 'bytes': it is %s" % (data, type(data))
        assert len(data) <= 2**30, "data must be <= a gibioctet"
        assert type(filename) is str, "type(filename) must be 'str', %s is not 'str': it is %s" % (filename, type(filename))

        with raisin.Lock(self.name, timeout=600, signature=signature):      # on s'assure que l'access a dropbox soit exclusif
            self.connect()                                                  # d'abort il faut que l'on soit connecte
            with raisin.Printer("sending %s to %s..." % (filename, self.name), signature=signature) as p:# comme cette operation peut prendre du temps, on previent l'utilisateur
                chunk_size = 1024*1024                                      # taille maximum de chaque petits paquets
                taille = len(data)                                          # c'est la taille totale du fichier
                if taille <= chunk_size:                                    # si on ne nous demande pas d'envoyer un trop gros objet
                    self.dbx.files_upload(data, os.path.join("/", filename))# on l'envoi directement
                else:                                                       # dans le cas ou il est un peu concequant
                    upload_session_start_result = self.dbx.files_upload_session_start(b"")# on en ouvre un fichier vide
                    cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=0)# que l'on va remplir petit a petit
                    commit = dropbox.files.CommitInfo(os.path.join("/", filename))# ce fichier est mis a la base
                    for index in range(0, taille-chunk_size, chunk_size):   # pour chaque petit sous paquet
                        cursor.offset = index                               # on continue le fichier au bon endroit
                        self.dbx.files_upload_session_append(data[index:index+chunk_size], cursor.session_id, cursor.offset)# on envoi le petit paquet
                        p.show(str(round(100*index/taille, 1))+"%")         # on indique a l'utilisateur ou l'on en est
                    cursor.offset = index+chunk_size                        # puis on se replace au bon endroit
                    self.dbx.files_upload_session_finish(data[cursor.offset:], cursor, commit)# on fait apparaitre le fichier dans dropbox

    def load(self, filename, signature=None):
        """
        deserialise l'objet '/filename'
        'name' est donc le nom du fichier sur dropbox
        retourne l'objet en cas de reussite
        retourne None en cas d'erreur
        """
        assert type(filename) is str, "type(filename) must be 'str', %s is not 'str': it is %s" % (filename, type(filename))

        self.connect()                  # on commence par ce connecter
        with raisin.Printer("loading %s from %s..." % (filename, self.name), signature=self.signature):# puis on dit ce que l'on fait
            return self.dbx.files_download(os.path.join("/", name))[1].content# on recupere le contenu du fichier

    def remove(self, filename, signature=None):
        """
        supprime le fichier '/name'
        'name' est donc le nom du fichier dans dropbox
        """
        assert type(filename) is str, "type(filename) must be 'str', %s is not 'str': it is %s" % (filename, type(filename))

        with raisin.Lock(self.name, timeout=60, signature=signature):   # avant de supprimer le fichier, il faut en avoir l'acces exclusif
            self.connect()                                              # une fois cette etape valide, on tente une connection
            with raisin.Printer("deleted %s from %s..." % (filename, self.name), signature=signature):# puis on previent que l'on supprime
                self.dbx.files_delete(os.path.join("/", filename))      # puis on tente la suppresion

    def is_free(self, signature=None):
        """
        retourne True si il n'y a pas ou plus de verrou
        retourne False si l'acces est pris
        """
        return raisin.Lock(self.name, signature=self.signature).is_free()

    def ls(self, signature=None):
        """
        retourne la liste de tous les fichiers
        """
        self.connect()                              # on a pas besoin de verrou pour aller lire le nom des fichiers
        with raisin.Printer("get all name from %s..." % self.name, signature=signature):# on previent quand meme de ce que l'on va faire
            return [e.name for e in self.dbx.files_list_folder("").entries]

    def __repr__(self):
        return "dropbox %s" % self.name

    def __str__(self):
        return self.__repr__()


if dropbox is not None:
    servers = [
    Dropbox("robin", "iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x"),
    Dropbox("sylvain", "I5SSyJu4YeIAAAAAAAAVNwvsyPf7NRROs4BvKY6GcqWhYfnRPnBXNEpKFkYGszBH"),
    Dropbox("louis", "ZJ9ccoM5wlAAAAAAAAAALfsexhJlBhuidc_t5_IIY5kFGikSars-KNnL9FTg85XP"),
    Dropbox("winona", "n9a3sVc71GAAAAAAAAAAEuhu2Zjm-l0vFkde4lZ0x5QFI3c-Chiso-yz2f8PMwjp"),
    Dropbox("francois", "tPrWxXGOVYcAAAAAAAAAm_3Bjqv491Ea6PJhYYvNhbEgYMf-KkevfZj8bptppgOm"),
    Dropbox("paul", "6xsftcuTrbAAAAAAAAABxvCD231UOr3LtqtnGdzXVocQpVfOeUYMw9BXfqnIwqIb")
    ]
else:
    servers = []
