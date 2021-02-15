from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(name='bloggo',
      version='1.1.2',
      description='A blog-oriented static site generator',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/askonomm/bloggo',
      author='Asko Nõmm',
      author_email='asko@askonomm.com',
      license='MIT',
      packages=['bloggo'],
      package_dir={'': '.'},
      classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.9'
      ],
      install_requires=[
            'pybars3>=0.9.7',
            'watchgod>=0.7',
            'mock>=4.0.3',
            'Markdown>=3.3.3'
      ],
      zip_safe=False)
