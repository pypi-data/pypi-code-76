"""Import project."""
from cmem.cmempy import config
from cmem.cmempy.api import send_request


def get_import_uri():
    """Get endpoint URI pattern for project import."""
    path = "/workspace/projects/{}/import/{}"
    return config.get_di_api_endpoint() + path


def import_project_rdf_turtle(project_name, rdf_turtle_string):
    """Import DI Project from RDF Turtle (without resource files)."""
    import_uri = get_import_uri().format(project_name, "rdfTurtle")
    response = send_request(
        import_uri,
        method="POST",
        data=rdf_turtle_string.encode("utf-8")
    )
    return response


def import_project(project_name, file_path, plugin_name="xmlZip"):
    """Import DI Project from RDF Turtle (without resource files)."""
    import_uri = get_import_uri().format(project_name, plugin_name)
    with open(file_path, 'rb') as data:
        response = send_request(
            import_uri,
            method="POST",
            data=data
        )
    return response
