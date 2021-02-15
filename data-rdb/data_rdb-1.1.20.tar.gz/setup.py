from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).resolve().parent

with open(this_directory/'README.md', encoding='utf-8') as f:
    readme = f.read()

with open(this_directory/'VERSION') as version_file:
    version = version_file.read().strip()

setup(name='data_rdb',
      version=version,
      description='DataDBS for RethinkDB',
      url='http://www.gitlab.com/dpineda/data_rdb',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['data_rdb'],
      install_requires=['datadbs',"rethinkdb"],
      include_package_data=True,      
      package_dir={'data_rdb': 'data_rdb'},
      package_data={
          'data_rdb': ['../doc', '../docs', '../requeriments.txt', '../tests']},
      long_description=readme,
      long_description_content_type='text/markdown',
      zip_safe=False)
