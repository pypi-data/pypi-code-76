'''
setup.py
'''
from os import path
from setuptools import setup
import temperature2mqtt

THIS_DIRECTORY = path.abspath(path.dirname(__file__))

with open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='temperature2mqtt',
    version=temperature2mqtt.__version__,
    description='Read DHT22 sensor from RPI and publish to mqtt..',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/JonasPed/temperature2mqtt',
    author='Jonas Pedersen',
    author_email='jonas@pedersen.ninja',
    license='Apache 2.0',
    packages=['temperature2mqtt'],
    install_requires=['paho-mqtt']
    )
