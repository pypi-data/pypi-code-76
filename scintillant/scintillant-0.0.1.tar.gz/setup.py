from setuptools import setup

# get key package details from scintillant/__version__.py
about = {
    '__title__': 'scintillant',
    '__description__': 'Fast bot creating framework',
    '__version__': '0.0.1',
    '__author__': 'Niel Ketov',
    '__author_email__': 'ketov-x@yandex.ru',
    '__url__': 'https://code.tatar.ru/projects/LILIYA/repos/scintillant',
    '__license__': 'Apache 2.0'
}  # type: ignore

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=[
        'scintillant',
        'scintillant.apimodels',
        'scintillant.apimodels.models',
        'scintillant.apimodels.db',
        'scintillant.controllers'
    ],
    include_package_data=True,
    python_requires=">=3.9.*",
    install_requires=['tqdm', 'werkzeug', 'requests', 'GitPython'],
    license=about['__license__'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'scintillant=scintillant.entry_points:main',
            'snlt=scintillant.entry_points:main'
        ],
    },
    keywords='package development template'
)
