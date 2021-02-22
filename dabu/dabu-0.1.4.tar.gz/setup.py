from setuptools import setup
import pathlib

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Financial and Insurance Industry',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.6',
    "Programming Language :: Python :: 3.7",
    'Programming Language :: Python :: 3.8',
    "Programming Language :: Python :: 3.9"]

# The directory containing this file
#HERE = pathlib.Path(__file__).parent
#
## The text of the README file
#README = (HERE / "README.md").read_text()

setup(
    name='dabu',
    version='0.1.4',
    description='Dabu facilita la obtencion de datos bursatiles de la Bolsa Mexiana de Valores',
#    long_description=open('README.md').read(),
    author='Carlos Crespo Elizondo',
    author_email='carlos@dabu.com',
    license='BSD 3',
    classifiers=classifiers,
    keywords='bmv, Bolsa Mexicana de Valores, Analisis fundamental, Precios de cierre',
    packages=['dabu'],
    install_requires=["pandas", "requests"]
)
