import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clibato",
    version="0.0.9",
    author="Jigar Mehta",
    author_email="hello@jigarius.com",
    description="A command-line tool that can backup and restore your dot-files or other simple files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU LGPL v2.1',
    url="https://github.com/jigarius/clibato",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'GitPython>=3.1.13',
        'PyYAML>=5.4.1'
    ],
    entry_points={
        'console_scripts': ['clibato=clibato.__main__:main'],
    }
)
