import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="praktikum",
    version="2.3.3",
    author="Henning Gast",
    author_email="henning@physik.rwth-aachen.de",
    description="Tools for the beginners' lab courses in physics at RWTH Aachen University",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="http://pgp.physik.rwth-aachen.de/software",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['cassy_info = praktikum.cassy_tools:cassy_info',
                            'cassy_plot = praktikum.cassy_tools:cassy_plot'] },
    install_requires=['numpy', 'scipy', 'matplotlib', 'future'],
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Natural Language :: German",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education"
    ),
)
