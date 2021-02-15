from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='dislash.py',
    version='0.1.7',
    description='A python wrapper for discord slash-commands',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EQUENOS/dislash.py',
    author='EQUENOS',
    author_email='equenos1@gmail.com',
    keywords='discord, discord-api, slash-commands',
    packages=['dislash'],
    python_requires='>=3.6, <4',
    install_requires=requirements,
    project_urls={
        'Documentation': 'https://dislashpy.readthedocs.io/en/latest',
        'Bug Reports': 'https://github.com/EQUENOS/dislash.py/issues',
        'Source': 'https://github.com/EQUENOS/dislash.py',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)