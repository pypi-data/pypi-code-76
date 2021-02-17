from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin, DeleteView
from django.views.generic.detail import BaseDetailView
from django.http import FileResponse, Http404
from django_tables2 import SingleTableView
from psycopg2.extras import DateTimeTZRange
from .models import Report
from .tables import ReportTable
from .forms import ReportForm
import os.path


class IndexView(FormMixin, SingleTableView):
    template_name = 'oscar/dashboard/reports/index.html'
    table_pagination = True
    model = Report
    table_class = ReportTable
    context_table_name = 'reports'
    desc_template = ''
    description = ''

    form_class = ReportForm

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-queued_on')
        return queryset


    def get_table_pagination(self, table):
        return dict(per_page=20)


    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            # Create report
            report = Report()
            report.content_type = None
            report.owner = request.user
            report.type_code = self.form.cleaned_data['report_type']
            report.date_range = DateTimeTZRange(
                lower=self.form.cleaned_data['date_from'],
                upper=self.form.cleaned_data['date_to'])
            report.save()
            # Queue report
            report.queue()
            # Message user
            messages.info(request, _("Successfully queued report for generation"))
            return redirect('dashboard:reports-index')
        return self.get(request, *args, **kwargs)


    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = _("Reports")
        return table


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class ReportDownloadView(BaseDetailView):
    model = Report
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def render_to_response(self, context, **response_kwargs):
        report = context['object']
        if not report.report_file.name:
            raise Http404()
        # Build filename
        extension = os.path.splitext(report.report_file.name)[1].replace('.', '')
        filename = '{date}_{type_code}_{uuid}.{ext}'.format(
            date=report.created_on.strftime('%Y-%m-%d'),
            type_code=report.type_code,
            uuid=report.uuid,
            ext=extension)
        # Send file to client
        resp = FileResponse(report.report_file,
             as_attachment=True,
             filename=filename)
        resp['Content-Type'] = report.mime_type
        return resp


class ReportDeleteView(DeleteView):
    model = Report
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    success_url = reverse_lazy('dashboard:reports-index')
    template_name = 'oscar/dashboard/reports/report_confirm_delete.html'
