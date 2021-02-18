from setuptools import setup, find_packages

setup(name='dmmf',
      version='0.1',
      description='Model Management',
      long_description='Darwin Model Management Framework',
      url='https://github.com/Direct-Line-Group/darwin-ds-dmmf-stub',
      author='Yuriy Akopov',
      author_email='yuriy.akopov@directlinegroup.co.uk',
      packages=find_packages(),
      package_data={'dmmf': []},

      install_requires=[],
      scripts=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
