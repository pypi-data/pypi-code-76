from setuptools import setup
with open("README.md", "r")as fh :
    long_description = fh.read()
setup(
    name='anifolds',
    version='0.0.1',
    url="https://github.com/RobiMez/Anicons_py",
    author="robimez",
    description='Anime icon creation tool!',
    py_modules=['anicons'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "jikanpy" ,
        "pyfiglet" ,
        "PyInquirer" ,
        "PIL",
    ]
)