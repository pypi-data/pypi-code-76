# -*- coding: utf-8 -*-
r"""
This module contains the keywords for the factory pattern classes used in this project.
"""
# =======================Creating Plotmode===========================
PAPERPRB = 'paperPRB'
DEFAULTLATEX = 'defaultLatex'
PRESENTATION = 'presentation'
YAML = 'yaml'
# =======================Specific Options for Plotmode===============

# Options for defining the Figure. The inputs are designed in a way that only figures within the allowed rules depending
# on the format can be created.
# -------------------------------------------------------------------
EXTENTTYPE = 'extent'
NARROW = 'narrow'
BROAD = 'broad'
TINY = 'tiny'
# figure height in inches, input type has to be float
FIGUREHEIGHT = 'figheight'
# -------------------------------------------------------------------
# Gridspec defines number of subplots with number of rows and number of columns data is provided as Tuple
GRID = 'grid'
