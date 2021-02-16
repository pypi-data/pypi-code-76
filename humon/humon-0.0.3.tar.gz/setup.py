# We're linking against '../build/bin/libhumon-d.a' which is built by `../build.py`.

from setuptools import setup, Extension

with open ('README.md', 'r') as f:
      long_desc = f.read()

setup(name="humon",
      version='0.0.3',
      description='A Python wrapper over humon\'s C API, for reading Humon token streams.',
      long_description = long_desc,
      long_description_content_type = 'text/markdown',
      author='Trevor Schrock',
      author_email='spacemeat@gmail.com',
      url='https://github.com/spacemeat/humon-py',

      packages=["humon"],
      ext_package="humon",
      ext_modules=[Extension("humon",
                             include_dirs = ['./clib/include/humon', './clib/src'],
                             extra_compile_args = ['-ggdb3', '-O0'],
                             sources = ["./clib/src/ansiColors.c",
                                        "./clib/src/encoding.c",
                                        "./clib/src/node.c",
                                        "./clib/src/parse.c",
                                        "./clib/src/printing.c",
                                        "./clib/src/tokenize.c",
                                        "./clib/src/trove.c",
                                        "./clib/src/utils.c",
                                        "./clib/src/vector.c",
                                        "./humon/cpkg/enumConsts.c",
                                        "./humon/cpkg/humonModule.c", 
                                        "./humon/cpkg/node-py.c",
                                        "./humon/cpkg/token-py.c",
                                        "./humon/cpkg/trove-py.c",
                                        "./humon/cpkg/utils.c"])
                   ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Topic :: Software Development"
      ],
      extras_require = {
            'dev': ['check-manifest', 'twine']
      },
      python_requires='>=3.8'
)


