import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="salal",
    version="0.10.1-alpha",
    author="Todd Haskell",
    author_email="todd@craggypeak.com",
    description="A system for building websites from templates and content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haskelt/salal",
    license="GNU General Public License v3",
    packages=['salal'],
    package_data={'': ['system.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    python_requires='>=3.6',
    install_requires=[
        'Jinja2>=2.11.2',
        'lxml>=4.1.0'
    ]
)
