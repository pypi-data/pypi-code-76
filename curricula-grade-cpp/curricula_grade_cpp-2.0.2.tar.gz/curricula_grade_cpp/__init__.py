from pathlib import Path

root = Path(__file__).absolute().parent


class Paths:
    INCLUDE = root.joinpath("include")
    GTEST = root.joinpath("gtest", "gtest.cpp")
