"""
:copyright 2012 CreaLibre (Monterrey, MEXICO), all rights reserved.
:contact http://www.crealibre.com/ -- mailto:info@crealibre.com

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), license is LGPL.
:contact: https://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
# flake8: noqa

import pathlib

FDS_CSS = pathlib.Path(__file__).parent.joinpath('data', 'css')

STYLESHEETS = [
    data('css/bootstrap.min.css'),
    data('cubes.bootstrap.css'),
    data('cubicweb.pictograms.css'),
]

for path in FDS_CSS.rglob("*.css"):
    file_path = path.relative_to(FDS_CSS)
    if "bootstrap" not in file_path.name:
        STYLESHEETS.append(data(f"css/{file_path}"))

CW_COMPAT_STYLESHEETS = [data('cubes.bootstrap.cw_compat.css')]

JAVASCRIPTS.extend((data('js/bootstrap.min.js'),
                    data('cubes.bootstrap.js'),
                    data('cubes.squareui.js')))
