import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_da_final_vkaul",
    version="0.0.1",
    author="Vibhesh Kaul",
    author_email="v.kaul@student.uw.edu.pl",
    description="Package computes specific statistics of students in Poland",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.uw.edu.pl/v.kaul/pythonda_finalassignment.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['pandas'],
)