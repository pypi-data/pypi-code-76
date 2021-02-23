#!/usr/bin/env python

import calendar
import re
from pathlib import Path


class Archives:

    def __init__(self):
        # On définit le format de fichier .zip attendu
        self.archiveRegex = re.compile(r'[0-9]{13}[A-Z]([0-9][0-9])?_(DT|DICT|DDC|ATU).zip')
        self.archivesList = list()

    def search(self, search_dir):
        """
        Recherche, dans le répertoire indiqué en premier paramètre,
        les fichiers .zip dont les noms correspondent à l'expression régulière donnée en second paramètre.
        """
        if Path(search_dir).exists():
            # On liste les fichiers contenus dans le dossier de recherche
            files_list = Path(search_dir).iterdir()
            # On filtre la liste pour n'obtenir que les fichiers correspondant à l'expression régulière
            self.archivesList = [Declaration(f) for f in files_list if re.match(self.archiveRegex, f.name)]

            self.archivesList.sort(key=lambda declaration: declaration.fileName)

        return self.archivesList


class Declaration:

    def __init__(self, path):
        path = Path(path)

        self.fileName = path.name
        self.filePath = path.resolve()
        self.dType = self.get_type(path)
        self.numero = self.get_numero(path)
        self.date = self.get_date(path)
        self.name = self.get_name(path)

    def get_name(self, path):
        """
        Retourne l'intitulé complet de la déclaration dans un format lisible
        """
        return f'{self.get_type(path)} n° {self.get_numero(path)} du {self.get_date(path)}'

    def get_type(self, path):
        """
        Retourne le type de déclaration
        """

        declaration_codes = {'DT': 'DT', 'DICT': 'DICT',
                             'DDC': 'DT-DICT conjointe', 'ATU': 'ATU'}

        file_name = path.stem
        return declaration_codes[file_name.split('_')[1]]

    def get_numero(self, path):
        """
        Retourne le numéro de la déclaration
        """
        file_name = path.stem
        return file_name.split('_')[0][8:].lstrip('0')

    def get_date(self, path):
        """
        Retourne la date de la déclaration
        """
        file_name = path.stem
        day_of_month = file_name[6:8].lstrip('0')
        month = calendar.month_name[int(file_name[4:6])]
        year = file_name[0:4]
        day = calendar.day_name[calendar.weekday(int(year), int(file_name[4:6]), int(day_of_month))]

        return f'{day} {day_of_month} {month} {year}'
