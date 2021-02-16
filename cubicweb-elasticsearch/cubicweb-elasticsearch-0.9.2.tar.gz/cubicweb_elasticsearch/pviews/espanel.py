from datetime import datetime

from elasticsearch.client import Elasticsearch

from jinja2 import Environment, PackageLoader, select_autoescape

from pyramid_debugtoolbar.panels import DebugPanel


env = Environment(
    loader=PackageLoader("cubicweb_elasticsearch.pviews", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class ESDebugPanel(DebugPanel):
    """ES queries panel"""

    name = "ES"
    has_content = True
    template = "cubicweb_elasticsearch.pviews:templates/espanel.jinja2"
    title = "Queries"
    nav_title = "ElasticSearch"

    def __init__(self, request):
        self.data = {"request_path": request.path_info, "queries": {}}
        self.queries = []
        orig_search = Elasticsearch.search

        def traced_search(es_client, index=None, doc_type=None, body=None, **params):
            start = datetime.now()
            query = {
                "index": index,
                "doc_type": doc_type,
                "body": body,
                "params": params,
                "starttime": start,
                "response": {},
                "elapsed": 0,
            }
            self.queries.append(query)
            result = orig_search(es_client, index, doc_type, body, **params)
            elapsed = datetime.now() - start
            miliseconds = elapsed.seconds * 1000 + elapsed.microseconds / 1000
            query.update(
                {
                    "response": {
                        "hits": result.get("hits", []),
                        "aggregations": result.get("aggregations", {}),
                    },
                    "elapsed": miliseconds,
                }
            )
            return result

        Elasticsearch.search = traced_search

    def render_content(self, request):
        template = env.get_template("espanel.jinja2")
        return template.render(queries=self.queries)


def includeme(config):
    config.add_debugtoolbar_panel(ESDebugPanel)
