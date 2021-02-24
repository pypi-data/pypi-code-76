from setuptools import setup



setup(name='StockStalker',
      version='0.1',
      description='easy to use, robust and quick stocks package',
      long_description="README.md",
      long_description_content_type='text/markdown',
      url='https://github.com/RockoonTechnologies/StockStalker',
      author='Meepers',
      author_email='rockoontech@gmail.com',
      license='MIT',
      packages=['StockStalker'],
      install_requires=[
          'beautifulsoup4==4.9.3',
          'pandas==1.1.5',
          'requests==2.25.1',
          'lxml==4.6.2',
          'Munch==2.5.0'
      ],
      zip_safe=False)
