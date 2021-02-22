import setuptools
from distutils.util import convert_path


about = {}

ver_path = convert_path('xyztest/__version__.py')
with open(ver_path) as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xyztest", # Replace with your own username
    version=about["__version__"],
    author="Amin Sadeghi",
    author_email="amin@sadeghi.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ma-sadeghi/xyztest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
