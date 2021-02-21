
from fastutils import strutils

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.forms import ModelForm

from django_fastadmin.widgets import AceWidget

from .models import Server
from .models import Schedule
from .models import Result


class ServerAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "uid", "enable", "last_updated_time", "alive"]
    list_filter = ["enable"]
    search_fields = ["name", "description", "uid"]


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"
        widgets = {
            "script": AceWidget(ace_options={
                "mode": "ace/mode/sh",
                "theme": "ace/theme/twilight",
            }),
        }

class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_filter = ["server", "enable"]
    list_display = ["title", "server", "uid", "schedule", "enable", "code"]
    search_fields = ["title", "description", "uid", "schedule", "user", "script", "code"]
    readonly_fields = ["uid", "code"]

class ResultAdmin(admin.ModelAdmin):
    list_display = ["id", "schedule", "run_time", "code", "stdout_display", "stderr_display"]
    list_filter = ["schedule", "code"]
    search_fields = ["stdout", "stderr"]
    readonly_fields = ["schedule", "run_time", "code", "stdout", "stderr"]

    def stdout_display(self, obj):
        return obj.stdout and strutils.text_display_shorten(obj.stdout, 20) or "-"
    stdout_display.short_description = _("Stdout")

    def stderr_display(self, obj):
        return obj.stderr and strutils.text_display_shorten(obj.stderr, 20) or "-"
    stderr_display.short_description = _("Stderr")


admin.site.register(Server, ServerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Result, ResultAdmin)
