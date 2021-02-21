import uuid
import json

from fastutils import hashutils

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings

DJANGO_CRONTAB_MANAGER_OFFLINE_SECONDS = getattr(settings, "DJANGO_CRONTAB_MANAGER_OFFLINE_SECONDS", 60*5)

class Server(models.Model):
    name = models.CharField(max_length=64, verbose_name=_("Name"))
    uid = models.CharField(max_length=128, default=uuid.uuid4, unique=True, verbose_name=_("UUID"))
    aclkey = models.CharField(max_length=128, default=uuid.uuid4, verbose_name=_("Acl Key"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))
    last_updated_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Last Updated Time"))
    enable = models.BooleanField(default=True, verbose_name=_("Enable"))

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        return super().save(*args, **kwargs)

    def alive(self):
        if not self.last_updated_time:
            return None
        delta = timezone.now() - self.last_updated_time
        seconds = delta.total_seconds()
        if seconds <= DJANGO_CRONTAB_MANAGER_OFFLINE_SECONDS:
            return True
        else:
            return False
    alive.short_description = _("Alive")
    alive.boolean = True

class Schedule(models.Model):
    schedule_help_text = _("""Linux crontab schedule settings, e.g. * * * * *""")
    code_help_text = _("MD5 code of the schedule settings. It will be auto computed.")

    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name=_("Server"))
    uid = models.UUIDField(null=True, blank=True, default=uuid.uuid4, verbose_name=_("UUID"))
    title = models.CharField(max_length=128, verbose_name=_("Title"), help_text=_("Describe the scheduled task, so that we know what it is."))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    schedule = models.CharField(max_length=256, default="* * * * *", verbose_name=_("Schedule Settings"), help_text=schedule_help_text)
    user = models.CharField(max_length=64, default="root", verbose_name=_("Running User"))
    script = models.TextField(null=True, blank=True, verbose_name=_("Shell Script"))
    enable = models.BooleanField(default=True, verbose_name=_("Enable"))
    code = models.CharField(max_length=32, null=True, blank=True, verbose_name=_("Setting Code"), help_text=code_help_text)

    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        self.script = self.script and self.script.replace("\r\n", "\n") or ""
        self.code = self.get_code()
        return super().save(*args, **kwargs)

    def get_core_info(self):
        return {
            "uid": str(self.uid),
            "title": self.title,
            "description": self.description,
            "schedule": self.schedule,
            "user": self.user,
            "script": self.script,
            "enable": self.enable,
            "add_time": str(self.add_time),
            "mod_time": str(self.modify_time),
        }
    
    def get_code(self):
        info = self.get_core_info()
        info_str = json.dumps(info)
        return hashutils.get_md5_hexdigest(info_str)
    
    def info(self):
        info = self.get_core_info()
        info["code"] = self.code
        return info

class Result(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name=_("Schedule"))
    run_time = models.DateTimeField(verbose_name=_("Run Time"))
    code = models.IntegerField(null=True, blank=True, verbose_name=_("Script Exit Code"))
    stdout = models.TextField(null=True, blank=True, verbose_name=_("Stdout Message"))
    stderr = models.TextField(null=True, blank=True, verbose_name=_("Stderr Message"))

    class Meta:
        verbose_name = _("Result")
        verbose_name_plural = _("Results")

    def __str__(self):
        return str(self.pk)
