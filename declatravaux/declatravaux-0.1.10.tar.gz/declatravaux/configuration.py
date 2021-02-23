#!/usr/bin/env python

import configparser
import platform
import os
import keyring

from pathlib import Path, PurePath


class Configuration:

    def __init__(self):

        config = configparser.ConfigParser()
        config.optionxform = str

        # Le chemin du fichier de configuration dépend du système d'exploitation
        self.config_file_path = self.get_config_file_path()

        # Si le fichier de configuration n'existe pas, on le crée

        if not Path(self.config_file_path).exists():
            self.create_config_file(self.config_file_path)

        # On charge les informations
        config.read(self.config_file_path)

        self._parameters = config
        self._password = keyring.get_password('declatravaux', os.getlogin())

    def __getitem__(self, key):

        if key in ('PremierLancement', 'RepertoireDeclarations', 'RepertoireRecherche'):
            return self._parameters['Configuration'][key]

        elif key in ('AdresseElectronique', 'ServeurSMTP', 'PortServeurSMTP', 'NomExpediteur'):
            return self._parameters['Courriels'][key]

    def __setitem__(self, key, value):
        self.parameters = {key: value}

    @staticmethod
    def get_config_file_path():
        """
        Retourne le chemin du fichier de configuration de l'application
        """
        chemin_fichier = ''

        # Le chemin du fichier de configuration dépend du système d'exploitation
        if platform.system() == 'Linux':

            try:
                config_dir = os.environ['XDG_CONFIG_HOME']
            except KeyError:
                config_dir = PurePath(Path.home(), '.config/')
            finally:
                config_file_path = PurePath(config_dir, 'declatravaux', 'declatravaux.conf')

        elif platform.system() == 'Windows':
            config_file_path = PurePath(os.environ['AppData'], 'DeclaTravaux', 'DeclaTravaux.conf')

        return config_file_path

    @staticmethod
    def create_config_file(file_path):
        """
        Fonction créant le fichier de configuration par défaut
        """

        config = configparser.ConfigParser()
        config.optionxform = str

        work_dir = Path(Path.home(), 'Documents', 'DéclaTravaux')
        search_dir = ''

        # Par défaut, les archives sont recherchées dans le répertoire « Téléchargements »
        # Si ce dernier n'est pas trouvé, elles sont recherchées dans le dossier de l'utilisateur
        if platform.system() == 'Linux':

            try:
                search_dir = Path(os.environ['XDG_DOWNLOAD_DIR'])

            except KeyError:
                search_dir = Path(Path.home(), 'Téléchargements')

                if not search_dir.exists():
                    search_dir = Path.home()

        elif platform.system() == 'Windows':
            search_dir = Path(Path.home(), 'Downloads')

        config['Configuration'] = {'PremierLancement': '1',
                                   'RepertoireDeclarations': str(work_dir),
                                   'RepertoireRecherche': str(search_dir)}

        config['Courriels'] = {'AdresseElectronique': '',
                               'ServeurSMTP': '',
                               'PortServeurSMTP': '',
                               'NomExpediteur': ''}

        Path(file_path.parent).mkdir(exist_ok=True)

        with open(file_path, 'w') as configFile:
            config.write(configFile)

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, param_dict):

        config = self._parameters

        # Le paramètre PremierLancement est automatiquement affecté de la valeur 0
        config['Configuration']['PremierLancement'] = '0'

        # On boucle les paramètres donnés en arguments
        # S'ils correspondent aux paramètres attendus, on modifie les paramètres
        for parameter, value in param_dict.items():

            if parameter in ('RepertoireDeclarations', 'RepertoireRecherche'):

                config['Configuration'][parameter] = value

            elif parameter in ('AdresseElectronique',
                               'ServeurSMTP', 'PortServeurSMTP', 'NomExpediteur'):

                config['Courriels'][parameter] = value

        # Le fichier de configuration est sauvegardé
        with open(self.config_file_path, 'w') as configFile:
            config.write(configFile)

        self._parameters = config

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        keyring.set_password('declatravaux', os.getlogin(), value)
        self._password = value
