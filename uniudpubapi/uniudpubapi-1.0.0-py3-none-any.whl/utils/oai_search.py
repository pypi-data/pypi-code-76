from bs4 import BeautifulSoup
import requests


def build_oai_url(handle: str,
                  prefix: str,
                  base_url: str = "https://air.uniud.it/oai/request?") -> str:
    """build the url for an oai request of a single record (in the case of
    institutional repository, one record corresponds to a publication)

    Parameters
    ----------
    handle
        entire handle of the publication (e.g. "http://hdl.handle.net/11390/693468")
    prefix
        prefix for the oai request.
        Accepted values:
        - "oai"
        - "ore"
    base_url : optional
        url of the oai repository, by default "https://air.uniud.it/oai/request?"

    Returns
    -------
    str
        url of the publication
    """
    pub_id = handle.split("/")
    oai_url = base_url + "verb=GetRecord&" \
        + "metadataPrefix=" + prefix \
        + "&identifier=oai:air.uniud.it:" \
        + pub_id[-2] + "/" + pub_id[-1]
    return oai_url


def get_oai_xml_response(handle: str, prefix: str = "oai_dc") -> BeautifulSoup:
    """[summary]

    Parameters
    ----------
    handle
        entire handle of the publication (e.g. "http://hdl.handle.net/11390/693468")
    prefix
        prefix for the oai request.
        Accepted values:
        - "oai"
        - "ore"

    Returns
    -------
    BeautifulSoup
        soup of the single publication identified by the guid

    Raises
    ------
    ConnectionError
        If there is a connection error during the process
    """
    record_url = build_oai_url(handle, prefix)
    try:
        var_response = requests.get(record_url)
    except ConnectionError:
        raise
    else:
        soup = BeautifulSoup(var_response.content, "lxml")
        if soup.find("error"):
            raise ConnectionError(" The publication identified by the following "
                                  + "handle " + handle
                                  + " hasn't been inserted into OAI"
                                  + "repository")
        return soup
