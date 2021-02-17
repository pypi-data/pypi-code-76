"""Setup for the StuyUtils package."""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stuy_utils",
    version="0.0.1",
    author="Anthony Chen",
    author_email="anthonychen318@gmail.com",
    description="Useful functions & utilities for Stuyvesant High School.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/achen318/StuyUtils",
    packages=setuptools.find_packages(),
    package_data={"stuy_utils": ["data/*.csv"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    data_files=[
        ("bell_schedule", ["stuy_utils/data/bell_schedule.csv"]),
        ("term_days", ["stuy_utils/data/term_days.csv"])
    ]
)
