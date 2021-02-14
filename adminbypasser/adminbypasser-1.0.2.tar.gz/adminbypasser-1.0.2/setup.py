from setuptools import setup, find_packages


setup(
    name="adminbypasser",
    version="1.0.2",
    description="Adminpanel bypasser",
    py_module=["adminbypasser"],
    scripts=['src/adminbypasser'],
    license="MIT",
    keywords="adminpanel,bypasser,bypass",
    packages=find_packages(),
    install_requires=[
        "bs4>=0.0.1",
        "requests>=2.24.0"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "check-manifest>=0.43",
            "twine>=3.2.0"
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
    ],

    url="https://github.com/0xbin/adminbypasser",
    author="xbin",
    author_email="xbin2021@gmail.com"
)


# pip install -e .
# python setup.py sdist
# twine.exe upload --repository-url=https://upload.pypi.org/legacy/ dist/*
