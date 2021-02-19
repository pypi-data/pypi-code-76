"ckgen setup module."

def main():

    from setuptools import setup, find_packages
    from ckgen.main import CESMKGen as kgen

    console_scripts = ["ckgen=ckgen.__main__:main"]
    install_requires = ["fortlab>=0.1.7"]

    setup(
        name=kgen._name_,
        version=kgen._version_,
        description=kgen._description_,
        long_description=kgen._long_description_,
        author=kgen._author_,
        author_email=kgen._author_email_,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        keywords="microapp fortlab ckgen",
        packages=find_packages(exclude=["tests"]),
        include_package_data=True,
        install_requires=install_requires,
        entry_points={ "console_scripts": console_scripts,
            "microapp.projects": "ckgen = ckgen"},
        project_urls={
            "Bug Reports": "https://github.com/grnydawn/ckgen/issues",
            "Source": "https://github.com/grnydawn/ckgen",
        }
    )

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
