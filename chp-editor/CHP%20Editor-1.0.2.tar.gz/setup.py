from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.2'
DESCRIPTION = 'Classroom Assistant'
LONG_DESCRIPTION = 'A package to have a desktop app to make your homework easier.'

setup(
    name="CHP Editor",
    version=VERSION,
    author="ArMafer",
    author_email="<angelshaparro@outlook.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui'],
    keywords=['python', 'classroom', 'homework', 'music player', 'calculator', 'wikipedia'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)