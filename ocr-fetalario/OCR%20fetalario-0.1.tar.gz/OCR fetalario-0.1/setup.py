
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="OCR fetalario",
    version="0.1",
    description="ws to process ocr",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords="OCR",
    author="iq",
    author_email="ivanqcotera@gmail.com",
    maintainer="iq",
    maintainer_email="ivanqcotera@gmail.com",
    url="https://github.com/iqvan/OCR_library",
    download_url='https://github.com/iqvan/OCR_library/archive/v1.0.0.tar.gz',
    license="MIT",
    install_requires=["aniso8601", "appdirs", "certifi", "cffi", "chardet",
                      "click", "coloredlogs", "cryptography", "distlib", "filelock",
                      "Flask", "Flask-RESTful", "humanfriendly", "idna", "img2pdf",
                      "importlib-metadata", "importlib-resources", "itsdangerous", "Jinja2", "lxml",
                      "MarkupSafe", "numpy", "ocrmypdf", "opencv-python", "pdftotext",
                      "pikepdf", "Pillow", "pipenv", "pycparser", "pycryptodome",
                      "pytesseract", "python-dotenv", "pytz", "pyzbar", "reportlab",
                      "requests", "six", "sortedcontainers", "tesseract", "tqdm",
                      "urllib3", "virtualenv", "virtualenv-clone", "Werkzeug", "zipp"],
)
