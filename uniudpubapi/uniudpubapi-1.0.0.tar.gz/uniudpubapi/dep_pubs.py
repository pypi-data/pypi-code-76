from .utils.decorators import timer
from .publications import Publication
from collections.abc import Iterable, Iterator
from typing import Dict, List
from .elements import factory, Element
from bs4 import BeautifulSoup
import requests
import re
import sys


class DepartmentPublications(Iterable):
    """This class provides functionality for finding publications that belong to
    UniUD institutional repository: https://air.uniud.it/.
    """

    def __init__(self, department: Dict[str, str],
                 bibtex_elements: List[str],
                 site_elements: List[str]) -> None:
        """
        Parameters
        ----------
        department
            A Dictionary with the name and surname of the researcher as a key,
            and an author id as value.
            e.g.
            department = {
                    "John Doe": "rp12345",
                    "Jane Doe": "rp54321",
            }
        elements_to_find
            a list containing all metadata to be found.
            ** WRITE THEM IN THE SAME ORDER YOU WANT THE RESPONSE TO **
            Mandatory elements: "title", "handle", "type"
            e.g.
            elements_to_find = ["title", "handle"]

        Raises
        ------
        ValueError
            If an invalid element is inside elements_to_find
            (read the note to see what are the accepted values).
        IndexError
            If there are no elements inside elements_to_find.

        Notes
        -----
        Check all available elements in "elements.py" before selecting
        elements_to_find elements.
        Available elements are at the and of the file ("elements.py")
        passed as first argument of the factory method
        "register_type_of_element".
        """

        self._department: Dict[str, str] = self._check_valid_dep(department)
        if not bibtex_elements and not site_elements:
            raise IndexError("There are no elements to find")

        self._bibtex_elements: List[Element] = []
        self._site_elements: List[Element] = []
        for el in bibtex_elements:
            self._bibtex_elements.append(factory.get_element(el))
        for el in site_elements:
            self._site_elements.append(factory.get_element(el))

        self._all_publications: List = []

    def _check_valid_dep(self, department: Dict[str, str]) -> Dict[str, str]:
        """Checks if the department dictionary has valid entries.

        Raises
        ------
        ValueError
            if entries don't use the correct form.
        """
        if department:
            for x, y in department.items():
                if re.search("[a-z]{2}[0-9]{5}", y) \
                        and re.search("^[a-zA-ZA-Za-zÀ-ÖØ-öø-ÿ ,.'-]+$", x):
                    continue
                else:
                    raise ValueError("Department entries are not correct")
        else:
            raise ValueError("Empty department")
        return department

    def _get_opensearch_xml_response(self, identifier: str) -> bytes:
        """Fetches xml pubs from opensearch repository.

        Retrives all the publications of the researcher corresponding
        to the identifier.

        Parameters
        ----------
        identifier
            researcher identifier (e.g. rp23339 -> this is an example of
            the expected format, don't try to use this code).

        Returns
        -------
        str
            the entire xml file response.

        Raises
        ------
        ConnectionError
            An error occurred during the connection.
        """

        url = "https://air.uniud.it/open-search/?query=author_authority:" + \
            identifier + \
            "&scope=11390/1063634&format=rss&sort_by=2&order=DESC&rpp=10000"
        try:
            var_url = requests.get(url)
        except ConnectionError as ce:
            raise ce
        else:
            return var_url.content

    def _is_duplicate(self, guid: str) -> bool:
        """Checks if the publication identified by "guid" has already been inserted.

        Raises
        ------
        ValueError
            If guid is empty or not a string.
        """

        if not guid or not isinstance(guid, str):
            raise ValueError("guid value is not correct")
        for pub in self._all_publications:
            if pub.guid == guid:
                return True
        return False

    @timer
    def find_department_publications(self) -> None:
        """Finds all publications of the department and stores them inside the object.

        Raises
        ------
        IndexError
            if there are no elements inside elements_to_find.

        Note
        ----
        ** IF A PUBLICATION HAS NO METADATA, IT WILL NOT BE CONSIDERED **
        """
        for x, y in self._department.items():
            root = BeautifulSoup(self._get_opensearch_xml_response(y), "lxml")
            i = 1
            n_pubs = len(root.findAll("item"))
            sys.stdout.write("\n")
            for item in root.findAll("item"):
                sys.stdout.flush()
                sys.stdout.write("\r" + "Finding " + x + "'s publications...{0} of "
                                 "{1}".format(i, n_pubs))

                handle = self._find_handle(item)
                if not self._is_duplicate(handle):
                    p = Publication(self._bibtex_elements,
                                    self._site_elements, handle)
                    if not p.is_empty():
                        self._all_publications.append(p)
                i += 1

    def _find_handle(self, soup: BeautifulSoup) -> str:
        """handle finder

        Parameters
        ----------
        soup : BeautifulSoup
            parser containing a single item of the xml document found with opensearch

        Returns
        -------
        str
            The handle of the publication

        Raises
        ------
        ValueError
            If the parser does note contain a single item

        Example
        -------
        With open-search, each publication has its own metadata inside an <item> tag
        This <item> tag should be the root of the BeautifulSoup element passed as
        parameter
        """
        if not soup.find("guid"):
            raise ValueError("It's not a single opensearch pub item")
        else:
            result = soup.find("guid").text \
                .replace("\n", " ").replace("\r", "")
        return result

    def __iter__(self):
        return DepartmentIterator(self._all_publications)


class DepartmentIterator(Iterator):
    """Iterator for DepartmentPublications object
    """

    def __init__(self, dep_pub: List[Publication]) -> None:
        self._dep_pub = dep_pub
        self._index = 0

    def __next__(self) -> Publication:
        """next item of the iterator

        Returns
        -------
        Publication
            a publication of the department

        Raises
        ------
        StopIteration
            when there are no more elements
        """
        try:
            ret_val = self._dep_pub[self._index]
            self._index += 1
        except IndexError:
            raise StopIteration
        return ret_val
