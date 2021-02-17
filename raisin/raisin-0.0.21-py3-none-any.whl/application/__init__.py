#!/usr/bin/env python3

"""
|========================================================|
| Gestion de la partie application logicielle de raisin. |
|========================================================|

1) Le partage des ressources
-C'est dans ce sous-module que l'on gere
les ressources que l'on offre a la communautee.
2) La configuration
-C'est aussi ici que l'on interagit graphiquement
avec l'utilisateur afin de tout configurer.
-On l'aide a naviger dans les repertoires.
3) persistance des donnes
-Enfin, c'est ici que l'on s'occupe d'enregistrer les
parametres et certaines donnees.
"""

__all__ = ["hmi", "settings", "install", "uninstall"]
