import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "latticetools",
    version = "0.61",
    author = "Jack Maxwell",
    author_email = "latticetools@maxman.cc",
    description = "Makes it easy to manipulate and visualise data on an n-dimensional lattice",
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = "",
    packages = setuptools.find_packages(),
    install_requires = [
        'numpy >= 1.16',
        'matplotlib >= 3',
        'scikit-image >= 0.15',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    keywords = 'lattice grid scientific visualization imaging sampling fourier warp',
)
