import setuptools

def readme():
	with open("README.rst",encoding='utf-8') as f:
		README = f.read()
	return README

setuptools.setup(
    name="loanpy",
    version="0.1.8",
    author="Viktor Martinović",
    author_email="viktor.martinovic@hotmail.com",
    description="framework for detecting old loanwords",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    url="https://github.com/martino-vic/loanpy",
    license="""Academic Free License ("AFL") v. 3.0""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    keywords="historical linguistics, computational linguistics, lexicology, Uralistics, borrowing detection, contact linguistics, loanword adaptation",
    project_urls={
        "Source": "https://github.com/martino-vic/loanpy",
        "Citation": "https://doi.org/10.5281/zenodo.4127115",
    },
    packages=["loanpy"],
    package_dir={"loanpy": "loanpy"},
    package_data={"loanpy": ["loanpy/data/*.csv","loanpy/data/*.txt"]},
    include_package_data=True,
    install_requires=["pandas","lingpy","nltk","gensim","Levenshtein"],
    python_requires='>=3.6',
)
