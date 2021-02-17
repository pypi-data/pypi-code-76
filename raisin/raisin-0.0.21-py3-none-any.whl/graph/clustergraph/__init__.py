#!/usr/bin/env python3

"""
|=================================|
| Graphe particulier qui modelise |
| un cluster de travail internet. |
|=================================|

* Modelise les differents noeud de connections:
    - Les machines qui appartiennent au reseau.
    - Les routeurs (box) pour les connections entrantes et sortantes.
    - Le noeud qui represente internet, le reseau wan.
* Modelise aussi les connections, melange entre les cables et les cartes
reseau qui permentent des connections avec un debit limite.
"""

__all__ = ["router", "computer", "connection", "network", "load"]
