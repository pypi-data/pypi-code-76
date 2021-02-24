import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fenix_library-configuration",
    version="0.0.3",
    author="Shivanand Pattanshetti",
    author_email="shivanandvp@rebornos.org",
    description="A library for parsing and storing settings and configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rebornos-team/fenix/libraries/configuration",
    download_url="https://pypi.org/project/fenix-library-configuration/",
    project_urls={
        'Documentation': 'https://rebornos-team.gitlab.io/fenix/libraries/configuration/',
        'Source': 'https://gitlab.com/rebornos-team/fenix/libraries/configuration',
        'Tracker': 'https://gitlab.com/rebornos-team/fenix/libraries/configuration/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Typing :: Typed",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_namespace_packages(include=['fenix_library.*']),
    namespace_packages=[
        "fenix_library"
    ],
    python_requires='>=3.6'
)