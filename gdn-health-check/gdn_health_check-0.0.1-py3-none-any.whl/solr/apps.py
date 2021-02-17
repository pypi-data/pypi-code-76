from django.apps import AppConfig

from health_check.plugins import plugin_dir


class HealthCheckConfig(AppConfig):
    name = 'gdn_health_check.solr'

    def ready(self):
        from .backends import GDNSolrHealthCheck
        plugin_dir.register(GDNSolrHealthCheck)
