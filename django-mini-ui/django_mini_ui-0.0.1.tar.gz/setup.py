import setuptools

with open("README.md", "r", encoding="utf-8") as _:
    long_description = _.read()

setuptools.setup(
    name = "django_mini_ui", 
    version = "0.0.1",
    author = "Malagundla Ranjith Kumar",
    author_email = "ranjithsvcetcseb@gmail.com",
    description = "A small UI editor for django apps.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ranjithsvcetcse/django-mini",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Framework :: Django :: 3.0",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    install_requires = [
        "django>=3",
    ],
    python_requires = '>=3.6',
)