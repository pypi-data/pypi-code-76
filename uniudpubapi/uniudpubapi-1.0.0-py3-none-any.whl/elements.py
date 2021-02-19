from abc import ABC, abstractmethod
import html
from bs4 import BeautifulSoup
from typing import List, Dict
import requests

# TODO verificare, una volta esportato in markdown, se è necessario usare
# la funzione html.unescape, in quanto potrebbe avere senso mantenere
# i caratteri speciali di html
# TODO item not found exception
# TODO ALLA FINE risistemo bene le classi dal punto di vista dell'eredità


class Element(ABC):
    """This class represents a single metadata element.
    e.g.
        "title" of a publication is an element.
        "authors" of a publication is an element
        ....

    Attributes
    ----------
    _tag_name
        The tag used inside the xml to describe this element
    _name
        For renaming purposes, if you want to refer to this element
        with a different name than this tag name
    """

    def __init__(self):
        self._tag_name = ""
        self._name = ""
        self._value = ""

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def string_value(self):
        return self._value

    @abstractmethod
    def markdown_value(self) -> Dict:
        """returns element in yaml format

        Returns
        -------
        Dict
            contains values of the element, formatted in markdown yaml.
            Key is the name of the element
            Value is the value of the element
        """
        pass

    @abstractmethod
    def bibtex_value(self) -> Dict:
        """returns element in bibtex format

        Returns
        -------
        Dict
            name and values for the single element, provided in bibtex-friendly
            format.
            Key is the name of the element
            Value is the value of the element
            Curly braces not included inside element value.
        """
        pass

    @abstractmethod
    def _get_element_value(self, soup: BeautifulSoup):
        """finds the value of the element.

        Parameters
        ----------
        soup : BeautifulSoup
            root of the publication obtained via OAI-PMH protocol
        """
        pass


class OaiElement(Element):
    """This class represents an element inside an xml document retrieved using
    OAI-PMH protocol. It is recommended to inherit from this class if the
    element is unique inside the xml document and it is defined by its tag
    (For example the title of the publication appear only one time inside
    the xml document, so the title element should inherit from this class).
    """

    def bibtex_value(self) -> Dict:
        """** See Element class  (parent) **
        """
        return {self._name: self.string_value()}

    def string_value(self) -> str:
        """** See Element class  (parent) **
        """
        return self._list_to_str(self._value, "")

    def _list_to_str(self, somelist: List, sep: str) -> str:
        """Converts a given list to string.

        Parameters
        ----------
        somelist : List
            list to be converted
        sep : str
            a separator placed between each element

        Returns
        -------
        str
            string containing elements from the list separated by the "sep" string
        """
        res = ""
        for i in range(len(somelist)):
            if i != len(somelist) - 1 and sep:
                res = res + str(somelist[i]) + " " + sep + " "
            else:
                res = res + str(somelist[i])
        return res

    def markdown_value(self) -> Dict:
        """** See Element class  (parent) **
        """
        return {self.name: "\"" + self.string_value() + "\""}

    def _find_value(self, soup: BeautifulSoup, start_str: str = "",
                    sep: str = "") -> List[str]:
        """Retrieves the metadata text of a specific xml tag of the publication

        Parameters
        ----------
        soup
            the soup of the entire xml document

        start_str
            first part of the value.
            If the first part of the value is note.

        sep
            separator that divides the start_str from the part of the actual value


        Returns
        -------
        List[str]
            contains the value (or values) of the element (xml tag).
            If there is more than one element with that tag, all values with that
            tag are inserted in the list
        """
        if not sep and not start_str:
            res = []
            for node in soup.findAll("dc:" + self._tag_name):
                res.append(html.unescape(node.get_text()))
        else:
            res = []
            # For values that are not identified with an xml tag
            for node in soup.findAll("dc:" + self._tag_name):
                if node.text.startswith(start_str):
                    if sep:
                        res.append(html.unescape(node.text.split(sep)[1]))
                    else:
                        res.append(html.unescape(node.text))
        return res


