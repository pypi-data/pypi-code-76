
import setuptools
from Cython.Build import cythonize
import os


ext_modules = cythonize("how_many_fish/fish_multiplier.pyx",
	compiler_directives={'language_level' : "3"})

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="how_many_fish", # Replace with your own username
    version="0.0.2",
    author="Oscar",
    author_email="oscargwilkins@gmail.com",
    description="Tells you you got 20 fish",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Delayed-Gitification/how_many_fish.git",
    packages=setuptools.find_packages(),
    ext_modules = ext_modules,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "how_many_fish = how_many_fish.__main__:main",
        ]},
    python_requires='>=3.6',
)