import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name = 'word2num_de',
    packages = ['word2num_de'],
    version = '1.1',
    license='MIT',
    description = 'Transforms written numbers in German to numbers.',
    long_description=README,
    long_description_content_type="text/markdown",
    author = 'Kaoru Schwarzenegger',
    url = 'https://github.com/kaorusss/word2num-de',
    download_url = 'https://github.com/kaorusss/word2num-de/archive/v1.1.tar.gz',
    keywords = ['numbers', 'convert', 'words', 'german'],
    classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python'
    ],
)