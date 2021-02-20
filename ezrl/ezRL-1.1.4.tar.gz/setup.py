
from setuptools import setup

with open("./README.md", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name = "ezRL",
    version = "1.1.4",
    description = "easy Reinforcement Learning tool for python",
    author = "ezRL_team",
    author_email = "ezrl.adm@gmail.com",
    url = "https://github.co.jp/",
    packages = ["ezRL", "ezRL/parts/catcher_game", "ezRL/parts/DQN_Agent", "ezRL/parts/normal_cnn", "ezRL/parts/"],
    install_requires = ["relpath"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "CC0 v1.0",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    ],
    # entry_points = """
    #     [console_scripts]
    #     hoge = hoge:hoge
    # """
)
