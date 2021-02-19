import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    string = f.read()
    reequirements = list(filter(None, string.split("\n")))


setuptools.setup(
    name='gitlab-issue-delete',
    version='1.1.2',
    author='Sachin Chavan',
    author_email='sachinewx@gmail.com',
    description='Delete GitLab issue in bulk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Git GitLab issue',
    url="https://github.com/sachinchavan9/gitlab-operation",
    packages=setuptools.find_packages(),
    install_requires=reequirements,
    entry_points={
        'console_scripts': ['gitlab-issue-delete=gitlab_operations.deleteissue:main'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.5',
    include_package_data=True,
    zip_safe=False
)
