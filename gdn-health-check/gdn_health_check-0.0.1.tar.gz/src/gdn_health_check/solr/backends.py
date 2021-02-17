import logging, pysolr

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable

from django.conf import settings
from requests.auth import HTTPBasicAuth

class GDNSolrHealthCheck(BaseHealthCheckBackend):
    def authentication(self):
        username = settings.SOLR_USERNAME
        password = settings.SOLR_PASSWORD
        if username and password:
            return HTTPBasicAuth(username, password)
        return None

    def check_status(self):
        try:
            # Create a client instance. The timeout and authentication options are not required.
            solr = pysolr.Solr(settings.SOLR_URL, always_commit=False, timeout=3, auth=self.authentication())

            # Do a health check to root path.
            solr.ping(handler='')

            return True
        except Exception as e:
            print(e)
            raise ServiceUnavailable('Unable access SOLR server') from e
