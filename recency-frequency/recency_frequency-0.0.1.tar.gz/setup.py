# setup.py

from setuptools import setup

setup(
    name='recency_frequency',
    version='0.0.1',
    description='Recency + Frequency',
    py_modules=['recency_frequency'],
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'pandas', #==1.2.1,
        'xlrd', #==2.0.1,
        'openpyxl', #==3.0.6
        ],
)

# API token 
#pypi-AgEIcHlwaS5vcmcCJGEyMmExMmUzLTZiMWQtNDgxYi04YjljLWI2NWQwZGY2ZjJlZgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYg60Emfo1jQrvRf9Pd2ECwCDjINW50nzPAiHEUGZU_6ao