"""Utility functions for CLI interface."""

import os
import re
import unicodedata

from cmem.cmempy.dp.proxy.graph import get_graphs_list

NAMESPACES = {
    "void": "http://rdfs.org/ns/void#",
    "di": "https://vocab.eccenca.com/di/",
    "shui": "https://vocab.eccenca.com/shui/",
    "dsm": "https://vocab.eccenca.com/dsm/",
    "owl": "http://www.w3.org/2002/07/owl#"
}


def is_completing():
    """Test for environment which indicates that we are in completion mode.

    Returns true if in validation mode, otherwise false.

    Returns: boolean
    """
    comp_words = os.getenv("COMP_WORDS", default=None)
    cmemc_complete = os.getenv("_CMEMC_COMPLETE", default=None)
    if comp_words is not None:
        return True
    if cmemc_complete is not None:
        return True
    return False


def iri_to_qname(iri):
    """Return a qname for an IRI based on well known namespaces.

    In case of no matching namespace, the full IRI is returned.

    Args:
        iri:

    Returns: string
    """
    for prefix in NAMESPACES:
        namespace = NAMESPACES[prefix]
        iri = iri.replace(namespace, prefix + ":")
    return iri


def read_rdf_graph_files(directory_path):
    """Read all files from directory_path and output as tuples.

    The tuple format is (filepath, graph_name),
    for example ("/tmp/rdf.nt", "http://example.com")
    """
    rdf_graphs = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            full_file_path = os.path.join(root, _file)
            graph_file_name = _file + ".graph"
            full_graph_file_name_path = os.path.join(
                root,
                graph_file_name
            )
            if(not _file.endswith(".graph")
               and os.path.exists(full_graph_file_name_path)):
                graph_name = read_file_to_string(
                    full_graph_file_name_path
                ).strip()
                rdf_graphs.append(
                    (full_file_path, graph_name)
                )
    return rdf_graphs


def read_ttl_files(directory_path):
    """Read all files from directory_path.

    Filter the files which ends with .ttl
    Returns list of tuples (full_path_to_file, filename)
    """
    ttl_files = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            full_file_path = os.path.join(root, _file)
            if _file.endswith(".ttl"):
                ttl_files.append(
                    (full_file_path, _file)
                )
    return ttl_files


def read_file_to_string(file_path):
    """Read file to string."""
    with open(file_path, "rb") as _file:
        return _file.read().decode("utf-8")


def get_graphs(writeable=True, readonly=True):
    """Retrieve list of accessible graphs from DP endpoint.

    readonly=True|writeable=True outputs all graphs
    readonly=False|writeable=True outputs only writeable graphs
    readonly=True|writeable=False outputs graphs without write access
    (but read access)
    """
    all_graphs = get_graphs_list()
    filtered_graphs = []
    for graph in all_graphs:
        if graph['writeable'] and writeable:
            filtered_graphs.append(graph)
        if not graph['writeable'] and readonly:
            filtered_graphs.append(graph)
    return filtered_graphs


def get_graphs_as_dict(writeable=True, readonly=True):
    """Get the graph response as dict with IRI as main key."""
    graph_dict = {}
    for graph in get_graphs(writeable=writeable, readonly=readonly):
        graph_dict[graph["iri"]] = graph
    return graph_dict


def convert_uri_to_filename(value, allow_unicode=False):
    """Convert URI to unix friendly filename.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert / to underscore. Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value)\
            .encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'\.', '_', value.lower())
    value = re.sub(r'/', '_', value.lower())
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
