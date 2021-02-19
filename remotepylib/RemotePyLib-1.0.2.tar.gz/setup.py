import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="RemotePyLib",
    version="1.0.2",
    author="Nalin Angrish",
    author_email="nalin@nalinangrish.me",
    description="A package to import libraries remotely.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.nalinangrish.me/apps/remotepylib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'importlib',
        'bs4'
    ],
    python_requires='>=3.0',
)