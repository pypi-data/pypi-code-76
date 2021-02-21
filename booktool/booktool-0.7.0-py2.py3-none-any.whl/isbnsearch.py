from typing import Iterator, Dict, List
from xml.etree import ElementTree

import html5lib
import requests

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
)


def get_isbnsearch(isbn: str) -> requests.Response:
    url = f"https://isbnsearch.org/isbn/{isbn}"
    # 403's if User-Agent is not set :(
    return requests.get(url, headers={"User-Agent": USER_AGENT})


def extract_isbnsearch_results(doc: ElementTree.Element) -> Iterator[Dict[str, str]]:
    for prices_div in doc.findall('.//div[@class="prices"]'):
        heading = prices_div.findtext("h2")
        conditions = {"New", "Used", "Rental"}
        condition = next(
            (condition for condition in conditions if condition in heading), "Unknown"
        )
        listitems = prices_div.findall("ul/li")
        for listitem in listitems:
            merchant = listitem.find('.//div[@class="merchant"]/a/img').get("alt")
            price = listitem.findtext(
                './/div[@class="info"]/div[@class="price"]/p[@class="pricelink"]/a'
            )
            yield {"condition": condition, "merchant": merchant, "price": price}


def get_isbnsearch_results(isbn: str) -> List[dict]:
    response = get_isbnsearch(isbn)
    doc = html5lib.parse(response.text, namespaceHTMLElements=False)
    return list(extract_isbnsearch_results(doc))
