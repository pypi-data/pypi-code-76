# -*- coding: utf-8 -*-
from otterplot.process.parser.cparser import CParser
from otterplot.process.parser.iparser import IParser


def main(parser: IParser):
    config = parser.config
    print(parser.config.content)


if __name__ == "__main__":
    main(CParser.parseinput())
