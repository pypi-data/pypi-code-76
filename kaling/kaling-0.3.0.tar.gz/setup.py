import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.3.0'
PACKAGE_NAME = 'kaling'
AUTHOR = 'andyyeyeye'
AUTHOR_EMAIL = 'andyye.jongcye@gmail.com'
URL = 'https://github.com/idev-develop/KakaoLink-Python'

LICENSE = 'MIT License'
DESCRIPTION = 'pure python library for sending kakaolinks'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf8")
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'requests',
      'bs4',
      'pycryptodome'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
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