class OreElement(Element):
    """This class represents an element inside an xml document retrieved using
    OAI-PMH protocol, ** using the ORE metadata format **.
    It is recommended to inherit from this class if the element is the value of
    an attribute of the tag.
    """

    def bibtex_value(self) -> Dict:
        """** See Element class  (parent) **
        """
        return {self._name: self.value}

    def _list_to_str(self, somedict: List, sep: str = "and") -> str:
        res = ""
        for i in range(len(somedict)):
            if i != len(somedict) - 1:
                res = res + str(somedict[i]) + " " + sep + " "
            else:
                res = res + str(somedict[i])
        return res


# ########################### END OF ABSTRACT ELEMENTS ############################


class Title(OaiElement):
    """This class ** inherit the behavior from the superclass **.
    It only defines the "_tag_name" and the "_name" for the "handle" element

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "title"
        self._name = "title"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup):
        res = super()._find_value(soup)
        return res[0] if res else res

    def bibtex_value(self) -> Dict:
        return {self._name: self.value}


# OAI version for finding oai element
class Handle(OaiElement):

    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "identifier"
        self._name = "handle"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = super()._find_value(soup, "http://hdl.handle.net", "")
        return res[0] if res else ""

    def bibtex_value(self):
        handle_splitted = self.value.split("/")
        value = handle_splitted[-2] + "/" + handle_splitted[-1]
        return {self._name: value}


# TODO gestire il modo in cui verranno presi tutti i set
class PubType(OaiElement):
    """Element which describes the publication type

    Attributes
    ----------
    _tag_name
        ** See Element class  (grandparent) **
    _name
        ** See Element class  (grandparent) **
    _sets
        Contains set codes and correspondent set name
        e.g.
        {
            ....
            "com_11390_1063635": "1 Contributo su Rivista"
            ....
        }

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "setspec"
        self._name = "type"
        # Sets for bibtex formatting
        self._sets = {
            "com_11390_1063635": "article",
            "com_11390_1063636": "inbook",
            "com_11390_1063637": "book",
            "com_11390_1063638": "inproceedings",
            "com_11390_1063639": "misc",
            "com_11390_1063640": "misc",
            "com_11390_1063641": "misc",
            "com_11390_1123313": "phdthesis"
        }
        # Sets for markdown formatting
        self._md_sets = {
            # See https://wowchemy.com/docs/managing-content/#manually for details
            "com_11390_1063635": "2",
            "com_11390_1063636": "6",
            "com_11390_1063637": "5",
            "com_11390_1063638": "1",
            "com_11390_1063639": "8",
            "com_11390_1063640": "0",
            "com_11390_1063641": "0",
            "com_11390_1123313": "7"
        }
        self._code = self._get_element_value(soup)
        self._value = self._sets[self._code]

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = ""
        for node in soup.findAll(self._tag_name):
            if node.text in self._sets:
                res = node.text
        return res

    def pub_type_code(self):
        return self._code

    def markdown_value(self):
        return {"publication_types": "[\"" + self._md_sets[self._code] + "\"]"}


