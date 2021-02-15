# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'lesana'
copyright = "2020, Elena Grandi"
author = "Elena ``of Valhalla''"

# The full version, including alpha/beta/rc tags
release = '0.8.1'
# The major project version
version = '0.8'

# compatibility with sphinx 1.8 on buster
master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

man_pages = [
    (
        'man/lesana', 'lesana',
        'manages collection inventories',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-edit', 'lesana-edit',
        'edits an existing lesana entry',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-export', 'lesana-export',
        'export data from one lesana collection to another',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-index', 'lesana-index',
        'Index some entries',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-init', 'lesana-init',
        'initialize a lesana collection',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-new', 'lesana-new',
        'create a new lesana entry',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-rm', 'lesana-rm',
        'remove an entry from a lesana collection',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-search', 'lesana-search',
        'search inside a lesana collection',
        'valhalla@trueelena.org', 1
    ),
    (
        'man/lesana-show', 'lesana-show',
        'show a lesana entry',
        'valhalla@trueelena.org', 1
    ),
]
