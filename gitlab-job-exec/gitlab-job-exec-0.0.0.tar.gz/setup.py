import setuptools


def get_version():
    return "0.0.0"


def get_requirements():
    requirements = []
    return requirements


with open("README.md", "r") as fh:
    long_description = fh.read()    # pylint: disable=invalid-name

setuptools.setup(
    name="gitlab-job-exec",
    version=get_version(),
    author="Uncrns",
    author_email="uncrns.devs@gmail.com",
    description="Execute GitLab-CI docker jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/uncrns/gitlab-job-exec",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        ],
    python_requires=">=3.6",
    install_requires=get_requirements(),
    entry_points={'console_scripts': ['gitlab-job-exec = gitlab_job_exec.cli:main']},
    )
