import setuptools

long_description = open("README.md").read()

setuptools.setup(
    name="pyhs3ng",
    version="1.0.5",
    author="Jason Rhubottom",
    author_email="jason@rhusoft.com",
    description="Python3 async library for interacting with HomeSeer HS3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrhubott/pyhs3",
    packages=["pyhs3ng"],
    install_requires=["asyncio", "aiohttp"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
