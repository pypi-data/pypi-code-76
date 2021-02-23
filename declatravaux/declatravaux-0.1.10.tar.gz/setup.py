# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['declatravaux']

package_data = \
{'': ['*'], 'declatravaux': ['static/*', 'ui/*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0', 'PyQt5==5.14', 'keyring>=21.2.0,<22.0.0']

setup_kwargs = {
    'name': 'declatravaux',
    'version': '0.1.10',
    'description': 'Utilitaire de transmission de déclarations issues de la plateforme http://www.reseaux-et-canalisations.ineris.fr/',
    'long_description': '# DéclaTravaux\n\nDéclaTravaux est un utilitaire de télétransmission des déclarations de projet de travaux (DT), des déclarations d\'intention de commencement de travaux (DICT) et des avis de travaux urgents (ATU).\n\nLe logiciel, développé dans le langage Python, est disponible sous la licence libre CeCILL (http://www.cecill.info/).\n\n## Contexte\n\nLorsque des travaux sont envisagés à proximité de réseaux ou canalisations, le maître d\'ouvrage et/ou l\'exécutant des travaux doit déclarer ce projet de travaux aux exploitants des réseaux concernés.\n\nPour ce faire, il doit obligatoirement consulter la plateforme http://www.reseaux-et-canalisations.ineris.fr/ : le déclarant y indique l\'emprise géographique des travaux prévus, et, en retour, le téléservice lui propose de télécharger une archive contenant les déclarations à souscrire auprès des différents exploitants concernés.\n\nIl appartient ensuite au déclarant d\'envoyer par courriel les différentes déclarations ainsi téléchargées aux exploitants identifiés.\n\n## Objet du logiciel\n\nLe présent logiciel a pour objet d\'automatiser l\'envoi par courriel des différentes déclarations.\n\nPar un traitement de l\'archive issue du téléservice, il extrait les informations relatives aux exploitants concernés et à leurs coordonnées, et procède à l\'envoi des déclarations correspondant à chacun d\'eux.\n\n## Utilisation\n\nLors du premier lancement du logiciel, il convient de renseigner les informations suivantes (bouton `Paramètres`) :\n* Configuration :\n    * Répertoire de recherche : répertoire dans lequel le logiciel va automatiquement rechercher les archives issues du téléservice ;\n    * Repertoire de traitement : répertoire dans lequel les archives sont conservées après avoir été traitées.\n* Courriels :\n    * Adresse électronique : adresse éléectronique utilisée pour envoyer les déclarations aux exploitants ;\n    * Mot de passe : mot de passe de connexion au serveur SMTP correspondant à l\'adresse électronique ;\n    * Adresse du serveur SMTP ;\n    * Port du serveur SMTP ;\n    * Nom de l\'expéditeur : identité utilisée en signature des courriels.\n\nUne fois ces informations renseignées, le logiciel va automatiquement rechercher des archives ZIP téléchargées sur le téléservice ; s\'il n\'en détecte aucune, il propose à l\'utilisateur de sélectionner manuellement une archive.\n\nUne fois le choix de l\'archive confirmé par l"utilisateur, le logiciel :\n1. extrait les informations relatives aux exploitants contenues dans l\'archive (notamment dans le fichier «\xa0*_description.xml\xa0») ;\n2. associe à chaque exploitant la déclaration correspondante (au format PDF) ;\n3. se connecte au serveur de messagerie de l\'utilisateur ;\n4. envoie un courriel à chaque exploitant, contenant en pièce jointe les fichiers requis ;\n5. envoie un courriel récapitulatif à l\'utilisateur, confirmant l\'envoi des différents courriels.\n\n## Bibliothèques tierces / Dépendances\n\nLe logiciel utilise les bibliothèques tierces suivantes :\n* keyring, disponible sous les licences MIT et PSF (https://github.com/jaraco/keyring) ;\n* PyPDF2, écrite par la société [Phaseit](http://phaseit.net/), disponible sous la licence BSD modifiée (http://mstamy2.github.io/PyPDF2/) ;\n* PyQt5, disponible sous la licence GPL (https://www.riverbankcomputing.com/software/pyqt/).',
    'author': 'Pierre Gobin',
    'author_email': 'contact@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
