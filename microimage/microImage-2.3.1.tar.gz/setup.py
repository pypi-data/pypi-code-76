import os
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "microImage",
    version = "2.3.1",
    author = "Vivien WALTER",
    author_email = "walter.vivien@gmail.com",
    description = ("Python module to open common types of image used in microscopy."),
    license = "GPL3.0",
    keywords = ["microscopy","image","open"],
    url = "https://github.com/vivien-walter/microImage",
    download_url = 'https://github.com/vivien-walter/microImage/archive/v_2.3.1.tar.gz',
    packages=['microImage'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.2',
    install_requires=[
        'bottleneck',
        'ffmpeg-python',
        'matplotlib',
        'numpy',
        'Pillow',
        'pims',
        'scikit-image',
    ]
)
