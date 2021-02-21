from django.contrib import admin
from .models import ApiResponseTimeLog
from .models import ApiResponseTimeStats

class ApiResponseTimeLogAdmin(admin.ModelAdmin):
    list_display = ["pk", "path", "response_time", "add_time"]
    list_filter = ["path"]
    ordering = ["add_time"]

class ApiResponseTimeStatsAdmin(admin.ModelAdmin):
    list_display = ["path", "count", "min_response_time", "avg_response_time", "max_response_time"]
    list_filter = ["path"]
    search_fields = ["path"]

admin.site.register(ApiResponseTimeLog, ApiResponseTimeLogAdmin)
admin.site.register(ApiResponseTimeStats, ApiResponseTimeStatsAdmin)
