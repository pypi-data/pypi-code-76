import os
import re
import platform
import subprocess
from rdflib import Graph, Namespace, RDF, URIRef, BNode
import validators
import random
from enum import Enum
from urllib.parse import urlparse


dsp_repo = Namespace("http://ns.dasch.swiss/repository#")


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def areURLs(urls: list):
    for url in urls:
        if not url:
            continue
        if not isURL(url):
            return False
    return True


def isURL(url: str):
    if url and not url.isspace():
        if validators.url(url):
            return True
        if validators.url('http://' + url):
            return True
        # LATER: good enough?
        # if validators.url('http://www.' + url):
        #     return True
    return False


def get_url_property_id(url: str) -> str:
    """
    This method tries to guess the propetyID for a URL.

    For certain pre-defined cases, a reasonable propertyID is chosen;
    otherwise, the net location is being extracted, if possible.

    Args:
        url (str): a URL

    Returns:
        str: a propertyID
    """
    if re.search(r'skos\.um\.es', url):
        return "SKOS UNESCO Nomenclature"
    if re.search(r'geonames\.org', url):
        return "Geonames"
    if re.search(r'pleiades\.stoa\.org', url):
        return "Pleiades"
    if re.search(r'orcid\.org', url):
        return "ORCID"
    if re.search(r'viaf\.org', url):
        return "VIAF"
    if re.search(r'\/gnd\/', url) or re.search(r'portal\.dnb\.de', url):
        return "GND"
    if re.search(r'n2t\.net\/ark\:\/99152', url):
        return "Periodo"
    if re.search(r'chronontology\.dainst\.org', url):
        return "ChronOntology"
    if re.search(r'creativecommons\.', url):
        return "Creative Commons"
    # LATER: propertyID's for common institutions
    loc = urlparse(url).netloc
    if len(loc.split('.')) > 2:
        return '.'.join(loc.split('.')[1:])
    if loc:
        return loc
    return url[:12]


def are_emails(mails: list):
    for mail in mails:
        if not mail:
            continue
        if not is_email(mail):
            return False
    return True


def is_email(mail: str):
    if mail and not mail.isspace():
        if validators.email(mail):
            return True
    return False


def get_coherent_graph(g: Graph) -> Graph:
    project = list(g.subjects(RDF.type, dsp_repo.Project))[0]
    traversed = []
    to_visit = [project]

    while to_visit:
        x = to_visit.pop()
        traversed.append(x)
        for _, p, o in g.triples((x, None, None)):
            if p != RDF.type and isinstance(o, (URIRef, BNode)) and o not in traversed:
                to_visit.append(o)
        for new_x in g.subjects(object=x):
            if new_x not in traversed:
                to_visit.append(new_x)

    for s, p, o in g:
        if s not in traversed:
            g.remove((s, None, None))

    return g


class Validity(Enum):
    VALID = 0
    INVALID_VALUE = 1
    REQUIRED_VALUE_MISSING = 2
    OPTIONAL_VALUE_MISSING = 3


class Cardinality(Enum):
    """
    A set of cardinalities that may be used for properties.
    """
    UNBOUND = 0
    ONE = 1
    ZERO_OR_ONE = 2
    ONE_TO_UNBOUND = 3
    ONE_TO_TWO = 4
    ZERO_TO_TWO = 5
    ONE_TO_UNBOUND_ORDERED = 6

    def get_optionality_string(card) -> str:
        """
        Returns wether or not a cardinality is optional.

        Args:
            card (Cardinality): the cardinality in question

        Returns:
            str: "Mandatory" or "Optional", depending on the cardinality
        """
        if Cardinality.isMandatory(card):
            return "Mandatory"
        else:
            return "Optional"

    def isMandatory(card) -> bool:
        if card == Cardinality.ONE \
                or card == Cardinality.ONE_TO_TWO \
                or card == Cardinality.ONE_TO_UNBOUND \
                or card == Cardinality.ONE_TO_UNBOUND_ORDERED:
            return True
        if card == Cardinality.UNBOUND \
                or card == Cardinality.ZERO_OR_ONE \
                or card == Cardinality.ZERO_TO_TWO:
            return False

    def as_sting(card) -> str:
        if card == Cardinality.UNBOUND:
            return "Unbound: 0-n values"
        elif card == Cardinality.ONE:
            return "Exactly one value"
        elif card == Cardinality.ZERO_OR_ONE:
            return "Optional: Zero or one value"
        elif card == Cardinality.ONE_TO_UNBOUND:
            return "Mandatory unbound: 1-n values"
        elif card == Cardinality.ONE_TO_TWO:
            return "One or two values"
        elif card == Cardinality.ZERO_TO_TWO:
            return "Optional: Zero, one or two values"
        elif card == Cardinality.ONE_TO_UNBOUND_ORDERED:
            return "Mandatory unbound: 1-n values (ordered)"


class Datatype(Enum):
    """
    A set of cardinalities that may be used for properties.
    """
    STRING = 0
    DATE = 1
    STRING_OR_URL = 2
    PLACE = 3
    PERSON_OR_ORGANIZATION = 4
    GRANT = 5
    DATA_MANAGEMENT_PLAN = 6
    URL = 7
    CONTROLLED_VOCABULARY = 8
    PROJECT = 9
    ATTRIBUTION = 10
    EMAIL = 11
    ADDRESS = 12
    PERSON = 13
    ORGANIZATION = 14
    DOWNLOAD = 15
    SHORTCODE = 16


class IRIFactory():

    @staticmethod
    def _get_all_iris(object_type: str, meta):
        try:
            if object_type == 'dataset':
                return [d.iri_suffix for d in meta.dataset]
            elif object_type == 'person':
                return [d.iri_suffix for d in meta.persons]
            elif object_type == 'organization':
                return [d.iri_suffix for d in meta.organizations]
            elif object_type == 'grant':
                return [d.iri_suffix for d in meta.grants]
            else:
                return []
        except Exception:
            return []

    @classmethod
    def get_unique_iri(cls, object_type: str, meta) -> str:
        existing = cls._get_all_iris(object_type, meta)
        for i in range(999):
            new = f"-{object_type}-{str(i).zfill(3)}"
            if new not in existing:
                return new
        return f"-{object_type}-{str(random.randint(1000,1000000)).zfill(7)}"
