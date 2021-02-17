from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='plot-wav',
    packages=['plot_wav'],
    install_requires=['argparse', 'numpy', 'matplotlib', 'librosa', 'scipy', 'wave'],

    version='0.1.0',
    license='MIT',

    author='Tatsuya Abe',
    author_email='abe12@mccc.jp',

    url='https://github.com/averak/plot-wav',

    desription='A tool for drawing wav files with various acoustic transformations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='wave spectrogram MFCC audio',

    entry_points={
        'console_scripts': [
            'plot-wav=plot_wav.core:main',
        ]
    },

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
