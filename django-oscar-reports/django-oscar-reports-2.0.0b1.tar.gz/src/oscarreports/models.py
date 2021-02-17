from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import DateTimeRangeField
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import get_template
from celery.result import AsyncResult
from oscar.models.fields import NullCharField
from . import settings as app_settings
from .utils import GeneratorRepository
import uuid
import os.path
import io


def get_report_upload_path(instance, filename):
    # Upload files to {MEDIA_ROOT}/{OSCAR_REPORTS_UPLOAD_PREFIX}/{YYYY}/{MM}/{DD}/{uuid}.{ext}
    extension = os.path.splitext(filename)[1].replace('.', '')
    return '{prefix}/{date}/{uuid}.{ext}'.format(
        prefix=app_settings.OSCAR_REPORTS_UPLOAD_PREFIX,
        date=instance.created_on.strftime('%Y/%m/%d'),
        uuid=instance.uuid,
        ext=extension)


class Report(models.Model):
    STATUS_CREATED = 'created'
    STATUS_QUEUED = 'queued'
    STATUS_IN_PROGRESS = 'in-progress'
    STATUS_COMPLETED = 'completed'
    STATUS_NAMES = {
        STATUS_CREATED: _("Created"),
        STATUS_QUEUED: _("Queued"),
        STATUS_IN_PROGRESS: _("In-Progress"),
        STATUS_COMPLETED: _("Completed"),
    }

    # Unique ID used in URLs and filenames
    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)

    # Store a link to the content-type (model) which was used to generate this report.
    # Only user's with the `can_view` permission on this content-type will be able to
    # see this report.
    content_type = models.ForeignKey(ContentType,
        verbose_name=_("Content Type"),
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True)

    # Report Metadata
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name=_("Owner"),
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')
    type_code = models.CharField(_("Type Code"), max_length=50)
    description = models.TextField(_("Description"))
    date_range = DateTimeRangeField(_("Date Range"), null=True, blank=True)

    # Celery Task ID
    task_id = models.UUIDField(_("Background Task ID"), editable=False, unique=True, null=True, blank=True)

    # Status Timestamps
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    queued_on = models.DateTimeField(_("Queued On"), null=True, blank=True)
    started_on = models.DateTimeField(_("Started On"), null=True, blank=True)
    completed_on = models.DateTimeField(_("Completed On"), null=True, blank=True)

    # Report File Output
    mime_type = NullCharField(_("MIME Type"), max_length=20)
    report_file = models.FileField(_("Report File"),
        upload_to=get_report_upload_path,
        null=True,
        blank=True)


    def __str__(self):
        return str(self.uuid)


    @property
    def status(self):
        if self.completed_on:
            return self.STATUS_COMPLETED
        if self.started_on:
            return self.STATUS_IN_PROGRESS
        if self.queued_on:
            return self.STATUS_QUEUED
        return self.STATUS_CREATED


    @property
    def status_name(self):
        return self.STATUS_NAMES.get(self.status, "")


    @property
    def is_complete(self):
        return self.status == self.STATUS_COMPLETED


    @property
    def generator_class(self):
        generator = GeneratorRepository().get_generator(self.type_code)
        if not generator:
            raise ValueError("Can not queue report: no generator class was found.")
        return generator


    @property
    def celery_task_result(self):
        if not self.task_id:
            return
        task_id = str(self.task_id).encode()
        return AsyncResult(task_id)


    @property
    def celery_task_status(self):
        result_future = self.celery_task_result
        if result_future is None:
            return None
        status = result_future.status
        if status is None or status == 'PENDING':
            return None
        return str(status).title()


    def queue(self, delay=10, report_format='CSV'):
        # Reset metadata
        generator = self.get_generator(report_format)
        self.description = generator.report_description()
        self.queued_on = None
        self.started_on = None
        self.completed_on = None
        self.task_id = None
        self.save(update_fields=[
            'description',
            'queued_on',
            'started_on',
            'completed_on',
            'task_id',
        ])
        # Queue the task using celery
        from . import tasks
        task = tasks.generate_report.apply_async(args=[self.uuid, report_format], countdown=delay)
        # Update the task metadata
        self.queued_on = timezone.now()
        self.task_id = task.id
        self.save(update_fields=[
            'queued_on',
            'task_id',
        ])
        return task
    queue.alters_data = True


    def generate(self, report_format='CSV'):
        # Record start time
        self.started_on = timezone.now()
        self.save(update_fields=['started_on'])
        # Generate report content
        generator = self.get_generator(report_format)
        report = generator.generate()
        # Save generated content
        filename = self.get_filename(report_format)
        content = io.BytesIO(report.content)
        self.mime_type = report['content-type']
        self.report_file.save(filename, content)
        self.completed_on = timezone.now()
        self.save(update_fields=[
            'mime_type',
            'report_file',
            'completed_on',
        ])
        self.send_completed_alert()
    generate.alters_data = True


    def send_completed_alert(self):
        if not self.owner.email:
            return
        ctx = {
            'site': Site.objects.get_current(),
            'report': self,
        }
        subject = get_template('oscar/dashboard/reports/emails/report_completed_alert_subject.txt').render(ctx)
        subject = subject.replace('\n', '')
        text = get_template('oscar/dashboard/reports/emails/report_completed_alert_body.txt').render(ctx)
        html = get_template('oscar/dashboard/reports/emails/report_completed_alert_body.html').render(ctx)
        to_addrs = [self.owner.email]
        msg = EmailMultiAlternatives(subject, text, settings.OSCAR_FROM_EMAIL, to_addrs)
        msg.attach_alternative(html, "text/html")
        msg.send()
    send_completed_alert.alters_data = True


    def get_generator(self, report_format):
        kwargs = {
            'start_date': self.date_range.lower if self.date_range else None,
            'end_date': self.date_range.upper if self.date_range else None,
            'formatter': report_format,
        }
        return self.generator_class(**kwargs)


    def get_filename(self, report_format):
        return '{}.{}'.format(self.uuid, report_format.lower())
