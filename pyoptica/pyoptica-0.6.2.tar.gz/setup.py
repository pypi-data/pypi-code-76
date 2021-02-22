import codecs
import os.path

from setuptools import setup

REQUIREMENTS = [
    'astropy', 'matplotlib', 'numpy', 'scipy'
]

PROJECT_URLS = {
    'Blog': 'https://pyoptica.gitlab.io/pyoptica-blog/'
}


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def readme():
    """
    This function just return the content of README.md
    """
    with open('README.md') as f:
        return f.read()


setup(
    name='pyoptica',
    version=get_version("pyoptica/__init__.py"),
    description='Tools to apply light propagation algorithms',
    long_description_content_type='text/markdown',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='fourier_optics light_propagation ',
    url='https://gitlab.com/pyoptica',
    project_url=PROJECT_URLS,
    author='Maciej Grochowicz, Michal Miler',
    author_email='pyoptica@protonmail.com',
    license='MIT License',
    packages=['pyoptica', 'pyoptica.optical_elements'],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    package_data={'': ['data/logos/*.png']},
    zip_safe=False,
)
