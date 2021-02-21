from typing import List
from xml.etree import ElementTree

import requests

CLASSIFY_URL = "http://classify.oclc.org/classify2/Classify"
CLASSIFY_NAMESPACE = "http://classify.oclc.org"
CLASSIFY_ERRORS = {
    "100": "No input. The method requires an input argument.",
    "101": "Invalid input. The standard number argument is invalid.",
    "102": "Not found. No data found for the input argument.",
    "200": "Unexpected error.",
}


class ClassifyError(Exception):
    def __init__(self, response_code: str, response: requests.Response = None):
        error = CLASSIFY_ERRORS[response_code]
        super().__init__(f"[code={response_code}] {error}")
        self.response = response


def classify(**params) -> List[str]:
    """
    `params` should be some combination of:

    stdnbr  | standard number (OCLC/ISBN/ISSN/UPC)
    oclc    | OCLC number
    isbn    | ISBN
    issn    | ISSN
    upc     | UPC
    ident   | FAST identifier
    heading | FAST heading
    owi     | OCLC work identifier
    author  | author name
    title   | title
    summary | produce a summary-only response (true/false)
    maxRecs | number of records to return (an integer)
    orderBy | desired ordering; one of the following (followed by " asc" or " desc"):
      "mancount" | number of editions
      "hold"     | holdings
      "lyr"      | date of first edition
      "hyr"      | date of latest edition
      "ln"       | language
      "sheading" | FAST subject heading
      "works"    | number of works with this FAST subject heading
      "type"     | FAST subject type

    Returns list of OCLC work identifiers.

    Throws a ClassifyError if API response code indicates an error.

    Reference: http://classify.oclc.org/classify2/api_docs/classify.html
    """
    response = requests.get(CLASSIFY_URL, params=params)
    root = ElementTree.XML(response.content)

    response_code = root.find("response", {"": CLASSIFY_NAMESPACE}).attrib["code"]
    if response_code in CLASSIFY_ERRORS:
        raise ClassifyError(response_code, response)

    if response_code in {"0", "2"}:
        # single-work response
        work_element = root.find("work", {"": CLASSIFY_NAMESPACE})
        return [work_element.text]
    # response_code == "4" (multi-work response) is the only other success condition
    work_elements = root.findall("works/work", {"": CLASSIFY_NAMESPACE})
    return [work_element.attrib["wi"] for work_element in work_elements]


def catalog_content(
    oclcnumber: str,
    wskey: str,
    dublin_core: bool = False,
    full_service: bool = False,
) -> requests.Response:
    """
    Retrieve a single bibliographic record in MARC XML or Dublin Core format.

    `dublin_core` determines value of "recordSchema" param:
      False => info:srw/schema/1/marcxml
      True  => info:srw/schema/1/dc
    """
    url = f"https://www.worldcat.org/webservices/catalog/content/{oclcnumber}"
    schema = "dc" if dublin_core else "marcxml"
    params = {
        "wskey": wskey,
        "recordSchema": f"info:srw/schema/1/{schema}",
        "servicelevel": "full" if full_service else "default",
    }
    return requests.get(url, params=params)
