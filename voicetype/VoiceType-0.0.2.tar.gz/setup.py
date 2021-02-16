from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A package to type using your voice.You can report errors or make suggestions on my github: https://github.com/Friend1975/VoiceType.git'

# Setting up
setup(
    name="VoiceType",
    version=VERSION,
    author="Friend1975",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['keyboard', 'SpeechRecognition'],
    keywords=['python', 'voice', 'typing', 'speech recognition'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)