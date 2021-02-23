"""
These are the Lyncs' default classifiers.
Ref. to https://pypi.org/classifiers/
"""


def get_classifiers(current=None):
    "Returns the classifiers for the package"
    # TODO

    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Physics",
    ]

    return current or classifiers
