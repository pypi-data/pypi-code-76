import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'Pakiet_Michala'
AUTHOR ='Michal Mi'
AUTHOR_EMAIL = 'm.p.milinski@gmail.com'
URL = 'https://pypi.python.org/pypi'

LICENSE = 'MIT'
DESCRIPTION = 'Kilka przydatnych funkcji zwracających czas w różnych postaciach'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'scrapeasy'
]

setup(name=PACKAGE_NAME,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )