from setuptools import setup, find_packages

setup(name='dynaconfig',
    version = '0.4',
    description="Dynamic config tree readerer.",
    long_description="Write dynamic configurations files with values that contain python expressions and can reference other configuration parameters.",
    author='C.D. Clark III',
    url='https://github.com/CD3/dynaconfig',
    license="MIT License",
    platforms=["any"],
    packages=find_packages(),
    install_requires=['pyyaml','fspathtree>=0.3'],
    entry_points='''
      [console_scripts]
      dynaconfig=dynaconfig.scripts.cli:dynaconfig
    ''',
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
    python_requires='>=3.4',
    )
