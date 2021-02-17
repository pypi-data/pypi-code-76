from django.contrib import admin
from .models import Log, Report

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    using = 'log'

    def get_queryset(self, request):
        return super(LogAdmin, self).get_queryset(request).using(self.using)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    using = 'log'

    list_display = ['id', 'index', 'status', 'created_at']
    list_filter = ['created_at', 'status', 'index']
    search_fields = ['index']

    def get_queryset(self, request):
        return super(ReportAdmin, self).get_queryset(request).using(self.using)
