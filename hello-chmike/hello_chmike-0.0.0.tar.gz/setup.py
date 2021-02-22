from setuptools import setup, Extension

setup(
  ext_modules=[Extension('hello.ext',
                       ['src/hello.c'],
                       depends=['src/hello.h'],
                       include_dirs=['src'],
              )],
)
