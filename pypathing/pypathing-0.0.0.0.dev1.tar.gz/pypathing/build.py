from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from numpy import get_include


def compile():
    extensions = [Extension( "scr.cy_generators", 
                            ["scr/cy_generators.pyx"]),
                Extension( "scr.cy_searchers",
                            ["scr/cy_searchers.pyx"],
                            include_dirs=[get_include()])]

    setup(
        ext_modules=cythonize(extensions, annotate=False)
    )

    # python36 setup.py build_ext --inplace

compile()