class Authors(OaiElement):
    """This class ** inherit the behavior from the superclass **.
    It only defines the "_tag_name" and the "_name" for the "authors" element

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "creator"
        self._name = "author"
        self._value = self._get_element_value(soup)

    def string_value(self):
        return self._list_to_str(self._value, "and")

    def _get_element_value(self, soup: BeautifulSoup):
        values = super()._find_value(soup)
        # pointed_name = False
        # full_name = False
        for i in range(len(values)):
            values[i] = values[i].title()
            values[i] = values[i].replace(",", "")
            buff = values[i].split()
            for j in range(len(buff)):
                if len(buff[j]) == 1 and buff[j].isalpha():
                    buff[j] += "."
                elif j != len(buff) - 1:
                    buff[j] += " "
            values[i] = "".join(buff)
        # for el in values:
            # If there is no period in the string
        #    if not el.find(".") + 1:
        #        full_name = True
        #    else:
        #        pointed_name = True
        # if full_name and pointed_name:
        #     self._normalize_values(values)
        return values

    # For full names and pointed names in the same pub
    def _normalize_values(self, values: List[str]) -> None:
        for i in range(len(values)):
            buff = values[i].split()
            new_value = ""
            if not values[i].find(".") + 1:
                for j in range(len(buff)):
                    if j and not buff[j].find(".") + 1:
                        buff[j] = " " + buff[j][0] + "."
                    new_value += buff[j]
                values[i] = new_value

    def markdown_value(self) -> Dict:
        res = "\n"
        for author in self._value:
            res += "- " + author.replace(".", "") + "\n"
        return {"authors": res}


class Year(OaiElement):
    """This class ** inherit the behavior from the superclass **.
    It only defines the "_tag_name" and the "_name" for the "date" element

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "date"
        self._name = "year"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = super()._find_value(soup)
        return res[0] if res else ""

    def markdown_value(self):
        return {"date": "\"" + self.string_value() + "-01" + "-01" + "\""}


