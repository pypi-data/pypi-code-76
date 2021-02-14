# Parse markdown table into tuple of lists
# Armaan Bhojwani 2021

from bs4 import BeautifulSoup
import markdown

from .deck import Card


def md2html(file):
    """Use the markdown module to convert input to HTML"""
    outp = ""
    for i in file:
        try:
            outp += markdown.markdown(
                open(i, "r").read(), extensions=["tables"]
            )
        except FileNotFoundError:
            raise Exception(
                f'lightcards: "{i}": No such file or directory'
            ) from None

    return outp


def parse_html(html, args, conf):
    """Use BeautifulSoup to parse the HTML"""

    def clean_text(inp):
        return inp.get_text().rstrip()

    soup = BeautifulSoup(html, "html.parser")
    outp, ths = [], []

    if args.table:
        table_num = args.table
    elif conf["table"]:
        table_num = conf["table"]
    else:
        table_num = False

    for i, table in enumerate(soup.find_all("table"), start=1):
        ths = table.find_all("th")
        if len(ths) != 2:
            if conf["lenient"] or not args.lenient:
                raise Exception("lightcards: Headings malformed")
        elif (table_num and i == table_num) or not table_num:
            try:
                for x in table.find_all("tr"):
                    y = x.find_all("td")
                    if y:
                        outp.append(Card(tuple([clean_text(z) for z in y])))
            except AttributeError:
                raise Exception("lightcards: No table found") from None

    # Return a tuple of nested lists
    return ([clean_text(x) for x in ths], outp)
