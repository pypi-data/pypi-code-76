from __future__ import absolute_import
from celery import shared_task



@shared_task(ignore_result=True)
def generate_report(report_uuid, report_format):
    from . import models
    report = models.Report.objects.get(uuid=report_uuid)
    report.generate(report_format)