class Abstract(OaiElement):
    """This class ** inherit the behavior from the superclass **.
    It only defines the "_tag_name" and the "_name" for the "abstract" element

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "description"
        self._name = "abstract"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = super()._find_value(soup)
        return res[0] if res else ""

    def markdown_value(self):
        splitted = self.string_value().split("\n")
        res = ""
        for item in splitted:
            res += "  " + item + "\n"
        return {"abstract": ">-\n" + res + "\n"}


# TODO DOI implementation
class Doi(OaiElement):
    """This class ** inherit the behavior from the superclass **.
    It only defines the "_tag_name" and the "_name" for the "Doi" element

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """

    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "identifier"
        self._name = "doi"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        """sets only the right parameters for the superclass method
        """
        res = super()._find_value(soup, "10.", sep="")
        return res[0] if res else ""


class Pages(OaiElement):

    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "relation"
        self._name = "pages"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        buff = super()._find_value(soup, "firstpage", ":")
        first_page = ""
        last_page = ""
        if buff:
            first_page = buff[0]
        buff = super()._find_value(soup, "lastpage", ":")
        if buff:
            last_page = buff[0]
        res = ""
        if first_page and last_page:
            res = first_page + "--" + last_page
        return res


# TODO volume = {CS2002/3} da riconoscere
class Volume(OaiElement):
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "relation"
        self._name = "volume"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        temp = super()._find_value(soup, "volume", ":")
        if temp:
            res = temp[0]
            if not res.replace(" ", "").isalpha():
                return res
        return ""

    def has_lncs(self) -> bool:
        temp = self._value
        temp_list = temp.split("lncs")
        if len(temp_list) > 1:
            return True
        return False

    def bibtex_value(self) -> Dict:
        res = self._value
        buff = self._value.casefold()
        if not buff.isdigit():
            buff_list = buff.split("lncs")
            temp_res = ""
            for item in buff_list:
                temp_res += item
            res = temp_res.replace(" ", "")
        return {self.name: res}


class Journal(OaiElement):

    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "relation"
        self._name = "journal"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        p = PubType(soup)
        p_type = p.pub_type_code()
        if p_type == "com_11390_1063635":
            res = super()._find_value(soup, "journal", ":")
            return res[0] if res else ""
        return ""


class BookTitle(OaiElement):
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "relation"
        self._name = "booktitle"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = super()._find_value(soup, "ispartofbook", ":")
        return res[0] if res else ""


class Publisher(OaiElement):
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "publisher"
        self._name = "publisher"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        result = ""
        for child in soup.findAll("dc:" + self._tag_name):
            if child.text.startswith("country:") or \
                    child.text.startswith("place:"):
                continue
            else:
                result = html.unescape(child.text)
        return result


class Series(OaiElement):
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "serie"
        self._name = "series"
        self._value = self._get_element_value(soup)

    def _get_element_value(self, soup: BeautifulSoup) -> str:
        res = ""
        temp = super()._find_value(soup, "serie", ":")
        if temp:
            res = temp[0]
        else:
            vol = Volume(soup).has_lncs()
            if vol:
                res = "lncs"
        return res


class Pdf(OreElement):
    """Which describes pdf links to the publication.

    Attributes
    ----------
    ** See Element class  (grandparent) **

    """
    def __init__(self, soup: BeautifulSoup):
        self._tag_name = "link"
        self._name = "pdf"
        self._value = self._get_element_value(soup)

    @property
    def value(self):
        return self._value

    def string_value(self):
        return self._list_to_str(self._value)

    def markdown_value(self) -> Dict[str, str]:
        res = "\n"
        length = len(self._value)
        for i in range(length):
            if length == 1:
                line = " " + "- name: PDF" + "\n"
            else:
                line = " " + "- name: PDF-" + str(i + 1) + "\n"
            line += "   url: " + "\"" + self._value[i] + "\"" + "\n"
            res += line
        return {"links": res}

    def _get_element_value(self, soup: BeautifulSoup) -> List[str]:
        """gets all pdf links of the publication

        Parameters
        ----------
        soup
            soup of the ** ORE ** xml document of the publication.

        Returns
        -------
        List[str]
            all publicly available pdf links

        Notes
        -----
        How to find ORE xml document?
        In the same way of the OAI xml document but specifing
        ** "metdataPrefix=ore" **
        e.g.
        https://air.uniud.it/oai/request?verb=GetRecord&metadataPrefix=ore&identifier=oai:air.uniud.it:11390/1142576
        """
        result = []
        for child in soup.findAll("atom:" + self._tag_name):
            try:
                if child["type"] == "application/pdf"\
                        and not self._private_pdf(child["href"]):
                    result.append(child["href"])
            except KeyError:
                continue
        return result

    def _private_pdf(self, url: str) -> bool:
        """Checks if pdf is private or not

        Parameters
        ----------
        url : str
            url of the pdf

        Returns
        -------
        bool
            True if private, False otherwise
        """
        header = requests.get(url).headers
        if header["Content-Type"].startswith("application/pdf"):
            return False
        else:
            return True


class ElementsFactory:
    """Class factory for creation of metadata elements
    """

    def __init__(self):
        self._pub_builders = {}

    def register_type_of_element(self, type_of_element: str,
                                 builder: type) -> None:
        """register a new type of element for the factory

        Parameters
        ----------
        type_of_element
            string to identify that element
        builder
            class of the element
        """
        self._pub_builders[type_of_element.lower()] = builder

    def get_element(self, type_of_element: str) -> Element:
        """gets the element object requested

        Parameters
        ----------
        type_of_element
            the element to return

        Returns
        -------
        T
            The object specified by the string passed as parameter

        Raises
        ------
        ValueError
            If the element has not been registered before
        """
        builder = self._pub_builders.get(type_of_element.lower())
        if not builder:
            raise ValueError(str(type_of_element) + " is not registered")
        return builder


factory = ElementsFactory()

# CHECK THE FIRST ARGUMENT TO KNOW ALL AVAILABLE ELEMENTS

factory.register_type_of_element("title", Title)
factory.register_type_of_element("handle", Handle)
factory.register_type_of_element("publication type", PubType)
factory.register_type_of_element("authors", Authors)
factory.register_type_of_element("year", Year)
factory.register_type_of_element("abstract", Abstract)
factory.register_type_of_element("doi", Doi)
factory.register_type_of_element("pdf", Pdf)
factory.register_type_of_element("pages", Pages)
factory.register_type_of_element("volume", Volume)
factory.register_type_of_element("journal", Journal)
factory.register_type_of_element("book_title", BookTitle)
factory.register_type_of_element("publisher", Publisher)
factory.register_type_of_element("series", Series)
