from typing import List, Dict
from .elements import OaiElement, OreElement
from .utils.oai_search import get_oai_xml_response


class Publication:
    """This class represents a single publication
    """

    def __init__(self, bibtex_elements: List, site_elements: List, guid: str) \
            -> None:
        """constructor

        Parameters
        ----------
        bibtex_elements : List
            A list that contains all the metadata for bibtex creation
        site_elements : List
            A list that contains all the metadata that should be displayed on a site
        guid
            Guid of the publication for identification purposes.

        Raises
        ------
        ConnectionError
            If there are some connection issues during the process
        ValueError
            If no element is passed

        Note
        ----
        ** If an element should be either on the site and on bibtex,
        include that element in both lists. **
        The research of the elements is done inside the constructor, so the
        instantiation of the class may take a while
        """
        self._guid = guid
        self._meta = {}
        self._bibtex_elements = bibtex_elements
        self._site_elements = site_elements
        all_elements = bibtex_elements \
            + list(set(site_elements) - set(bibtex_elements))

        if not all_elements:
            raise ValueError("There are no elements to find")

        ore = False
        for element in all_elements:
            if issubclass(element, OreElement):
                ore = True
        try:
            self._meta = self._find_pub_meta(all_elements, ore)
        except ConnectionError as ce:
            print(ce)

    def is_empty(self) -> bool:
        """True if empty, False otherwise"""
        return False if self._meta else True

    @property
    def guid(self) -> str:
        """Returns guid (or handle) of the publication"""
        return self._guid

    # TODO correggere la gestione delle eccezioni
    def _find_pub_meta(self, elements_to_find: List, ore: bool = False) -> Dict:
        """Finds publication metadata

        Parameters
        ----------
        elements_to_find
            A list that contains all the metadata that should be found
        ore : optional
            If true looks also for additional metadata via OAI-PMH protocol
            using the ore format. For example pdf links of the publication

        Returns
        -------
        Dict
            All the metadata that has been founded.
            If a single metadata is not found, this will be omitted.

        Raises
        ------
        ConnectionError:
            If there is a connection issue during the process

        Note
        ----
        ** IF A METDATA IS NOT FOUND,
        IT WILL NOT BE INSERTED INSIDE THIS PUBLICATION. **
        """
        pub = {}
        try:
            oai_soup = get_oai_xml_response(self._guid)
        except ConnectionError:
            raise
        if ore:
            try:
                ore_soup = get_oai_xml_response(self._guid, prefix="ore")
            except ConnectionError:
                raise

        for element in elements_to_find:
            if issubclass(element, OaiElement):
                result = element(oai_soup)
            elif issubclass(element, OreElement):
                result = element(ore_soup)
            else:
                result = ""
            # only if it is not empty
            if result.value:
                pub[result.name] = result
        return pub

    def get_bibtex_representation(self) -> Dict[str, str]:
        """publication metadata with name and values of elements in bibtex format

        Returns
        -------
        Dict
            All metadata of the publication. The key is the name of the element
            (e.g. "author") and the value is the value of that element
            (e.g. "John Doe and Jane Doe and Another Doe").
        """
        res = {}
        if self._meta:
            for element in self._meta.values():
                if type(element) in self._bibtex_elements:
                    v = element.bibtex_value()
                    res.update(v)
        return res

    def get_site_meta(self) -> Dict[str, str]:
        """Publication metadata with names and values in yaml format for markdown

        Returns
        -------
        Dict
            All metadata of the publication. The key is the name of the element
            (e.g. "Title") and the value is the value of that element
            (e.g. "This is the title of the publication").

        Note
        ----
        The key of the of the returned dictionary ** does not containt ** the colon
        at the and of the string. When exported in markdown It should be added
        """
        res = {}
        if self._meta:
            for element in self._meta.values():
                if type(element) in self._site_elements:
                    v = element.markdown_value()
                    res.update(v)
        return res
