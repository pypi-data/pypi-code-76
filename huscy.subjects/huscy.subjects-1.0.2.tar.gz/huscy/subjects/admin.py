from django.contrib import admin

from huscy.subjects import models


class ChildAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class PatientAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(models.Address)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.Contact)
admin.site.register(models.Inactivity)
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Note)
admin.site.register(models.Subject)
