#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import raisin

__all__ = ["CsvFileReader"]


def _find_delimiter_quotechar(file_path, delimiter, quotechar):
    """
    retourne le separateur et le quotechar le plus logic pour separer les donnees 'datas'.
    'datas (STR)' est le contenu direct d'un fichier csv, sans mise en forme prealable
    cherche les separateurs parmis:
        -"\t"
        -","
        -";"
        -" "
    cherche les quotechar parmis:
        -"'"
        -'"'
    """
    raise NotImplementedError

class CsvFileReader:
    """
    permet de lire un fichier csv et retourne un dictionaire de ce dernier
    """
    def __init__(self, file, encoding, signature, **kwargs):
        self.file_path = file
        self.encoding = encoding
        self.signature = signature
        self.delimiter = kwargs.get("delimiter", None)
        self.quotechar = kwargs.get("quotechar", None)
        assert self.quotechar in (None, "'", '"'), "les quotechar ne peuvent etre que ' ou \", pas %s" % self.quotechar
        if (not self.delimiter) or (not self.quotechar):            # si le separateur n'est pas specifier ou que le separateur de texte ne l'est pas non plus
            self.delimiter = _find_delimiter_quotechar(self.file_path, self.delimiter, self.quotechar)# on va essayer de le choisir intelligement
        self.file = open(self.file_path, "r", encoding=encoding)    # pointeur vers le fichier en lecture

    def close(self):
        """
        ferme le fichier
        n'a aucun effet si le fichier est deja ferme
        """
        with raisin.Printer("closing file %s..." % self.file_path, signature=self.signature):
            return self.file.close()

    def __iter__(self):
        """
        retourne peu a peu chaque ligne sous forme de liste
        """
        while 1:                                                    # on ne s'arrette jamais de lire le csv
            ligne_str = self.file.readline()                        # tant qu'il reste des lignes a lire
            if ligne_str == "":                                     # c'est a dire tant que l'on est par arrive a la fin
                break                                               # si tel est le cas, on sort du generateur
            ligne_str = ligne_str[:-1]                              # on supprime le '\n' present a la fin de la ligne
            liste = []                                              # initialisation de la liste
            in_str = False                                          # devient True si l'on est en plein milieu d'une chaine de caractere
            mot = ""                                                # c'est le mot en cours d'analyse
            echappement = 0                                         # c'est le nombre de caractere d'echappement
            for car in ligne_str:                                   # pour chaque caracteres
                if car == self.delimiter and not in_str:            # si on arrive sur un separateur
                    try:                                            # on va tenter de transformer en objet
                        data = eval(mot)                            # python, la suite de caractere precedente
                    except:                                         # si ca echoue une premiere fois
                        try:                                        # on essai une deuxieme fois
                            data = eval(mot.replace(",", "."))      # en remplaceant les virgules par des points (pour la gestion des nombres)
                        except:                                     # si meme ca ca ne fonctionne pas
                            data = mot                              # alors, on garde l'objet en str, sans changer son typage
                    liste.append(data)                              # alors on passe au paquet suivant
                    mot = ""                                        # on reinitialise tout pour la suite
                    continue                                        # puis on passe directement au caractere suivant
                if car == self.quotechar and not in_str:            # si l'on entre dans une chaine de caractere
                    assert mot == "", "une chaine de caractere n'est pas precede d'un separateur"# on fait une petite verification
                    in_str = True                                   # si la verification est bonne, on sait que l'on entre dans une chaine
                elif car == "\\" and in_str:                        # si on est dans une chaine et qu'il y a un caractere d'echappement
                    echappement = 1-echapement                      # alors on change la parite de echapement
                elif car == self.quotechar and in_str and not echappement:# si on arrive a la fin d'une chaine
                    echappement = 0                                 # alors on remet les compteurs a 0 pour le caractere d'echappement
                    in_str = False                                  # puis on signal que l'on est plus dans une chaine
                mot += car
            yield liste

    def read(self):
        """
        retourne un dictionaire de ce csv
        """
        return [l for l in self]

    def __enter__(self):
        """
        permet d'utiliser le mot clef 'with'
        """
        return self

    def __exit__(self, *args):
        self.close()    