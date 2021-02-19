#!/usr/bin/env python

from distutils.core import setup

# setup(name='nn2',
#       version='1.0.50',
#       description='nn2 lib',
#       author='João Neto',
#       author_email='joao.filipe.neto@gmail.com',
#       packages=['nn2'],
# )


setup(name='dl2050nn',
      packages=['dl2050nn'],
      version='1.0.50',
      license='MIT',
      description='NN python lib',
      author='João Neto',
      author_email='joao.filipe.neto@gmail.com',
      keywords=['Neural Networks'],
      url='https://github.com/jn2050/nn2',
      download_url='https://github.com/jn2050/nn2/archive/v_1_0_50.tar.gz',
      # install_requires=[
      #       'pathlib',
      #       'zipfile',
      #       'json',
      #       'socket',
      #       'smtplib',
      #       'ssl',
      #       'boto3',
      #       'asyncpg',
      #       '',
      # ],
      classifiers=[
            'Development Status :: 4 - Beta',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
      ],
)
