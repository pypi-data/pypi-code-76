import setuptools
from numpy.distutils.core import setup
from numpy.distutils.core import Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

ext = [Extension(name = 'compflow_fort_from_Ma', sources = ['fortran/from_Ma.f']),
       Extension(name = 'compflow_fort_der_from_Ma', sources = ['fortran/der_from_Ma.f']),
       Extension(name = 'compflow_fort_to_Ma', sources = ['fortran/to_Ma.f'])]

setup(
    name="compflow",
    version="0.3.0",
    author="James Brind",
    author_email="jb753@cam.ac.uk",
    description="Compressible aerodynamics library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jb753.user.srcf.net/compflow-docs/index.html",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "scipy"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    ext_modules=ext,
    keywords=['compressible','flow','aerodynamics','fluid','engineering']

)
