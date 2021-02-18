from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Wrapper for scraping simplemachineforums'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="smfscraper", 
        version=VERSION,
        author="Utsav Magar",
        author_email="utsavmagar88728@gmail.com",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        url='https://github.com/ryuuzu/smfscaper',
        install_requires=['requests', 'beautifulsoup4'],
        python_requires='>=3.6',
        
        keywords=['python', 'first package', 'smf', 'simplemachineforums', 'smfscraper', 'smfapi'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)