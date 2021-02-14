import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numeraltoolkit-jaydenmw", # Replace with your own username
    version="0.0.3",
    author="JaydenMW",
    author_email="jmw.team.mail@gmail.com",
    description="A python SDK for scripts that use numbers.",
    url="https://codeberg.org/jaydenmw/numeraltool.sdk.jaydenmw",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
