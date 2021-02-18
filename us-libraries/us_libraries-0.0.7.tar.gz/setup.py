import setuptools


def get_version():
    with open('version') as version_file:
        return version_file.readline()


requirement_file = open('requirements.txt')
requirements = [l for l in requirement_file.readlines() if not l.startswith('-')]
requirement_file.close()

setuptools.setup(
    name="us_libraries",
    version=get_version(),
    author="Ukuspeed",
    author_email="info@ukuspeed.gmail.com",
    description="Libraries for us services",
    url="https://github.com/ukuspeed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
