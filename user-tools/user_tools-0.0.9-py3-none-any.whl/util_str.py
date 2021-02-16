#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Custom str function."""


def format_str(string: str) -> str:
    """Remove all kinds of blanks in the string,
       including full-width blanks and non-breaking blanks"""
    string = string.replace("\r\n", "")
    string = string.replace("\t", "")
    string = string.replace("\r", "")
    string = string.replace("\n", "")
    string = string.replace("\xa0", "")
    string = string.replace("\u3000", "")
    string = string.strip()
