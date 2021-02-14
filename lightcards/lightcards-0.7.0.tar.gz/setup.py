from setuptools import setup
import os
import shutil

pwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(pwd, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def mkdir(dir):
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass


if os.geteuid() == 0:
    mkdir("/etc/lightcards/")
    shutil.copyfile("./config.py", "/etc/lightcards/config.py")
else:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    xdg_dest = f"{xdg}/lightcards/config.py"

    home = os.path.expanduser("~")
    home_dest = f"{home}/.config/lightcards/config.py"

    if xdg and not os.path.exists(xdg_dest):
        mkdir(f"{xdg}/lightcards")
        shutil.copyfile("./config.py", xdg_dest)
    elif not os.path.exists(home_dest):
        mkdir(f"{home}/.config/lightcards")
        shutil.copyfile("./config.py", home_dest)


setup(
    name="lightcards",
    version="0.7.0",
    description="Terminal flashcards from Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lightcards.armaanb.net",
    author="Armaan Bhojwani",
    author_email="me@armaanb.net",
    license="MIT",
    packages=["lightcards"],
    install_requires=["beautifulsoup4", "markdown"],
    data_files=[
        ("man/man1", ["man/lightcards.1"]),
        ("man/man5", ["man/lightcards-config.5"]),
    ],
    entry_points={
        "console_scripts": ["lightcards=lightcards:main"],
    },
    classifiers=[
        "Intended Audience :: Education",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
    ],
)
