from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(name='bloggo',
      version='1.1.0',
      description='A blog-oriented static site generator',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/askonomm/bloggo',
      author='Asko Nõmm',
      author_email='asko@askonomm.com',
      license='MIT',
      packages=['bloggo'],
      zip_safe=False)
