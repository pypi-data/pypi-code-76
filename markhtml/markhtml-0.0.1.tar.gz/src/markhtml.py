#!/usr/bin/env python
import argparse
import markdown
import os
from string import Template
from pathlib import Path

# Set up paths
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
TEMPLATE_FILE = os.path.join(SRC_DIR, 'template.html')

def initialize_parser():
    md = markdown.Markdown(extensions=["toc"])
    return md


def read_filename():
    parser = argparse.ArgumentParser(description="Convert a MD file into HTML.")
    parser.add_argument("filename", nargs="+", help="The markdown filename")

    args = parser.parse_args()
    filename = args.filename[0]
    return filename


def open_file(filename):
    with open(filename, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        return text


def render(html, toc):
    context = {"content": html, "toc": toc}
    with open(TEMPLATE_FILE, "r") as f:
        src = Template(f.read())
        result = src.substitute(context)
        return result


def save(text, filename):
    out_filename = Path(filename).with_suffix('.html')
    with open(
        out_filename, "w", encoding="utf-8", errors="xmlcharrefreplace"
    ) as output_file:
        output_file.write(text)
        print("Generated file: {}".format(out_filename))


def main():
    filename = read_filename()
    md = initialize_parser()
    text = open_file(filename)
    html = md.convert(text)
    toc = md.toc
    page = render(html, toc)
    save(page, filename)


if __name__ == "__main__":
    main()
