import setuptools
import os.path as op


setuptools.setup(
    name="file-tree",
    version="0.2.1",
    url="https://git.fmrib.ox.ac.uk/ndcn0236/file-tree",

    author="Michiel Cottaar",
    author_email="MichielCottaar@protonmail.com",

    description="Describe structure directory for pipeline",
    long_description=open('README.md').read(),

    package_dir={'': "src"},

    packages=setuptools.find_packages("src", exclude=('tests*', )),

    zip_safe=False,

    install_requires=[
        "numpy", "xarray", "pandas", "parse",
    ],

    project_urls = {
        "Documentation": "https://open.win.ox.ac.uk/pages/ndcn0236/file-tree/",
    },

    include_package_data=True,

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
