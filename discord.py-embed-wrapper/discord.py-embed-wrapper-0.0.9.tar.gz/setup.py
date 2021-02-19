import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord.py-embed-wrapper",
    version="0.0.9",
    author="sleoh",
    author_email="simon.henkel@gmx.de",
    description="A small wrapper for easy creation of discord.py Embeds and sending/editing of Messages including those Embeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/sleoh/discord.py-embed-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)