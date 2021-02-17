#!/usr/bin/env python3

"""
|=========================|
| Human Machine Interface |
|=========================|

Interaction avec l'utilisation.
1) Permet de lui poser question soit directement
dans le terminal ou bien si tkinter est installe,
Un interface graphique plus poussee est employée.
2) Permet aussi de lui presenter les choses de facon 
humainement lisibles. Afin de lui presenter
les donnees de facon lisible.
"""

__all__ = ["dialog", "theme", "checks", "pathmanager", "schedules"]

import logging
try:
    import tkinter
    import tkinter.messagebox as messagebox
    import tkinter.ttk as ttk
except ImportError:
    logging.warn("'tkinter' failed to import, no possibility to have interface graphical.")
    tkinter = None
    messagebox = None
    ttk = None
