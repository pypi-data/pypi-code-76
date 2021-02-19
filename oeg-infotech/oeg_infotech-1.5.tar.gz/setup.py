"""For pypi.org upload."""
import setuptools

LONG = """
# oeg.infotech.xml

Library for OrgEnergoGaz Infotech xml processing
"""

setuptools.setup(
  name='oeg_infotech',
  version='1.5',
  author='Vitaly Bogomolov',
  author_email='mail@vitaly-bogomolov.ru',
  description='Library for OrgEnergoGaz Infotech xml processing',
  long_description=LONG,
  long_description_content_type="text/markdown",
  url='https://github.com/vb64/oeg.infotech.xml',
  packages=['oeg_infotech', 'oeg_infotech.codes'],
  download_url='https://github.com/vb64/oeg.infotech.xml/archive/v1.5.tar.gz',
  keywords=['python', 'OrgEnergoGaz', 'Infotech', 'IUST', 'xml'],
  classifiers=[
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
