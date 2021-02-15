import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jibber-jabber",
    version="0.0.9", # change it to 0.1 when you are happy
    author="CE",
    author_email="celupo@pm.me",
    description="Simple product name generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cerodriguez/gibberish",
    packages=setuptools.find_packages(),
    package_data={'jibberjabber': ['dist.*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)