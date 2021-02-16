# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '2.2.11'

setup(
    name='camcomskin.padova',
    version=version,
    description="CCIAAPD Plone Theme Agid",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
    ],
    keywords='web zope plone theme',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/PloneGov-IT/camcomskin.padova',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['camcomskin'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'collective.contentleadimage',
        'collective.editablemenu == 0.2.1',
        'collective.portletpage',
        'Products.ContentWellPortlets == 4.3.0',
        'redturtle.portlet.collection',
        'redturtle.smartlink',
        'redturtle.tiles.management<1.0.0',
        'rer.portlet.advanced_static',
        'rer.portlet.er_navigation',
        'collective.tiles.advancedstatic<1.1.1',
        'collective.tiles.collection<1.0.0',
        'z3c.jbot',
        'quintagroup.formlib.captcha',
        # Non metto come dipendenza direttamente pd.prenotazioni, perché
        # sennò non funziona l'override delle traduzioni, e z3c.pdftemplate
        # serve per l'override di una vista "prenotazione_print_pdf"
        'z3c.pdftemplate',
        'redturtle.video',
        'plone.app.imaging',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
