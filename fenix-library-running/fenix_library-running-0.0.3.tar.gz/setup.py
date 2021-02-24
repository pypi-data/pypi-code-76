import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fenix_library-running",
    version="0.0.3",
    author="Shivanand Pattanshetti",
    author_email="shivanandvp@rebornos.org",
    description="A library to run and live-log OS commands, functions, scripts, and batch jobs either immedietly, or queued for later execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rebornos-team/fenix/libraries/running",
    download_url="https://pypi.org/project/fenix-library-running/",
    project_urls={
        'Documentation': 'https://rebornos-team.gitlab.io/fenix/libraries/running/',
        'Source': 'https://gitlab.com/rebornos-team/fenix/libraries/running',
        'Tracker': 'https://gitlab.com/rebornos-team/fenix/libraries/running/issues',
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