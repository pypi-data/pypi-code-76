from setuptools import setup, find_packages

setup(name='track_analyzer',
      version=0.0,
      description=" Python package to analyze cel trajectories.",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      author="Arthur Michaut",
      license="GPL",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
      python_requires='>=3.6',
      )
