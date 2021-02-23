from os import path
from setuptools import setup
from setuptools import find_packages
# from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt')) as f:
    reqs = f.read().rstrip().splitlines()
print(reqs)
setup(
     install_requires=reqs,
     
     packages = find_packages(exclude=['contrib', 'docs', 'tests']),
     package_data={
   'build_data': ['*'],     # All files from folder A
   'EBMPICO': ['*'], 
   'lstm_crf': ['*'], 
   'LSTMCRFApp': ['*'], 
   'pico': ['*'],  #All text files from folder B
   'tags': ['tag.py']
   },
     entry_points={
        "console_scripts": [
            "pico = pico.__main__:main"
        ]
    },
    scripts=['manage.py'],

)