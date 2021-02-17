from django.conf.urls import url
from oscar.apps.dashboard.reports import apps
from oscar.core.loading import get_class


class ReportsDashboardConfig(apps.ReportsDashboardConfig):
    name = 'oscarreports'


    def ready(self):
        super().ready()
        from . import handlers  # NOQA
        self.index_view = get_class('reports_dashboard.views', 'IndexView')
        self.download_view = get_class('reports_dashboard.views', 'ReportDownloadView')
        self.delete_view = get_class('reports_dashboard.views', 'ReportDeleteView')


    def get_urls(self):
        urls = [
            url(r'^$',
                self.index_view.as_view(), name='reports-index'),
            url(r'^(?P<uuid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/download/$',
                self.download_view.as_view(), name='reports-download'),
            url(r'^(?P<uuid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/delete/$',
                self.delete_view.as_view(), name='reports-delete'),
        ]
        return self.post_process_urls(urls)
