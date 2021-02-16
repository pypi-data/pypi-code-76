import setuptools

VERSION = '3.0.0'

PKG_NAME = 'behalearn'
AUTHOR = 'Behametrics'
AUTHOR_EMAIL = 'tp2018tim4@gmail.com'
with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()
URL = 'https://gitlab.com/behametrics/behalearn'

setuptools.setup(
    name=PKG_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=(
        'Library for processing and visualizing behavioral biometric data'),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'seaborn',
        'bokeh'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
